import yaml
from datetime import datetime, timedelta

def get_organization(info):
    if info['agreement'] == 'individual':
        return 'individual'
    else:
        if 'institution' in info:
            return info['institution']
        else:
            return 'unexpected'

with open('people.yaml', 'r') as stream:
    try:
        old_yaml = yaml.safe_load(stream)
        data = []
        #for each entry in the old yaml file
        for key in old_yaml:
            entry = {
                'profile': {'name': ''},
                'enrollments': [],
                'email': [],
                'github': []
            }

            #PROFILE/NAME
            entry['profile']['name'] = old_yaml[key]['name']

            #INSTITUTIONS
            #if there is more than one institution listed
            if 'before' in old_yaml[key]:
                start_date = ''
                dates = sorted(old_yaml[key]['before'])

                # for each of those dates
                for i,end_date in enumerate(dates):

                    #get the information contained by each date entry
                    to_process = old_yaml[key]['before'][end_date]

                    # if it is the first date and the agreement is not none
                    if i == 0 and 'agreement' in to_process and to_process['agreement'] != 'none':
                        # add it to the new yaml file
                        entry['enrollments'].append({'organization': get_organization(to_process),
                                                     'end': end_date})
                    # if it is a middle date and the agreement is not none
                    elif 'agreement' in to_process and to_process['agreement'] != 'none':
                        # add this to the new yaml file
                        entry['enrollments'].append({'organization': get_organization(to_process),
                                                     'start': start_date,
                                                     'end': end_date})

                    #update the start date
                    start_date = end_date + timedelta(days=1)

                #if the current agreement is not none
                if old_yaml[key]['agreement'] != 'none':
                    entry['enrollments'].append({'organization': get_organization(old_yaml[key]),
                                                 'start': start_date})

            #if there is only one institution listed
            else:
                if old_yaml[key]['agreement'] != 'none':
                    entry['enrollments'].append({'organization': get_organization(old_yaml[key])})

            #EMAILS
            entry['email'].append(old_yaml[key]['email'])
            #in case there are other emails
            if 'other_emails' in old_yaml[key]:
                for email in old_yaml[key]['other_emails']:
                    entry['email'].append(email)

            #GITHUB
            entry['github'].append(key)

            # add the new entry to the new yaml file
            data.append(entry)

        with open('identities.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    except yaml.YAMLError as exc:
        print(exc)
