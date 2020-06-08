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
Describes the functions of the script

""".format(script_name=os.path.basename(sys.argv[0])))

def cmd_info():
    print("Showing MySQL ports, Deployed environment and Container name...")
    print("\n| MySQL Port |      Container     |     Environment Name   ")
    print("--"*30)
    running_containers = ranqxlib.subp_capture("docker container ls --format {{.Names}}")
    db_containers = [container for container in running_containers if "mysql" in container]
    db_container_inspect = ranqxlib.subp_capture("docker inspect " + " ".join(db_containers), splitlines=False)
    for db_container_json in json.loads(db_container_inspect):
        print("| {:10} |  {:16.16}  | {}".format(
            db_container_json['Config']['Labels']['com.example.port'],
            db_container_json['Name'][1:],
            db_container_json['Config']['Labels']['com.example.envname'],
            ))
 
    # Example of format with 2 parameters    
    print("Branch {} File ID located at {} ".format(branch.name, str(branch.id_file)))
            
################################################################################
# Execution

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
