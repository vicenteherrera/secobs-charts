import os
import sys

import charts_eval.config as config
import charts_eval.evaluation.tools as tools
import charts_eval.evaluation.templates as templates
import charts_eval.evaluation.utils as utils

# -----------------------------------------------------------------------

def generate_templates():
    print( "# Reading charts list files" )
    print( "  1. reading AH source file " )
    charts_db_source = utils.load_yaml( config.charts_source_filename )
    if os.path.exists( config.charts_db_filename ):
        print( "  2. reading existing charts PSS" )
        charts_db = utils.load_yaml( config.charts_db_filename )
    else:
        print( "  2. charts DB not found, creating new one" )
        charts_db = {}

    print( "# Downloading charts and generating templates" )
    templates.generate( charts_db_source, charts_db )
    utils.save_yaml( config.charts_db_filename, charts_db )

def evaluate_tools():
    print( "# Reading charts db" )
    if not os.path.exists( config.charts_db_filename ):
        print("**Error, charts db filename not found: %s" % config.charts_db_filename )
    charts_db = utils.load_yaml( config.charts_db_filename )

    print( "# Evaluating charts with tools" )
    tools.evaluate( charts_db )
    utils.save_yaml( config.charts_db_filename, charts_db )
