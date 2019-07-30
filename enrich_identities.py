"""
This script was created in order to better identify people
based on the various emails they use to write git commits,
which may differ from the email they use 
"""

import github3
import yaml
import os

def add_email(username, git_commit):
    git_author_email = git_commit.commit.author['email']#see if you can get email from commit instead of git commit
    contributor = people[username]
    if contributor['email'] != git_author_email: #if the email is not the same
        if 'other_emails' in contributor and git_author_email not in contributor['other_emails']:#check to see if it is in other emails
            contributor['other_emails'].append(git_author_email)
        elif 'other_emails' not in contributor: #or create the key other_emails and add it there
            contributor['other_emails'] = [git_author_email]

def write_file(data):
    with open('result.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

people = {}

#first load the people.yaml file
with open('people.yaml', 'r') as stream:
    try:
        people = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

gh = github3.login('alangsto', token=os.environ['GITHUB_KEY'])
repos = gh.organization('edX').repositories()
emails = []
for repo in repos:
    if not repo.fork: #only look at repositories that are not forks
            commits = repo.commits()
            for git_commit in commits: #commit is a short commit, git_commit is a repository commit
                try:
                    try: #if the username is still active
                        username = git_commit.author.login
                        add_email(username, git_commit)

                    except AttributeError as exc: 
                        #then we want to look at name, and see if we can assign an email to an existing name
                        for name in people:
                            person = people[name]
                            if person['name'] == git_commit.commit.author['name']:
                                add_email(name, git_commit)
                    except KeyError:
                        #happens for usernames that aren't included in our people.yaml file
                        print('Key Error: ' + git_commit.author.login + ", " + git_commit.commit.author['name'])

                except github3.exceptions.ForbiddenError as exc:
                    #if we hit a rate limit, still want to write to the file
                    write_file(people)
                    print(exc)
                    break


#create new yaml file with same format
write_file(people)
