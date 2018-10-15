# coding=utf-8
import argparse
import json
import subprocess
import sys


# SSH into a remote server and find war files under certain directories
# Returns a list of absolute paths and/or file names depending on the location
# of files
def get_file_paths(instance):
    path = f"*/{instance}/*/current/dist/*.war"
    command = [
        'ssh', '-l', xe_user, xe_host, 'find', banner_home,
        '-type l -wholename', path, '-exec readlink {} \;'
    ]
    ssh = subprocess.Popen(
        command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf8'
    )
    result = ssh.stdout.readlines()
    # If we didn't get any files, something's wrong
    if not result:
        error = ssh.stderr.readlines()
        sys.exit(f"ERROR: {error}")

    return result


# Parse the whole filename into the application name and version.
def parse_file_names(instance):
    file_paths = get_file_paths(instance)

    # Strip absolute path so only the file name remains
    file_names = list(map(lambda x: x.split("/")[-1], file_paths))

    for file in file_names:
        name_parts = file.split("-")
        app = name_parts[0]
        version = name_parts[1].split(".war")[0]

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
