# coding=utf-8
import argparse
import json
import subprocess
import sys


# SSH into a remote server and find war files under certain directories
def get_file_names(instance):
    path = f"*/{instance}/*/current/dist/*.war"
    command = [
        'ssh', '-l', xe_user, xe_host, 'find', banner_home,
        '-type l -wholename', path, '-exec readlink {} \;'
    ]
    ssh = subprocess.Popen(
        command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    result = ssh.stdout.readlines()
    # If we didn't get any files, something's wrong
    if not result:
        error = ssh.stderr.readlines()
        sys.exit(f"ERROR: {error}")

    return result


# Parse the whole filename into the application name and version.
def parse_file_names(instance):
    file_names = get_file_names(instance)

    for file in file_names:
        app = file.split('-', 1)[0]
        version = file.split('-', 1)[-1]
        version = version.split('.war', 1)[0]

        version_dict = {"instance": instance, "version": version}

        if app in xe_apps:
            xe_apps[app]['versions'].append(version_dict)
        else:
            xe_apps[app] = {"applicationName": app, "versions": [version_dict]}


# Call above methods to get a dict containing all the apps, then write to a
# json file
def write_apps_to_file():

    # For each deployed environment, do a search for war files in the
    # respective directories
    for instance in environments:
        parse_file_names(instance)

    # Create json file, overwrite if it exists.
    with open('xe_apps.json', 'w') as xe_app_file:
        json.dump(xe_apps, xe_app_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="path to input file", dest="input_file")
    namespace = parser.parse_args()
    config_json = json.load(open(namespace.input_file))

    xe_user = config_json["xe_user"]
    xe_host = config_json["xe_host"]
    banner_home = config_json["banner_home"]
    environments = config_json["environments"]

    xe_apps = {}

    write_apps_to_file()
