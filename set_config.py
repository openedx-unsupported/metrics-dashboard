"""
Used to gather the slack and github api tokens from an environment variable,
and then write those to a config file. 
"""

import os
import configparser
import sys

def get_tokens(argv):
        github = argv[1] #os.environ['GITHUB_KEY']
        slack = argv[2] #os.environ['SLACK_KEY']
        db_user = argv[3] #os.environ['DB_USER']
        db_pass = argv[4] #os.environ['DB_PASS']
        db_host = argv[5] #os.environ['DB_HOST']
        db_name = argv[6] #os.environ['DB_NAME']
        elastic_url = argv[7] #os.environ['ELASTIC_URL']
        kibana_url = argv[8] #os.environ['KIBANA_URL']
        discourse = argv[9] #os.environ['DISCOURSE_KEY'] 

        return {
                "github": github, 
                "slack": slack,
                "db_user": db_user,
                "db_pass": db_pass,
                "db_host": db_host,
                "db_name": db_name,
                "elastic_url": elastic_url,
                "kibana_url": kibana_url,
                "discourse": discourse
        }

def write_config(tokens):
	infra_config = configparser.RawConfigParser()

        infra_config.read('infra.cfg')
        infra_config.set('es_collection', 'url', tokens['elastic_url'])
        infra_config.set('es_enrichment', 'url', tokens['elastic_url'])
        infra_config.set('sortinghat', 'user', tokens['db_user'])
        infra_config.set('sortinghat', 'password', tokens['db_pass'])
        infra_config.set('panels', 'kibiter_url', tokens['kibana_url'])
        infra_config.set('sortinghat', 'database', tokens['db_name'])
        infra_config.set('sortinghat', 'host', tokens['db_host'])

        with open('infra.cfg', 'w') as configfile:
                infra_config.write(configfile)

        token_config = configparser.RawConfigParser()

        token_config.add_section('github')
        token_config.set('github', 'api-token', tokens['github'])
        token_config.add_section('slack')
        token_config.set('slack', 'api-token', tokens['slack'])
        token_config.add_section('discourse')
        token_config.set('discourse', 'api-token', tokens['discourse'])

        with open('override.cfg', 'w') as configfile:
                token_config.write(configfile)

if __name__ == '__main__':
        tokens = get_tokens(sys.argv)
        write_config(tokens)
