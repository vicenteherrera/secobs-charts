import os
import sys

import charts_eval.config as config
import charts_eval.evaluation.tools as tools
import charts_eval.evaluation.templates as templates
import charts_eval.evaluation.utils as utils

# -----------------------------------------------------------------------

def generate_templates(param: str):
    retry_errors = False
    if param == "--retry-errors": retry_errors = True

    print( "# Reading charts data files" )
    print( "  1. reading AH source file " )
    charts_db_source = utils.load_yaml( config.charts_source_filename )
    if not utils.is_file_empty( config.charts_db_filename ):
        print( "  2. reading charts db" )
        charts_db = utils.load_yaml( config.charts_db_filename )
    else:
        print( "  2. charts db not found, creating new one" )
        charts_db = {}
    print( "# Downloading charts and generating templates" )
    templates.generate( charts_db_source, charts_db, retry_errors )
    print( "# Saving charts db" )
    utils.save_yaml( config.charts_db_filename, charts_db )

def evaluate_tools(param: str):
    force=False
    if param=="--force": force=True
    print( "# Reading charts db" )
    if utils.is_file_empty( config.charts_db_filename ):
        print("**Error, charts db filename not found or empty: %s" % config.charts_db_filename )
    charts_db = utils.load_yaml( config.charts_db_filename )
    print( "# Evaluating charts with tools" )
    tools.evaluate( charts_db, force )
    print( "# Saving charts db" )
    utils.save_yaml( config.charts_db_filename, charts_db )
