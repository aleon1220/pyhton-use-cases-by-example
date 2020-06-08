import base64
import os
import shutil
import time
import pathlib
import re
import sys
import traceback
import json

def usage():
    print(
"""
Manage Company docker-compose software in a multi-branch-style environment.
Works like a charm with Bitbucket git branches

    {script_name} <command> [<branch>]

<branch> must follow the format "feature/BRANCH-nnn<text>", or just BRANCH-XXX for
delete and restart.

Commands:
  * info - get port, container name and env name of running stacks

This script must be executed on a machine configured for multi-branch
deployment.

Requirements:
  * Read-only access to the Bitbucket account
  * An Nginx server
  * A *.test.company.io wildcard certificate
  * boto3 installed

""".format(script_name=os.path.basename(sys.argv[0])))


################################################################################
# Shared functionality

def cmd_info():
    print("Showing MySQL ports, Deployed environment and Container name...")
    print("\n| MySQL Port |      Container     |     Environment Name   ")
    print("--"*30)
    running_containers = ranqxlib.subp_capture("docker container ls --format {{.Names}}")
    db_containers = [container for container in running_containers if "mysql" in container]
    db_container_inspect = ranqxlib.subp_capture("docker inspect " + " ".join(db_containers), splitlines=False)
    for db_container_json in json.loads(db_container_inspect):
        print("| {:10} |  {:16.16}  | {}".format(
            db_container_json['Config']['Labels']['com.ranqx.loan.port'],
            db_container_json['Name'][1:],
            db_container_json['Config']['Labels']['com.ranqx.loan.envname'],
            ))
    # Example of format with 2 parameters    
    print("Branch {} File ID located at {} ".format(branch.name, str(branch.id_file)))
            
################################################################################
# Main Execution

try:
    aws_account = ranqxlib.get_aws_account()
    if aws_account['name'] not in ("dev", "unknown"):
        raise Exception("Multi deploys must happen in dev")

    # Check command line arguments
    if len(sys.argv) <= 1:
        usage()
        sys.exit(0)

    # Execute the command specified if it exists
    command_name = "cmd_" + sys.argv[1]
    if command_name in dir():
        exec(command_name + "()")
    else:
        print("***Info:\n The command given is not part of the deploy-multi functionality.\n")
        raise Exception("Unknown command")

except Exception as e:
    print("***Error:")
    traceback.print_exc()
    sys.exit(1) 
