#!/usr/bin/env python
"""
Gets all of the repos/channels for a grimoirelabs project
"""
import os
import github3
import json
from slackclient import SlackClient


def create_projects(projects, config):
    git_token = config['github']['api-token']
    slack_token = config['slack']['api-token']
    discourse_token = config['discourse']['api-token']

    for key in projects:
        if 'git' in projects[key] and 'http' not in projects[key]['git'][0]:
            git_organization = projects[key]['git'][0]
            git_repos = get_git_repos(git_organization, git_token)
            projects[key]['git'] = git_repos
            projects[key]['github'] = git_repos
            projects[key]['github:repo'] = git_repos
        if 'slack' in projects[key] and projects[key]['slack'] == []:
            projects[key]['slack'] = get_slack_channels(slack_token)
    return projects

def get_git_repos(org, token):
    gh = github3.login(token = token)
    repos = gh.organization('edX').repositories('public')
    repo_list = []
    for repo in repos:
        if not repo.fork:
            repo_list.append(repo.html_url)
    return repo_list

def get_slack_channels(token):
    client = SlackClient(token)
    channels = client.api_call("channels.list", exclude_archived=1)['channels']
    channel_list = []
    for channel in channels:
        channel_list.append(channel['id'])
    return channel_list

if __name__ == '__main__':

    '''
    Test 1: Tests automatically filling the values for the
            project for both a github organization and a slack workspace.

            Passes when length of projects for slack is equivalent to number of
            channels and length of projects for github is equivalent to the
            number of public repos for a github organization.
    '''
    projects1 = {
        "Open edX": {
            "git": [ "edx"],
            "github": [],
            "github:repo": [],
            "slack": [],
            "discourse": []
        }
    }
    config1 = {
        'github' : {'api-token' : os.environ['GITHUB_KEY']}, #use correct tokens here
        'slack' : {'api-token' : os.environ['SLACK_KEY']},
        'discourse' : {'api-token' : os.environ['DISCOURSE_KEY']}
    }

    create_projects(projects1, config1)

    if len(projects1['Open edX']['slack']) == 154 and len(projects1['Open edX']['github']) == 224:
        print('Test 1 Passed: Filling in projects for Git and Slack')
    else:
        print(len(projects1['Open edX']['github']))
        print(len(projects1['Open edX']['slack']))

    '''
    Test 2: Tests automatically filling the values for the
            project for only a slack workspace.

            Passes when length of projects for slack is equivalent to number of
            channels and length of projects for github is equivalent to the
            specified projects.
    '''

    projects2 = {
        "Open edX": {
            "git": [ 'https://github.com/edx/publisher-frontend'],
            "github": ['https://github.com/edx/publisher-frontend'],
            "github:repos": ['https://github.com/edx/publisher-frontend'],
            "slack": []
        }
    }
    create_projects(projects2, config1)
    if len(projects2['Open edX']['slack']) == 154 and len(projects2['Open edX']['github']) == 1:
        print('Test 2 Passed: Filling in projects for only Slack')
    else:
        '''print('Test 2 failed:\n Length of slack:'
                + len(projects1['Open edX']['slack'])
                + '\nLength of github: ' + len(projects2['Open edX']['github']))''' #need to fix this

    '''
    Test 3: Tests that this fills in values for multiple projects within the same
            dictionary.

            Passes if length for each part (i.e. github, slack) of each project is
            correct (i.e. equal to the number of channels, number of public repositories,
            number of specified repos, number of specified channels).
    '''

    projects3 = {
        "Open edX": {
            "git": [ 'https://github.com/edx/publisher-frontend'],
            "github": ['https://github.com/edx/publisher-frontend'],
            "github:repos": ['https://github.com/edx/publisher-frontend'],
            "slack": []
        },
        "Test": {
            "git": ['openedx'],
            "github": [],
            "github:repos": [],
            "slack": ['test']
        }
    }
    create_projects(projects3, config1)
    if (len(projects3['Open edX']['slack']) == 154 and
        len(projects3['Open edX']['github']) == 1 and
        len(projects3['Test']['slack']) == 1 and
        len(projects3['Test']['github']) == 3):
        print('Test 3 Passed: Testing multiple projects')

    '''
    Test 4: Tests with our data
    '''
    projects4 = {"Open edX": {"git": ["https://github.com/edx/cs_comments_service", "https://github.com/edx/xqueue", "https://github.com/edx/django-wiki", "https://github.com/edx/ease", "https://github.com/edx/edx-ora", "https://github.com/edx/loghandlersplus", "https://github.com/edx/XBlock", "https://github.com/edx/djeventstream", "https://github.com/edx/insights", "https://github.com/edx/edxanalytics", "https://github.com/edx/archived-edx.github.io", "https://github.com/edx/configuration", "https://github.com/edx/codejail", "https://github.com/edx/arch-prototype", "https://github.com/edx/skel", "https://github.com/edx/edx-platform", "https://github.com/edx/xserver", "https://github.com/edx/edx-tools", "https://github.com/edx/js-test-tool", "https://github.com/edx/notifier", "https://github.com/edx/event-tracking", "https://github.com/edx/git-client-plugin", "https://github.com/edx/edx-demo-course", "https://github.com/edx/patch-juggler", "https://github.com/edx/repo-tools", "https://github.com/edx/git-plugin", "https://github.com/edx/edx-e2e-tests", "https://github.com/edx/bok-choy", "https://github.com/edx/asgard", "https://github.com/edx/datajam", "https://github.com/edx/datajam-analytics", "https://github.com/edx/edx-ora2", "https://github.com/edx/test-metrics", "https://github.com/edx/acid-block", "https://github.com/edx/xblock-sdk", "https://github.com/edx/edx-certificates", "https://github.com/edx/xqueue-watcher", "https://github.com/edx/dogapi", "https://github.com/edx/alton", "https://github.com/edx/opaque-keys", "https://github.com/edx/edx-analytics-data-api", "https://github.com/edx/i18n-tools", "https://github.com/edx/edx-submissions", "https://github.com/edx/edx-analytics-dashboard", "https://github.com/edx/django-oauth2-provider", "https://github.com/edx/edx-val", "https://github.com/edx/openedx-webhooks", "https://github.com/edx/edx-analytics-configuration", "https://github.com/edx/edx-analytics-data-api-client", "https://github.com/edx/edx-analytics-pipeline", "https://github.com/edx/edx-oauth2-provider", "https://github.com/edx/django-lang-pref-middleware", "https://github.com/edx/edx-documentation", "https://github.com/edx/luigi", "https://github.com/edx/xblock-utils", "https://github.com/edx/edx-fonts", "https://github.com/edx/edx-analytics-api-client", "https://github.com/edx/harprofiler", "https://github.com/edx/MongoDBProxy", "https://github.com/edx/edx-notes-api", "https://github.com/edx/edx-analytics-hadoop-util", "https://github.com/edx/edx-milestones", "https://github.com/edx/edx-django-profiler", "https://github.com/edx/edx-notifications", "https://github.com/edx/edx-app-ios", "https://github.com/edx/edx-app-android", "https://github.com/edx/edx-search", "https://github.com/edx/ux-pattern-library", "https://github.com/edx/pyinstrument", "https://github.com/edx/edx-lint", "https://github.com/edx/ecommerce", "https://github.com/edx/auth-backends", "https://github.com/edx/edx-app-gradle-plugin", "https://github.com/edx/testeng-ci", "https://github.com/edx/edx-reverification-block", "https://github.com/edx/edx-rest-api-client", "https://github.com/edx/thumb-stack", "https://github.com/edx/edx-common-client", "https://github.com/edx/edx-proctoring", "https://github.com/edx/edx-user-state-client", "https://github.com/edx/ecommerce-scripts", "https://github.com/edx/edx-organizations", "https://github.com/edx/ccx-keys", "https://github.com/edx/discussions", "https://github.com/edx/edx-load-tests", "https://github.com/edx/xsy", "https://github.com/edx/edx-ui-toolkit", "https://github.com/edx/openedx-conference-pages", "https://github.com/edx/django-rest-framework-oauth", "https://github.com/edx/cookiecutter-django-ida", "https://github.com/edx/programs", "https://github.com/edx/demo-performance-course", "https://github.com/edx/ecommerce-worker", "https://github.com/edx/django-openid-auth", "https://github.com/edx/django-pyfs", "https://github.com/edx/django-rest-framework", "https://github.com/edx/demo-test-course", "https://github.com/edx/build-pipeline", "https://github.com/edx/edx-custom-a11y-rules", "https://github.com/edx/django-splash", "https://github.com/edx/edx-analytics-exporter", "https://github.com/edx/xblock-lti-consumer", "https://github.com/edx/course-discovery", "https://github.com/edx/credentials", "https://github.com/edx/edx-django-extensions", "https://github.com/edx/edx-grader-support", "https://github.com/edx/tubular", "https://github.com/edx/dummy-webapp", "https://github.com/edx/edx-capa", "https://github.com/edx/edx-django-release-util", "https://github.com/edx/edx-drf-extensions", "https://github.com/edx/edx-django-sites-extensions", "https://github.com/edx/pa11ycrawler", "https://github.com/edx/open-edx-proposals", "https://github.com/edx/edx-icon", "https://github.com/edx/api-manager", "https://github.com/edx/sample-themes", "https://github.com/edx/jenkins-job-dsl", "https://github.com/edx/openedxstats", "https://github.com/edx/gomatic", "https://github.com/edx/edx-safety", "https://github.com/edx/edx-gomatic", "https://github.com/edx/eslint-config-edx", "https://github.com/edx/cookiecutter-django-app", "https://github.com/edx/vagrant-timer", "https://github.com/edx/edx-app-android-white-label-demo", "https://github.com/edx/cookiecutter-xblock", "https://github.com/edx/django-user-tasks", "https://github.com/edx/notifications", "https://github.com/edx/notifications-pipeline-steps", "https://github.com/edx/edx-sphinx-theme", "https://github.com/edx/django-config-models", "https://github.com/edx/edx-enterprise", "https://github.com/edx/web-fragments", "https://github.com/edx/devstack", "https://github.com/edx/pa11ycrawler-ignore", "https://github.com/edx/edx-celeryutils", "https://github.com/edx/edx-salesforce", "https://github.com/edx/credentials-themes", "https://github.com/edx/help-tokens", "https://github.com/edx/paragon", "https://github.com/edx/language-negotiation-lambda", "https://github.com/edx/edx-docker-base", "https://github.com/edx/jenkins-configuration", "https://github.com/edx/py-opt-cli", "https://github.com/edx/supported-components", "https://github.com/edx/bootstrapped", "https://github.com/edx/edx-bootstrap", "https://github.com/edx/edx-video-pipeline", "https://github.com/edx/edx-video-worker", "https://github.com/edx/ConceptXBlock", "https://github.com/edx/AudioXBlock", "https://github.com/edx/RecommenderXBlock", "https://github.com/edx/AnimationXBlock", "https://github.com/edx/RateXBlock", "https://github.com/edx/DoneXBlock", "https://github.com/edx/django-celery", "https://github.com/edx/edx-ace", "https://github.com/edx/studio-frontend", "https://github.com/edx/stylelint-config-edx", "https://github.com/edx/xblock-review", "https://github.com/edx/django-oauth-plus", "https://github.com/edx/edx-enterprise-data", "https://github.com/edx/analytics-python", "https://github.com/edx/edx-app-test", "https://github.com/edx/edx-app-qa", "https://github.com/edx/completion", "https://github.com/edx/openedx-census", "https://github.com/edx/frontend-cookie-cutter-application", "https://github.com/edx/journals", "https://github.com/edx/user-util", "https://github.com/edx/XSS-Linter", "https://github.com/edx/cookie-policy-banner", "https://github.com/edx/xapi-events", "https://github.com/edx/create-edx-react-app", "https://github.com/edx/docs.edx.org", "https://github.com/edx/chunkey", "https://github.com/edx/v_videocompile", "https://github.com/edx/edx-portal", "https://github.com/edx/cookie-cutter-react-component-library", "https://github.com/edx/floor-plan-connector", "https://github.com/edx/journals-frontend", "https://github.com/edx/django-plugins", "https://github.com/edx/edx-toggles", "https://github.com/edx/TinCanPython", "https://github.com/edx/edx-django-utils", "https://github.com/edx/frontend-cookiecutter-library", "https://github.com/edx/vertica_docker", "https://github.com/edx/xss-utils", "https://github.com/edx/frontend-auth", "https://github.com/edx/edx-developer-docs", "https://github.com/edx/gradebook", "https://github.com/edx/mockprock", "https://github.com/edx/code-annotations", "https://github.com/edx/cypress-e2e-tests", "https://github.com/edx/publisher-frontend", "https://github.com/edx/mdrst", "https://github.com/edx/frontend-component-footer", "https://github.com/edx/frontend-component-site-header", "https://github.com/edx/frontend-app-profile", "https://github.com/edx/hermes", "https://github.com/edx/registrar", "https://github.com/edx/asym-crypto-yaml", "https://github.com/edx/edx-rbac", "https://github.com/edx/edx-when", "https://github.com/edx/crowdsourcehinter", "https://github.com/edx/html-webpack-new-relic-plugin", "https://github.com/edx/frontend-app-learner-portal", "https://github.com/edx/frontend-analytics", "https://github.com/edx/frontend-logging", "https://github.com/edx/frontend-app-ecommerce", "https://github.com/edx/openedx-calc", "https://github.com/edx/frontend-app-account", "https://github.com/edx/frontend-common", "https://github.com/edx/edx-zoom", "https://github.com/edx/portal-designer", "https://github.com/edx/frontend-app-payment", "https://github.com/edx/openedx-chem", "https://github.com/edx/frontend-i18n", "https://github.com/edx/staff_graded-xblock", "https://github.com/edx/super-csv", "https://github.com/edx/frontend-app-program-manager", "https://github.com/edx/edx-bulk-grades", "https://github.com/edx/edx4edx_lite"], "github": ["https://github.com/edx/cs_comments_service", "https://github.com/edx/xqueue", "https://github.com/edx/django-wiki", "https://github.com/edx/ease", "https://github.com/edx/edx-ora", "https://github.com/edx/loghandlersplus", "https://github.com/edx/XBlock", "https://github.com/edx/djeventstream", "https://github.com/edx/insights", "https://github.com/edx/edxanalytics", "https://github.com/edx/archived-edx.github.io", "https://github.com/edx/configuration", "https://github.com/edx/codejail", "https://github.com/edx/arch-prototype", "https://github.com/edx/skel", "https://github.com/edx/edx-platform", "https://github.com/edx/xserver", "https://github.com/edx/edx-tools", "https://github.com/edx/js-test-tool", "https://github.com/edx/notifier", "https://github.com/edx/event-tracking", "https://github.com/edx/git-client-plugin", "https://github.com/edx/edx-demo-course", "https://github.com/edx/patch-juggler", "https://github.com/edx/repo-tools", "https://github.com/edx/git-plugin", "https://github.com/edx/edx-e2e-tests", "https://github.com/edx/bok-choy", "https://github.com/edx/asgard", "https://github.com/edx/datajam", "https://github.com/edx/datajam-analytics", "https://github.com/edx/edx-ora2", "https://github.com/edx/test-metrics", "https://github.com/edx/acid-block", "https://github.com/edx/xblock-sdk", "https://github.com/edx/edx-certificates", "https://github.com/edx/xqueue-watcher", "https://github.com/edx/dogapi", "https://github.com/edx/alton", "https://github.com/edx/opaque-keys", "https://github.com/edx/edx-analytics-data-api", "https://github.com/edx/i18n-tools", "https://github.com/edx/edx-submissions", "https://github.com/edx/edx-analytics-dashboard", "https://github.com/edx/django-oauth2-provider", "https://github.com/edx/edx-val", "https://github.com/edx/openedx-webhooks", "https://github.com/edx/edx-analytics-configuration", "https://github.com/edx/edx-analytics-data-api-client", "https://github.com/edx/edx-analytics-pipeline", "https://github.com/edx/edx-oauth2-provider", "https://github.com/edx/django-lang-pref-middleware", "https://github.com/edx/edx-documentation", "https://github.com/edx/luigi", "https://github.com/edx/xblock-utils", "https://github.com/edx/edx-fonts", "https://github.com/edx/edx-analytics-api-client", "https://github.com/edx/harprofiler", "https://github.com/edx/MongoDBProxy", "https://github.com/edx/edx-notes-api", "https://github.com/edx/edx-analytics-hadoop-util", "https://github.com/edx/edx-milestones", "https://github.com/edx/edx-django-profiler", "https://github.com/edx/edx-notifications", "https://github.com/edx/edx-app-ios", "https://github.com/edx/edx-app-android", "https://github.com/edx/edx-search", "https://github.com/edx/ux-pattern-library", "https://github.com/edx/pyinstrument", "https://github.com/edx/edx-lint", "https://github.com/edx/ecommerce", "https://github.com/edx/auth-backends", "https://github.com/edx/edx-app-gradle-plugin", "https://github.com/edx/testeng-ci", "https://github.com/edx/edx-reverification-block", "https://github.com/edx/edx-rest-api-client", "https://github.com/edx/thumb-stack", "https://github.com/edx/edx-common-client", "https://github.com/edx/edx-proctoring", "https://github.com/edx/edx-user-state-client", "https://github.com/edx/ecommerce-scripts", "https://github.com/edx/edx-organizations", "https://github.com/edx/ccx-keys", "https://github.com/edx/discussions", "https://github.com/edx/edx-load-tests", "https://github.com/edx/xsy", "https://github.com/edx/edx-ui-toolkit", "https://github.com/edx/openedx-conference-pages", "https://github.com/edx/django-rest-framework-oauth", "https://github.com/edx/cookiecutter-django-ida", "https://github.com/edx/programs", "https://github.com/edx/demo-performance-course", "https://github.com/edx/ecommerce-worker", "https://github.com/edx/django-openid-auth", "https://github.com/edx/django-pyfs", "https://github.com/edx/django-rest-framework", "https://github.com/edx/demo-test-course", "https://github.com/edx/build-pipeline", "https://github.com/edx/edx-custom-a11y-rules", "https://github.com/edx/django-splash", "https://github.com/edx/edx-analytics-exporter", "https://github.com/edx/xblock-lti-consumer", "https://github.com/edx/course-discovery", "https://github.com/edx/credentials", "https://github.com/edx/edx-django-extensions", "https://github.com/edx/edx-grader-support", "https://github.com/edx/tubular", "https://github.com/edx/dummy-webapp", "https://github.com/edx/edx-capa", "https://github.com/edx/edx-django-release-util", "https://github.com/edx/edx-drf-extensions", "https://github.com/edx/edx-django-sites-extensions", "https://github.com/edx/pa11ycrawler", "https://github.com/edx/open-edx-proposals", "https://github.com/edx/edx-icon", "https://github.com/edx/api-manager", "https://github.com/edx/sample-themes", "https://github.com/edx/jenkins-job-dsl", "https://github.com/edx/openedxstats", "https://github.com/edx/gomatic", "https://github.com/edx/edx-safety", "https://github.com/edx/edx-gomatic", "https://github.com/edx/eslint-config-edx", "https://github.com/edx/cookiecutter-django-app", "https://github.com/edx/vagrant-timer", "https://github.com/edx/edx-app-android-white-label-demo", "https://github.com/edx/cookiecutter-xblock", "https://github.com/edx/django-user-tasks", "https://github.com/edx/notifications", "https://github.com/edx/notifications-pipeline-steps", "https://github.com/edx/edx-sphinx-theme", "https://github.com/edx/django-config-models", "https://github.com/edx/edx-enterprise", "https://github.com/edx/web-fragments", "https://github.com/edx/devstack", "https://github.com/edx/pa11ycrawler-ignore", "https://github.com/edx/edx-celeryutils", "https://github.com/edx/edx-salesforce", "https://github.com/edx/credentials-themes", "https://github.com/edx/help-tokens", "https://github.com/edx/paragon", "https://github.com/edx/language-negotiation-lambda", "https://github.com/edx/edx-docker-base", "https://github.com/edx/jenkins-configuration", "https://github.com/edx/py-opt-cli", "https://github.com/edx/supported-components", "https://github.com/edx/bootstrapped", "https://github.com/edx/edx-bootstrap", "https://github.com/edx/edx-video-pipeline", "https://github.com/edx/edx-video-worker", "https://github.com/edx/ConceptXBlock", "https://github.com/edx/AudioXBlock", "https://github.com/edx/RecommenderXBlock", "https://github.com/edx/AnimationXBlock", "https://github.com/edx/RateXBlock", "https://github.com/edx/DoneXBlock", "https://github.com/edx/django-celery", "https://github.com/edx/edx-ace", "https://github.com/edx/studio-frontend", "https://github.com/edx/stylelint-config-edx", "https://github.com/edx/xblock-review", "https://github.com/edx/django-oauth-plus", "https://github.com/edx/edx-enterprise-data", "https://github.com/edx/analytics-python", "https://github.com/edx/edx-app-test", "https://github.com/edx/edx-app-qa", "https://github.com/edx/completion", "https://github.com/edx/openedx-census", "https://github.com/edx/frontend-cookie-cutter-application", "https://github.com/edx/journals", "https://github.com/edx/user-util", "https://github.com/edx/XSS-Linter", "https://github.com/edx/cookie-policy-banner", "https://github.com/edx/xapi-events", "https://github.com/edx/create-edx-react-app", "https://github.com/edx/docs.edx.org", "https://github.com/edx/chunkey", "https://github.com/edx/v_videocompile", "https://github.com/edx/edx-portal", "https://github.com/edx/cookie-cutter-react-component-library", "https://github.com/edx/floor-plan-connector", "https://github.com/edx/journals-frontend", "https://github.com/edx/django-plugins", "https://github.com/edx/edx-toggles", "https://github.com/edx/TinCanPython", "https://github.com/edx/edx-django-utils", "https://github.com/edx/frontend-cookiecutter-library", "https://github.com/edx/vertica_docker", "https://github.com/edx/xss-utils", "https://github.com/edx/frontend-auth", "https://github.com/edx/edx-developer-docs", "https://github.com/edx/gradebook", "https://github.com/edx/mockprock", "https://github.com/edx/code-annotations", "https://github.com/edx/cypress-e2e-tests", "https://github.com/edx/publisher-frontend", "https://github.com/edx/mdrst", "https://github.com/edx/frontend-component-footer", "https://github.com/edx/frontend-component-site-header", "https://github.com/edx/frontend-app-profile", "https://github.com/edx/hermes", "https://github.com/edx/registrar", "https://github.com/edx/asym-crypto-yaml", "https://github.com/edx/edx-rbac", "https://github.com/edx/edx-when", "https://github.com/edx/crowdsourcehinter", "https://github.com/edx/html-webpack-new-relic-plugin", "https://github.com/edx/frontend-app-learner-portal", "https://github.com/edx/frontend-analytics", "https://github.com/edx/frontend-logging", "https://github.com/edx/frontend-app-ecommerce", "https://github.com/edx/openedx-calc", "https://github.com/edx/frontend-app-account", "https://github.com/edx/frontend-common", "https://github.com/edx/edx-zoom", "https://github.com/edx/portal-designer", "https://github.com/edx/frontend-app-payment", "https://github.com/edx/openedx-chem", "https://github.com/edx/frontend-i18n", "https://github.com/edx/staff_graded-xblock", "https://github.com/edx/super-csv", "https://github.com/edx/frontend-app-program-manager", "https://github.com/edx/edx-bulk-grades", "https://github.com/edx/edx4edx_lite"], "slack": ["CE73RNA1J", "C18DN7JDR", "C1KMGGK7B", "CBJG9K5AB", "C1GV2QCTX", "C18CP8CFQ", "C0F4KLB5Z", "C9HL8MXRU", "CHYH0BDTR", "C321C5NVB", "C0RU5BTCP", "CDLBJS6FL", "CHJV96WS3", "C7U57FJ6M", "CFKQ54XD4", "C0NKZ5NQJ", "C5HEQHD6Y", "C0P4X6SQM", "C2X8RTMAR", "CK94QNCQ0", "CE3QFEETH", "CH95Z37A5", "C8VNEGK8S", "C0F584CH0", "CDH6K8ZK3", "C4913NQCE", "C116PL2SW", "C502JJBLN", "C0HN8M50D", "C0RE99TT4", "C0F22D6D7", "C1JL4UGVA", "C2YCNUJHG", "C1H96824B", "C13NSPFSP", "C1H7GU8VD", "C12M8M5AR", "CAXGT1PDJ", "C0MGYSC6A", "CHEU1FJ4V", "CDAG4KN2C", "CH37FF4AW", "CD93YLU9M", "C0EFVC6RK", "C1LM7G955", "C114ZRBPV", "C0WL6SPRA", "CBBLN5Q92", "CHFETNX88", "CCY2WTBK7", "C4RGQL82C", "C5EFG44P5", "C0HNBT5FT", "C9K3K46CR", "C1EDFL21M", "C5FRNT74L", "C4EAVJNNQ", "C67SNSHJB", "C0F0AD1HT", "C0YPSP0P5", "CD0H6H8P5", "CBL2US2G7", "CB1APK5D5", "CHJ7GA013", "C1K0A7BFD", "C0EUBSV7D", "C1HKV3BHV", "CA0DFM0FP", "C02SNA1U4", "C02SNEPU6", "CGSFKNDMW", "C1HF0SBA7", "C1HJ07C68", "C1HHWC8S0", "C2M6V63EV", "C2L5U7J5N", "C0PFZVB0E", "C1GS0DT7F", "CFS88FU59", "C0PG1BEAU", "C0PFYU9EV", "C0PFT4EG3", "C0PG0L40H", "C1HK3B5DY", "C0PFW2WKZ", "C0PG4D5GQ", "C1HF93HNX", "C3CBY0LBE", "C0PFZTVJN", "C3C7QUYLB", "C794AG9HP", "C1HHU62KW", "C91M88HD3", "CA9BS81T7", "CE90JM6SE", "CHFEUACKS", "C1KHYD4LT", "CFSA1T268", "CGEHJQK17", "C1N0RH6LD", "CHW5JSV9P", "C8SN0NWAC", "CA183QY2Y", "CGRU5KU6A", "CHSK2T70S", "C118NHV16", "C0DQBGEN4", "CFYRF14BZ", "C36B28HE0", "C1UEPR1FF", "C469C1QJZ", "CB29ZP7NJ", "C0F0FQS7R", "CB05HAGS2", "C4C6A836U", "C1QLT1H6D", "C70EXHW01", "C0GR05YC9", "CEJKH4VBK", "C0HRHFQ49", "C02SNEYAJ", "C5JKQTKAA", "C8VN7RGRF", "C0F0NA2F5", "C5HTRMS0J", "C1YNP01MJ", "CAY3F0BPD", "C02SNDNPC", "C2Q6MDF34", "C0F2FLRQU", "C26T5JFDX", "C0HDQ1A5P", "C0RKFAQEA", "C0X181LQ1", "C109EQPM1", "C1L370YTZ", "C20D9NWCT", "C0F63UDL0", "CH9SC5PRT", "CE6LE8WD7", "CHFCRQYDV", "CF5PSNV8S", "CJW040YMT", "C1DUYU95L", "C1HKGGL1J", "C1EH2UU07", "C586BMF5H", "C57P43CSV", "C5JFGF7FC", "C5JDBQMHS", "CAFM1HU3C", "CEJF3H52L", "CH974URD5", "C02SM402H", "C08B4LZEZ", "CELRNJ84E", "C4BTM66AW", "C26BW6LJF", "CJF1K4WKF", "CFPD5ECUB", "C0S120CBG", "C6DCAACSW", "CC4GBRA4X", "C116PL3LJ", "CD506K945", "CDB7T9K6E", "C1H7FTCTZ", "C02SUL70H", "C48CG81N0", "C0WKV86TH", "C02SNA1UC", "C0PG3FUE7", "C1X358B3K", "CCUR8HM62", "CDCCM2X7Z", "C0Q4B9YKS", "C52M3RZK2", "C1LE356SY", "CGB0S3L12", "C4YS3MLE4", "C0DQ7GA6P", "CAZ7N2SSX", "C0H4U6TFS", "C0G15M90X", "C9PPC2BHP", "CGE253B7V", "CH8LJ4ESG", "C1JRTS7T4", "C1P9TFUE7", "C1JQR69L6", "C1PB8HBFS", "C1P4K0685", "CCBJURJKY", "C1HJ0BT25", "C0GF6FTHA"]}}
    create_projects(projects4, config1)
    print("Number of repos: %s" % len(projects4["Open edX"]["git"]))
    if len(projects4['Open edX']['slack']) == 154 and len(projects4['Open edX']['github']) == 224:
        print('Test 4 Passed: Not filling data for Git and Slack')
    else:
        print('Test 4 failed')
