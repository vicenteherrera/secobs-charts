
import os
import charts_eval.evaluation.tools as tools
import charts_eval.config as config
import charts_eval.evaluation.tools as tools
import charts_eval.evaluation.templates as templates
import charts_eval.evaluation.utils as utils
from charts_eval.evaluation.chart import Chart

def _anonymize_data(charts_db: dict) -> dict:
    new_db = []
    keys = charts_db.keys()

    for key in keys:
        chart_new={}
        chart_src=charts_db[key]
        if "status" in chart_src and "cache" in chart_src["status"]:   
            chart_new["status"]={ "cache": chart_src["status"]["cache"] }

        if "tools" in chart_src:
            chart_new["tools"] = {}
            for tool in tools.tools_list:
                if tool in chart_src["tools"]:
                    chart_new["tools"][tool] = chart_src["tools"][tool]
                    chart_new["tools"][tool].pop("chart_version",'')

        new_db.append(chart_new)
    
    return new_db

def _error_db(charts_db: dict) -> dict:
    new_db = {}
    keys = charts_db.keys()

    for key in keys:
        chart = Chart(charts_db[key])

        if chart.is_error():
            new_db[key] = chart.get_dict()
    return new_db

def generate_data():
    print( "# Reading charts db" )
    if utils.is_file_empty( config.charts_db_filename ):
        print("**Error, charts db filename not found or empty: %s" % config.charts_db_filename )
    charts_db = utils.load_yaml( config.charts_db_filename )
    print( "# Generating db with anonymous data" )
    utils.save_yaml( config.charts_db_anon_filename, _anonymize_data( charts_db ) )
    print("# Generating db only with charts in error")
    utils.save_yaml( config.charts_db_errors_filename, _error_db(charts_db) )

