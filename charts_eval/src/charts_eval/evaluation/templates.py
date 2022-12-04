import os
from datetime import datetime
from urllib import parse

from charts_eval.evaluation.chart import Chart
import charts_eval.config as config
import charts_eval.evaluation.utils as utils

def _logs_prefix( chart: Chart ) -> str:
    # TODO: Make sure there is no collision with slugify names
    return config.logs_dir + "/" + \
        parse.quote(chart.repo + "_" + chart.name + "_" + chart.version)

def _log_helm( chart: Chart ) -> str:
    return _logs_prefix(chart) + "_helm.log"

def _download_template( chart: Chart ) -> bool:
    """Returns True on error"""
    print("  Downloading chart")
    url = parse.quote_plus(chart.url)
    log_helm = _log_helm(chart)
    os.system( "helm repo add " + chart.repo + " " + url + " 1>" + log_helm + " 2>&1")
    repo_update = os.system( \
        "helm repo update " + chart.repo + " 1>>" + log_helm + " 2>&1")
    if repo_update >0 or utils.is_in_file("cannot be reached", log_helm):
        return True
    return False

def _generate_template( chart: Chart ) -> bool:
    """Returns True on error"""
    template = _logs_prefix(chart) + "_template.yaml"
    log_helm = _log_helm(chart)
    gen_template = 0
    if not os.path.exists(template):
        # TODO: retry previously errored templates
        print("  Generating template")
        command = "helm template " + \
            '"' + parse.quote_plus(chart.repo) + "/" + parse.quote_plus(chart.name) + '"' + \
            " --version " + chart.version + " >" + template + " 2>>" + log_helm
        print(command)
        gen_template = os.system(command)
    else:
        print("  Template cached")
        return False
    # template_data = Path(template).read_text()
    if ( gen_template > 0 or utils.is_in_file("error", log_helm)):
        return True
    return False

def generate( charts_db_source: dict, charts_db: dict ):
    """Generate template files on cache dir and store status on charts db"""
    now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    # TODO: delete old log and templates to save disk space
    # TODO: Remove evaluated charts that no longer appear in Artifact Hub
    i=0
    for dic_chart in charts_db_source:
        # chart is from source if it doesn't exists in db
        chart = Chart(dic_chart)

        if chart.key in charts_db:
            # we copy existing chart info for tools evaluation
            chart_prev = Chart( charts_db[chart.key] )
            chart.tools = chart_prev.tools

        i+=1
        print("# [%s/%s] %s / %s %s" % \
            (i, len(charts_db_source), chart.repo, chart.name, chart.version))
        status="generated"
        error = False
        if not os.path.exists( _log_helm(chart) ):
            error = _download_template(chart)

        if error:
            print("  **Error downloading chart")
            status = "error_download"        
        else:
            error = _generate_template(chart)
            if ( error ):
                print("  **Error generating template")
                status = "error_template"

        chart.status = {
            "cache" : status,
            "chart_version" : chart.version,
            "datetime" : now,
        }
        charts_db[chart.key] = chart.get_dict()
