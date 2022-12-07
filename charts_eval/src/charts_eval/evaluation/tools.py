import os
import sys
from datetime import datetime
import yaml
import urllib

import charts_eval.config as config
import charts_eval.evaluation.utils as utils
from charts_eval.evaluation.chart import Chart
from charts_eval.evaluation.templates import get_logs_prefix

tools_list = ["pss", "badrobot", "images"]

def _evaluate_pss(chart: Chart) -> dict:
    psa_checker_path = "psa-checker"
    psa_version = "0.0.1"
    # psa_version = subprocess.getoutput(psa_checker_path + ' --version')
    # psa_version = psa_version[len("psa-checker version "):]

    start = datetime.now()
    now = start.strftime("%Y-%m-%d, %H:%M:%S")
    template       = chart.status["template_filename"]
    logs_prefix    = get_logs_prefix(chart)
    log_baseline   = logs_prefix + "_baseline.log"
    log_restricted = logs_prefix + "_restricted.log"

    n_evaluated=0
    n_non_evaluable=0
    n_wrong_version=0
    n_crd=0
    
    if utils.is_file_empty(template):
        print("**Error, no template generated or empty at %s" % template)
        sys.exit(1)
    else: 
        print("  PSS evaluation: baseline")
        baseline   = os.system('cat "' + template + '" | ' + psa_checker_path + " --level baseline   -f - >" + log_baseline + " 2>&1")
        print("  PSS evaluation: restricted")
        restricted = os.system('cat "' + template + '" | ' + psa_checker_path + " --level restricted -f - >" + log_restricted + " 2>&1")
        n_evaluated     = utils.count_in_file("PSS level", log_restricted) - 1
        n_non_evaluable = utils.count_in_file("Kind not evaluable", log_restricted)
        n_wrong_version = utils.count_in_file("not evaluable for kind:", log_restricted)
        n_crd = utils.count_in_file("Non standard k8s node found", log_restricted)
        print("    Objects non-evaluable: " + str(n_non_evaluable))
        print("    Objects evaluated: " + str(n_evaluated))
        print("    Objects CRD: " + str(n_crd))
        print("    Objects wrong version: " + str(n_wrong_version))
        
        if n_wrong_version > 0:
            level = "version_not_evaluable"
        elif ( n_evaluated+n_non_evaluable + n_crd ) == 0:
            level = "empty_no_object"
        elif n_evaluated == 0:
            if n_crd == 0:
                level = "no_pod_object"
            else:
                level = "no_pod_object_but_crd"
        elif ( restricted == 0 and baseline == 0 ):
            level = "restricted"
        elif ( baseline == 0 ):
            level = "baseline"
        else:
            level = "privileged"

    print("  Level: " + level)

    psa_dict = {
        "chart_version" : chart.version,
        "tool_version": psa_version,
        "date": now,
        "status": "evaluated",
        "data": {
            "level" : level,
            "n_evaluated": n_evaluated, 
            "n_non_evaluable":n_non_evaluable,
            "n_crd": n_crd,
            "n_wrong_version":n_wrong_version,
        }
    }

    return psa_dict

# --------------------------------------------------------------------

def _evaluate_badrobot(chart: Chart) -> dict:
    template       = chart.status["template_filename"]
    logs_prefix    = get_logs_prefix(chart)
    log_badrobot   = logs_prefix + "_badrobot.log"
    now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    br_version = '0.0.1'

    os.system("badrobot scan " + template + " > " + log_badrobot )
    os.system("cat " + log_badrobot + " | jq '[.[].score] | add' > " + log_badrobot + "_sum")
    with open(log_badrobot+"_sum") as f:
        score_badrobot = f.readline().strip('\n')
    print("    Score: %s" % score_badrobot)
    result = {
        "chart_version" : chart.version,
        "tool_version": br_version,
        "date": now,
        "status": "evaluated",
        "data": {
            "score": score_badrobot,
        }
    }
    return result

# --------------------------------------------------------------------

def _evaluate_images(chart: Chart) -> dict:
    template       = chart.status["template_filename"]
    log_images   = get_logs_prefix(chart) + "_images.log"
    now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    tool_version = "0.0.1"
    images_data=[]

    error = os.system("cat " + template + " | yq '..|.image? | select(.)' | sort -u > " + log_images )
    if error == 0:
        with open(log_images) as f: images = f.readline()
        for img in images.split("\n"):
            if img != '' and img != '---':
                images_data.append(img)

    print("    Images: %s" % images_data)

    result = {
        "chart_version" : chart.version,
        "tool_version" : tool_version,
        "data": images_data,
        "date": now
    }
    return result

# --------------------------------------------------------------------

def _evaluate_tool(chart: Chart, tool: str) -> dict:
    """Returns dictionary with evaluation result from tool"""
    if tool=="pss":
        result = _evaluate_pss(chart)
    elif tool=="badrobot":
        result = _evaluate_badrobot(chart)
    elif tool=="images":
        result = _evaluate_images(chart)
    else:
        print("**Error, tool not found %s" % tool)
    
    chart.tools[tool]=result

# --------------------------------------------------------------------

def evaluate(charts_db: dict, force: bool):
    """Evaluate tools on all charts and store results on charts db"""

    start = datetime.now()
    i = j = 1
    keys = charts_db.keys()
    for key in keys:
        chart = Chart(charts_db[key])
        print("# [%s/%s] %s / %s %s" % \
            (i, len(charts_db), chart.repo, chart.name, chart.version))
        i+=1
        for tool in tools_list:
            if not chart.is_generated():
                chart.tools[tool]={}
            elif force or chart.needs_evaluation(tool):
                print("  Adding %s evaluation" % tool)
                _evaluate_tool(chart, tool)
                j += 1
        charts_db[key] = chart.get_dict()

    print( "# Result of evaluation for all charts with tools")
    print( "%s tools: %s" % (len(tools_list), tools_list))
    print( "%s new chart tool evaluations" % ( j - 1 ) )
    print( "%s total charts processed in %s" % (len(keys), ( datetime.now() - start ) ))