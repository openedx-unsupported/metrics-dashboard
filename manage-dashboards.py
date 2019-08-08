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
    dashboards = search_dashboards(os.environ['ELASTIC_URL'], '.kibana')

    for dash in dashboards:
        id = dash['_id'].split(':')[1] #get dashboard id
        json_name = dash['title'].replace(' ', '-') + "-dashboard.json" #create filename for dashboard
        file_path = 'dashboards/' + json_name
        if re.match(r'[-\w_]+\.json',json_name): #check to make sure file being removed has a valid name
            print('updating existing dashboard: ' + file_path)
            try:
                os.remove(file_path)
            except (FileNotFoundError):
                print('saving new dashboard: ' + file_path)
        else:
            raise Exception('Not a valid file path: ' + file_path)
        export_dashboard( #export using kidash API
            os.environ['ELASTIC_URL'], #elastic_url
            id, #dashboard id
            file_path, #export_file
            '.kibana',
            False
        )
    print('Exported all dashboards successfully')

def import_dash():
    '''
    imports all dashboards stored in the dashboards directory to the kibana index. 
    '''
    for file in os.listdir('dashboards'):
        if file.endswith((".json")):
            print('Importing dashboard: ' + file)
            import_dashboard(
                os.environ['ELASTIC_URL'],
                os.environ['KIBANA_URL'],
                ('dashboards/%s' % file)
            )
            

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
