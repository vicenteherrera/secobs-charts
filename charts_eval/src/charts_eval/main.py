
import sys
import sys

from charts_eval.evaluation.evaluate import evaluate_tools, generate_templates
from charts_eval.postprocess.generate_docs import generate_docs

def help():
    print("**Error, expected one parameter for a command")
    print("evaluate: iterate all charts and perform tool evaluation")
    print("postprocess: prepare postprocess data and generated documentation")

def cli(args=None):
    """Process command line arguments."""
    if not args:
        args = sys.argv[1:]    

    if len(args)!=1:
        help()
        sys.exit(1)

    command = args[0]

    if (command == 'generate'):
        generate_templates()
    elif (command == 'evaluate'):
        evaluate_tools()
    elif (command == 'postprocess'):
        generate_docs()
    else:
        print("Command not recognized: %s" % command)
        sys.exit(1)

if __name__ == "__main__":
    cli()