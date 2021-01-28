"""
Used to create a projects.json file based on a json file that specifies only an org name (see
more in get_projects.py) and then call sirmordred.
"""
import json
import get_projects
import os
import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--readfile", dest="readfile", default="og_projects.json", help="Path of projects file to read from")
parser.add_argument("-wr", "--writefile", dest="writefile", default="projects.json", help="Path of projects file to write to")
parser.add_argument("-cf", "--credentials", dest="config", default="credentials.cfg", help="Path of credentials file")

args = parser.parse_args()

def initialize(writefile):
    '''
    Deletes projects.json file if it already exists
    '''
    if os.path.exists(writefile):
        os.remove(writefile)
    else:
        raise ValueError("%s does not exist" % args.writefile)

def read_og_projects(filepath):
    '''
    Reads the original projects file that contains the organization name.
    Returns a dictionary that represents the original projects file.
    '''
    if os.path.exists(filepath):
        projects = {}
        with open(filepath) as json_file:
            projects = json.load(json_file)
        return projects
    else:
        raise ValueError("%s does not exist" % args.readfile)

def get_config(filename):
    '''
    Reads the configuration file that contains the github and slack api token.
    Returns a dictionary that represents the config file.
    '''
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config
    else:
        raise ValueError("%s does not exist" % args.config)

def write_projects(projects):
    '''
    Writes new projects to the specified file.
    '''
    with open(args.writefile, 'w+') as outfile:
        json.dump(projects, outfile)

if __name__ == '__main__':
    initialize(args.writefile)
    projects = read_og_projects(args.readfile)
    config = get_config(args.config)
    new_projects = get_projects.create_projects(projects, config)
    write_projects(new_projects)
