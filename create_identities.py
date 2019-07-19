import yaml
from datetime import datetime, timedelta

def get_organization(info):
    if info['agreement'] == 'individual':
        return 'individual'
    elif info['agreement'] == 'institution':
        return info['institution']

with open('people.yaml', 'r') as stream:
    try:
        old_yaml = yaml.safe_load(stream)
        data = []
        for key in old_yaml: #for each entry in the old yaml file
            entry = {
                        'profile': {'name': ''}, 
                        'enrollments': [],
                        'email': [],
                        'github': []
                    }

            #PROFILE/NAME
            entry['profile']['name'] = old_yaml[key]['name']

            #INSTITUTIONS
            if 'before' in old_yaml[key]: #if there is more than one institution listed
                start_date = ''
                dates = sorted(old_yaml[key]['before'])

                for i,end_date in enumerate(dates): # for each of those dates

                    to_process = old_yaml[key]['before'][end_date] #get the information contained by each
                                                                    #date entry

                    if i == 0 and to_process['agreement'] != 'none': # if it is the first date and the agreement is not none
                        entry['enrollments'].append({'organization': get_organization(to_process), # add it to the new yaml file
                                                     'end': end_date})
                    elif to_process['agreement'] != 'none': # if it is a middle date and the agreement is not none
                        entry['enrollments'].append({'organization': get_organization(to_process), # add this to the new yaml file
                                                     'start': start_date,
                                                     'end': end_date})

                    start_date = end_date + timedelta(days=1) #update the start date

                if old_yaml[key]['agreement'] != 'none': #if the current agreement is not none
                    entry['enrollments'].append({'organization': get_organization(old_yaml[key]), 
                                                 'start': start_date})

            else: #if there is only one institution listed
                entry['enrollments'].append({'organization': get_organization(old_yaml[key])})

            #EMAILS
            entry['email'].append(old_yaml[key]['email'])
            if 'other_emails' in old_yaml[key]: #in case there are other emails
                for email in old_yaml[key]['other_emails']:
                    entry['email'].append(email)
  
            #GITHUB
            entry['github'].append(key)

            data.append(entry) # add the new entry to the new yaml file
        
        with open('identities.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
            
    except yaml.YAMLError as exc:
        print(exc)

