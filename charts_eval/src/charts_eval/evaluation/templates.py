import os
from datetime import datetime
from urllib import parse

from charts_eval.evaluation.chart import Chart
import charts_eval.config as config
import charts_eval.evaluation.utils as utils

def get_logs_prefix( chart: Chart ) -> str:
    # TODO: Make sure there is no collision with slugify names
    return config.logs_dir + "/" + \
        parse.quote(chart.repo + "_" + chart.name + "_" + chart.version)

def _log_helm( chart: Chart ) -> str:
    return get_logs_prefix(chart) + "_helm.log"

def _download_template( chart: Chart ) -> bool:
    """Returns True on error"""
    print("  Downloading chart")
    url = parse.quote_plus(chart.url)
    log_helm = _log_helm(chart)
    os.system( "helm repo add " + chart.repo + " " + url + " 1>" + log_helm + " 2>&1")
    # TODO: Check if update is neccessary, .e.g.:
    # helm search repo prometheus-community/prometheus-to-sd -o yaml | yq .[0].version
    repo_update = os.system( \
        "helm repo update " + chart.repo + " 1>>" + log_helm + " 2>&1")
    if repo_update >0 or utils.is_in_file("cannot be reached", log_helm):
        return True
    return False

def _template_filename(chart: Chart):
    return get_logs_prefix(chart) + "_template.yaml"

def _generate_template( chart: Chart ) -> bool:
    """Returns True on error"""
    template = _template_filename(chart)
    log_helm = _log_helm(chart)
    gen_template = 0
    if not os.path.exists(template):
        # TODO: retry previously errored templates
        print("  Generating template")
        command = "helm template " + \
            '"' + parse.quote_plus(chart.repo) + "/" + parse.quote_plus(chart.name) + '"' + \
            " --version " + chart.version + " >" + template + " 2>>" + log_helm
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
    start = datetime.now()
    now = start.strftime("%Y-%m-%d, %H:%M:%S")
    # TODO: delete old log and templates to save disk space
    # TODO: Remove evaluated charts that no longer appear in Artifact Hub
    i = new = nerror = 0
    found=[]
    duplicated=[]
    for dic_chart in charts_db_source:
        chart = Chart(dic_chart)
        template=""
        status="generated"
        i+=1
        print("# [%s/%s] %s / %s %s" % \
            (i, len(charts_db_source), chart.repo, chart.name, chart.version))
        
        # Store source chart keys to check duplicates
        # and if we have extra keys later
        if chart.key in found:
            duplicated.append(chart.key)
        found.append(chart.key)

        # If chart data exists we copy previous tools evaluation
        if chart.key in charts_db:
            chart_prev = Chart( charts_db[chart.key] )
            chart.tools = chart_prev.tools

        # Generate template
        template = _template_filename(chart)
        error = False
        if not os.path.exists( _log_helm(chart) ):
            error = _download_template(chart)
        if error:
            print("  **Error downloading chart")
            status = "error_download"
            template = ""   
            nerror += 1  
        else:
            error = _generate_template(chart)
            if ( error ):
                print("  **Error generating template")
                status = "error_template"
                template = ""
                nerror += 1
            else:
                new += 1

        # Store chart data
        chart.status = {
            "cache" : status,
            "template_filename": template,
            "chart_version" : chart.version,
            "datetime" : now,
        }
        charts_db[chart.key] = chart.get_dict()

    # Existing charts not found in source gets flagged as removed
    keys=charts_db.keys()
    j=0
    for key in keys:
        if key not in found:
            charts_db[key]["status"]["cache"]="removed"
            j += 1
    print("%s charts removed from db" % j)
    print("%s duplicated charts: %s" % (len(duplicated),duplicated))
    print("%s charts error downloading or generating" % nerror)
    print("Generated %s of %s total charts templates in %s" % \
        ( new , i, str( datetime.now() - start ) ))
