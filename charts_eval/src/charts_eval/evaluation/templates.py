import os
from datetime import datetime
from urllib import parse

from charts_eval.evaluation.chart import Chart
import charts_eval.config as config
import charts_eval.evaluation.utils as utils

def get_logs_prefix( chart: Chart ) -> str:
    return config.logs_dir + "/" + \
        parse.quote(chart.repo + "_" + chart.name + "_" + chart.version)

def _log_helm( chart: Chart ) -> str:
    return get_logs_prefix(chart) + "_helm.log"

def _download_template( chart: Chart ) -> bool:
    """Returns True on error"""
    print("  Downloading chart")
    url = chart.url
    log_helm = _log_helm(chart)

    # TODO: Check if add / update is neccessary, .e.g.:
    # helm search repo prometheus-community/prometheus-to-sd -o yaml | yq .[0].version

    # TODO: Avoid regenerating if helm log exists
    os.system( "echo '# helm repo add " + chart.repo + " " + url + "' 1>" + log_helm + " 2>&1")
    os.system( "helm repo add " + chart.repo + " " + url + " 1>>" + log_helm + " 2>&1")

    os.system( "echo '# helm repo update " + chart.repo + "' 1>>" + log_helm + " 2>&1")
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
    if utils.is_file_empty(template):
        # TODO: retry previously errored templates
        print("  Generating template")
        command = "helm template " + \
            '"' + parse.quote_plus(chart.repo) + "/" + parse.quote_plus(chart.name) + '"' + \
            " --version " + chart.version + ' >"' + template + '" 2>>' + log_helm
        gen_template = os.system(command)
    else:
        print("  Template cached")
        return False
    # template_data = Path(template).read_text()
    if gen_template > 0 or \
        utils.is_in_file("Use --debug flag to render out invalid YAML", log_helm) or \
        utils.is_in_file("Error: failed to download", log_helm):
        if os.path.exists(template): os.remove(template)
        return True
    return False

def generate( charts_db_source: dict, charts_db: dict, retry_errors: bool ):
    """Generate template files on cache dir and store status on charts db"""
    start = datetime.now()
    now = start.strftime("%Y-%m-%d, %H:%M:%S")
    # TODO: delete old log and templates to save disk space
    i = new = nerror = nexist = 0
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
        # and if we have extra removed keys
        if chart.key in found:
            duplicated.append(chart.key)
        found.append(chart.key)

        # If chart data exists we copy previous status and tools evaluation
        if chart.key in charts_db:
            chart_prev = Chart( charts_db[chart.key] )
            chart.tools = chart_prev.tools
            chart.status = chart_prev.status

        # Generate template
        template = _template_filename(chart)
        error = False
        if retry_errors == False:
            if chart.is_error():
                print("  **Error on previous chart evaluation")
                nerror +=1
                continue
        else:
            if not chart.is_error():
                print("  Skipping chart not in error")
                continue
        
        # TODO: or log_helm is error
        if utils.is_file_empty( _log_helm(chart) ) or retry_errors == True:
            error = _download_template(chart)

        if error:
            print("**Error downloading chart")
            status = "error_download"
            template = ""   
            nerror += 1  
        else:
            if not utils.is_file_empty( template ):
                nexist += 1
            else:
                error = _generate_template(chart)
                if ( error ):
                    print("**Error generating template")
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
    print("# New charts and template generation results")
    print("%s charts removed from db" % j)
    # TODO: store duplicated charts with different keys
    print("%s duplicated charts: %s" % (len(duplicated),duplicated))
    print("%s charts error downloading or generating" % nerror)
    print("%s charts templates generated" % new )
    print("%s charts previously generated" % nexist )
    print("%s total charts processed in %s" % (i, ( datetime.now() - start ) ))
