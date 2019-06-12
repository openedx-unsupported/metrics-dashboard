# -*- coding: utf-8 -*-

"""
provides methods to automatically export and import all dashboards for the Open edX metrics dashboard
"""

from kidash.kidash import import_dashboard, export_dashboard, search_dashboards
import os
import sys
import re

def export_dash():
    '''
    exports all dashboards stored in the kibana index to the dashboards directory. 
    Filenames will be configured based on dashboard titles.
    '''
    try:
        dashboards = search_dashboards('http://localhost:9200', '.kibana')

        for dash in dashboards:
            id = dash['_id'].split(':')[1] #get dashboard id
            json_name = dash['title'].replace(' ', '-') + "-dashboard.json" #create filename for dashboard
            file_path = 'dashboards/' + json_name
            if re.match(r'[-\w_]+\.json',json_name): #check to make sure file being removed has a valid name
                print('valid file')
                os.remove(file_path)
            else:
                raise Exception('Not a file path')
            export_dashboard( #export using kidash API
                'http://localhost:9200', #elastic_url
                id, #dashboard id
                file_path, #export_file
                '.kibana',
                False
                )
        print('Exported all dashboards successfully')
    except (KeyError):
        raise Exception('Could not export')

def import_dash():
    '''
    imports all dashboards stored in the dashboards directory to the kibana index. 
    '''
    try:
        for file in os.listdir('dashboards'):
            if file.endswith((".json")):
                    import_dashboard(
                        'http://127.0.0.1:9200', #elastic_url
                        'http://localhost:5601', #kibana_url
                        ('dashboards/%s' % file) #import_file
                        )
    except (KeyError):
        raise Exception('Could not import')
            

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'import':
            import_dash()
        elif sys.argv[1] == 'export':
            export_dash()
    else:
        if len(sys.argv) == 1:
            print("Please supply which functionality (either export or import) you would like to use.")
        if len(sys.argv) > 2:
            print("Too many arguments supplied. Please only specify if you would like to import or export.")
