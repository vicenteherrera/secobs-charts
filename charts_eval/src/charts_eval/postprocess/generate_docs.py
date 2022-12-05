import yaml
import os
import sys
from datetime import datetime
from string import ascii_lowercase


from charts_eval.config import charts_db_filename, doc_filename_prefix
from charts_eval.evaluation.utils import load_yaml

def get_chart_name(url: str):
    parts = url.split("/")
    user  = parts[ len(parts) - 1 ]
    return user

def generate_docs():

    print("# Reading charts db")
    charts_db = load_yaml(charts_db_filename)

    # print("# Ordering charts alphabetically")
    # charts_source.sort(key=lambda x: x["repository"]["name"] + " " + get_chart_name( x["url"] ) )

    print("# Iterating charts")
    keys = charts_db.keys()

    # It's more optimal to loop all charts once and process each tool,
    # but it's more complex to understand, and anyway this is very fast

    # PSS -----------------------------------------------------------
    print("# Calculate PSS statistics")

    count = {
        "total":0,
        "privileged":0,
        "baseline":0,
        "restricted":0,
        "error_download":0,
    }
    calpha = {}
    for l in ascii_lowercase:
        calpha[l]=0

    i=0
    max_date = ""

    for key in keys:
        dic_chart = charts_db[key]
        level = "unknown"
        i += 1
        calpha[dic_chart["repository"]["name"][0]] += 1

        if "status" in dic_chart and "cache" in dic_chart["status"]:
            # default status includes error downloading chart or generating the template
            level = dic_chart["status"]["cache"]
        else:
            print("Chart status not found for %s" % dic_chart["repository"]["name"] )

        if "tools" not in dic_chart:
            print( "No tools evaluation for %s" % dic_chart["repository"]["name"] )
        elif level[0:5]!="error":
            if "pss" in dic_chart["tools"]:
                pss_level = dic_chart["tools"]["pss"]["data"]["level"]
                if pss_level != "": level = pss_level
                if dic_chart["tools"]["pss"]["date"] > max_date:
                    max_date = dic_chart["tools"]["pss"]["date"]

        count["total"] +=1
        if level not in count: count[level] = 1
        else: count[level] += 1

    # Badrobot -----------------------------------------------------------
    print("# Calculate Badrobot statistics")

    # Initi Badrobot bucket calc
    br_buckets = {}
    br_min_buckets = -700
    br_size_buckets = -50
    br_min = br_non_evaluable = br_no_workload = br_blank = br_zero = 0
    for i in range(0, br_min_buckets, br_size_buckets):
        br_buckets[str(i)] = 0

    i=0
    for key in keys:
        dic_chart = charts_db[key]
        level = "unknown"
        i += 1

        if "status" in dic_chart and "cache" in dic_chart["status"]:
            # status includes error downloading chart or generating the template
            level = dic_chart["status"]["cache"]
        if level[0:5] == "error":
            print( "Skipping chart in error %s" % dic_chart["repository"]["name"] )
            br_non_evaluable += 1
        elif "tools" not in dic_chart or \
            "badrobot" not in dic_chart["tools"] or \
            "data"     not in dic_chart["tools"]["badrobot"] or \
            "score"    not in dic_chart["tools"]["badrobot"]["data"]:
            print( "No badrobot evaluation for %s" % dic_chart["repository"]["name"] )
            br_non_evaluable += 1
        else:
            score = dic_chart["tools"]["badrobot"]["data"]["score"]
            if score == "":
                print( "Blank score for %s" % dic_chart["repository"]["name"] )
                br_blank += 1
            elif level in ["empty_no_object", "no_pod_object_but_crd", "no_pod_object"]:
                # TODO: decouple from PSS evaluation
                br_no_workload += 1
            else:
                score = int(score)
                if score < br_min: br_min = int(score)
                if score == 0: br_zero += 1
                for i in range(0, br_min_buckets + br_size_buckets, br_size_buckets):
                    if i >= score and score > ( i + br_size_buckets ):
                        br_buckets[str(i)] += 1
                        break


    header = "[Go to root documentation](https://vicenteherrera.com/secobs-charts)  \n"
    header += "[Go to index of charts evaluation](https://vicenteherrera.com/secobs-charts/docs/generated/charts_levels)\n\n"
    header += "## Artifact Hub's Helm charts evaluation\n\n"
    max_date = "Evaluation date: " + max_date + "\n"
    list_md = open(doc_filename_prefix+".md", "w")
    list_md.write(header + "Source: [Artifact Hub](https://artifacthub.io/)  \n" + max_date + "\n### Pod Security Standards (PSS)\n\n")
    list_md.write("[Pod Security Standards (PSS)](https://kubernetes.io/docs/concepts/security/pod-security-standards/) define three levels of security (restricted, baseline and privileged) that can be enforced for pods in a namespace. Evaluation done with [psa-checker](https://vicenteherrera.com/psa-checker/) command line tool, that checks into Kubernetes objects that can create pods.\n\n")
    list_md.write("| Category | Quantity | Percentage |\n|------|------|------|\n")
    for key in count.keys():
        list_md.write("| " + key.capitalize() + " | " + str(count[key]) + " | ")
        list_md.write( str(round(100*count[key]/count["total"],2))+"% |\n" )
    list_md.write("\n")
    list_md.write("Legend:\n")
    list_md.write(" * PSS level:\n")
    list_md.write("   * Privileged: Pod specs makes use of privileged settings, the most insecure. Containers are able to access host capabilities.\n")
    list_md.write("   * Baseline: Pod specs without extra security or extra privileges. Doesn't account for CRD that may create pods.\n")
    list_md.write("   * Restricted: Pod specs follow the best security practices, like requiring containers to not run as root, and drop extra capabilities. Doesn't account for CRDs that may create pods.\n")
    list_md.write(" * Error_download: Downloading the template from original source wasn't possible.\n")
    list_md.write(" * Error_template: Rendering the template without providing parameters resulted in error.\n")
    list_md.write(" * No_pod_object_but_crd: The chart didn't render any object that can create pods, but has CRD that could do so.\n")
    list_md.write(" * No_pod_object_no_crd: The chart didn't render any object that can create pods nor CRDs.\n")
    list_md.write(" * Version_not_evaluable: The cart includes deployment, daemonset, etc. of v1beta1 that can't be evaluated by the library.\n")
    list_md.write("\n")

    list_md.write("### Operator evaluation with BadRobot score\n\n")
    list_md.write("[BadRobot](https://github.com/controlplaneio/badrobot) evaluates how secure Kubernetes operators are. For each operator included in a chart, a score is calculated with a set of security practices. The closer to zero the score, the better.\n\n")
    # list_md.write("Worse score: " + str(brmin)+"\n\n")
    list_md.write("| Score | Number of charts |\n|------|------|\n")
    list_md.write("| Non-evaluable | " + str(br_non_evaluable) + " |\n")
    list_md.write("| Blank score | " + str(br_blank) + " |\n")
    list_md.write("| No workload | " + str(br_no_workload) + " |\n")
    list_md.write("| Score == 0 | " + str(br_zero) + " |\n")

    keys = br_buckets.keys()
    for key in keys:
        list_md.write("| [" + str(key) + ", " + str(int(key) + br_size_buckets) + ") | " + str(br_buckets[key]) + " |\n")

    list_md.write("\n### Charts list\n\n")

    # Create index links
    index = "[main](./charts_levels)&nbsp; "
    for l in ascii_lowercase:
        index += "["+l.upper()+"("+str(calpha[l])+")](./charts_levels_"+l+")&nbsp; "
    list_md.write("Alphabetical list of all repositories (number of charts in parenthesis):\n\n")
    list_md.write(index)

    print("# Iterating all charts")
    i=0
    last_letter=""
    keys = charts_db.keys()    
    for key in keys:
        dic_chart = charts_db[key]
        repo        = dic_chart["repository"]["name"]
        url         = dic_chart["repository"]["url"]
        version     = dic_chart["version"]
        app_version = dic_chart["app_version"]
        parts       = dic_chart["url"].split("/")
        chart        = get_chart_name( dic_chart["url"] )
        letter = repo[0]
        i+=1

        if letter != last_letter:
            last_letter = letter
            # print("# Writing header: "+letter)
            list_md.close()
            list_md = open(doc_filename_prefix+"_"+letter+".md", "w")
            list_md.write(header + max_date + "\n" + index)
            list_md.write("\n\n| repo | chart | PSS level | BadRobot score | chart version | app version |\n")
            list_md.write("|------|------|------|------|------|------|\n")

        level = ""
        brscore = ""
        if "pss" in dic_chart:
            level = dic_chart["tools"]["pss"]["level"]
            if "badrobot" in dic_chart:
                brscore = dic_chart["tools"]["badrobot"]["score"]
        list_md.write("| [" + repo + "](" + url + ") | " + chart + " | " + level  + " | " + brscore  + " | " + version + " | " + app_version  + " |\n")


    list_md.close()
