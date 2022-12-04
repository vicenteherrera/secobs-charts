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

    print("# Reading charts")
    charts_pss = load_yaml(charts_db_filename)

    # print("# Ordering charts alphabetically")
    # charts_source.sort(key=lambda x: x["repository"]["name"] + " " + get_chart_name( x["url"] ) )

    print("# Iterating charts")
    now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    count = {
        "total":0,
        "privileged":0,
        "baseline":0,
        "restricted":0,
        "error_download":0,
        "error_template":0,
    }
    i=0
    calpha = {}
    for l in ascii_lowercase:
        calpha[l]=0

    brbuckets = {}
    br_min_buckets = -700
    br_size_buckets = -50
    brmin = br_non_evaluable = br_no_workload = 0
    for i in range(0, br_min_buckets, br_size_buckets):
        brbuckets[str(i)] = 0

    print("# Counting")
    date = ""
    keys_pss = charts_pss.keys()    
    for key in keys_pss:
        dic_chart = charts_pss[key]
        level = "unknown"
        i += 1
        calpha[dic_chart["repository"]["name"][0]] += 1
        if "tools" not in dic_chart:
            continue
        if "pss" in dic_chart["tools"]:
            if dic_chart["tools"]["pss"]["date"] > date:
                date = dic_chart["tools"]["pss"]["date"]
            level = dic_chart["tools"]["pss"]["level"]
        if "badrobot" in dic_chart["tools"]:
            score = dic_chart["tools"]["badrobot"]["score"]
            if score == "":
                br_non_evaluable += 1
            elif dic_chart["tools"]["pss"]["level"] in ["empty_no_object", "no_pod_object_but_crd", "no_pod_object"]:
                # TODO: decouple from PSS evaluation
                br_no_workload += 1
            else:
                score = int(score)
                if score < brmin: brmin = int(score)
                for i in range(0, br_min_buckets + br_size_buckets, br_size_buckets):
                    if i >= score and score > ( i + br_size_buckets ):
                        brbuckets[str(i)] += 1
                        break

        count["total"] +=1
        if level not in count:
            count[level] = 1
        else:
            count[level] += 1
        # print( "# ["+ str(i) + "/" + str(len(charts_pss))+ "] " + dic_chart["repository"]["name"] + level)

    header = "[Go to root documentation](https://vicenteherrera.com/secobs-charts)  \n"
    header += "[Go to index of charts evaluation](https://vicenteherrera.com/secobs-charts/docs/generated/charts_levels.md)\n\n"
    header += "## Artifact Hub's Helm charts evaluation\n\n"
    date = "Evaluation date: " + date + "\n"
    list_md = open(doc_filename_prefix+".md", "w")
    list_md.write(header + "Source: [Artifact Hub](https://artifacthub.io/)  \n" + date + "\n### Pod Security Standards (PSS)\n\n")
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
    list_md.write("| No workload | " + str(br_no_workload) + " |\n")

    keys = brbuckets.keys()
    for key in keys:
        list_md.write("| [" + str(key) + ", " + str(int(key) + br_size_buckets) + ") | " + str(brbuckets[key]) + " |\n")


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
    keys_pss = charts_pss.keys()    
    for key in keys_pss:
        dic_chart = charts_pss[key]
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
            list_md.write(header + date + "\n" + index)
            list_md.write("\n\n| repo | chart | PSS level | BadRobot score | chart version | app version |\n")
            list_md.write("|------|------|------|------|------|------|\n")

        level = ""
        brscore = ""
        if "pss" in dic_chart:
            level = dic_chart["tools"]["pss"]["level"]
            if "badrobot" in dic_chart:
                brscore = dic_chart["tools"]["badrobot"]["score"]
        # print( "# ["+ str(i) + "/" + str(len(keys_pss))+ "] " + repo + " " + chart + " " + level)
        list_md.write("| [" + repo + "](" + url + ") | " + chart + " | " + level  + " | " + brscore  + " | " + version + " | " + app_version  + " |\n")
        # sys.exit()


    list_md.close()
