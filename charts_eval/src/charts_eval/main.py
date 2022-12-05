
import sys
import sys

from charts_eval.evaluation.evaluate import evaluate_tools, generate_templates
from charts_eval.postprocess.docs import generate_docs
from charts_eval.postprocess.data import generate_data

def help():
    print("**Error, expected one parameter for a command")
    print("evaluate: iterate all charts and perform tool evaluation")
    print("postprocess: prepare postprocess data and generated documentation")

def cli(args=None):
    """Process command line arguments."""
    if not args:
        args = sys.argv[1:]    

    if len(args)<1:
        help()
        sys.exit(1)

    command = args[0]
    param=""
    if len(args)>1:
        param = args[1]

    if (command == 'generate'):
        generate_templates()
    elif (command == 'evaluate'):
        evaluate_tools(param)
    elif (command == 'postprocess'):
        generate_data()
        generate_docs()
        
    else:
        print("Command not recognized: %s" % command)
        sys.exit(1)

if __name__ == "__main__":
    cli()