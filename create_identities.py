import yaml

with open("people.yaml", 'r') as stream:
    try:
        old_yaml = yaml.safe_load(stream)
        data = []
        for key in old_yaml:
        	entry = {
        				'profile': {'name': ''}, 
        				'enrollments': [{'organization': ''}],
        				'email': [],
        				'github': []
        			}

        	#PROFILE/NAME
        	entry['profile']['name'] = old_yaml[key]['name']

        	#INSTITUTIONS
        	#need to fix in case of more institutions
        	if 'institution' in old_yaml[key]:
        		entry['enrollments'][0]['organization'] = old_yaml[key]['institution']
        	else:
        		entry['enrollments'][0]['organization'] = 'Independent'

        	#EMAILS
        	entry['email'].append(old_yaml[key]['email'])
        	if 'other_emails' in old_yaml[key]: #in case there are other emails
        		for email in old_yaml[key]['other_emails']:
        			entry['email'].append(email)
  
        	#GITHUB
        	entry['github'].append(key)

        	data.append(entry)
        
        with open('identities.yaml', 'w') as outfile:
        	yaml.dump(data, outfile, default_flow_style=False)
        	
    except yaml.YAMLError as exc:
        print(exc)