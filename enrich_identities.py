"""
This script was created in order to better identify people
based on the various emails they use to write git commits,
which may differ from the email they use 
"""

from github import Github
import yaml
import os

with open('people.yaml', 'r') as stream:
    try:
        people = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

gh = Github(os.environ['GITHUB_KEY'])
repos = gh.get_organization('edX').get_repos('public')
for repo in repos:
    try:
        commits = repo.get_commits()
        for commit in commits:

            try: #if the username is still active
                username = commit.author.login
                git_author_email = commit.commit.author.email
                contributor = people[username]
                if contributor['email'] != git_author_email:
                    if 'other_emails' in contributor and git_author_email not in contributor['other_emails']:
                        print(git_author_email)
                        contributor['other_emails'].append(git_author_email)
                    if 'other_emails' not in contributor:
                        print(git_author_email)
                        contributor.update({'other_emails': [git_author_email]})

            except: #inactive username, can't parse data
                i = 0

    except:
        print('Empty repository\n')

with open('result.yaml', 'w') as outfile:
        yaml.dump(people, outfile, default_flow_style=False)