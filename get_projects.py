"""
Gets all of the repos/channels for a grimoirelabs project
"""
import os
import github3
import json
from slack import WebClient


def create_projects(projects, config):
    git_token = config['github']['api-token']
    slack_token = config['slack']['api-token']
    discourse_token = config['discourse']['api-token']

    for key in projects:
        if 'git' in projects[key] and 'http' not in projects[key]['git']:

            git_repos = []
            
            for organization in projects[key]['git']:
                git_repos.extend(get_git_repos(organization, git_token))
                
            projects[key]['git'] = git_repos
            projects[key]['github'] = git_repos
            projects[key]['github:repo'] = git_repos
            
        if 'slack' in projects[key] and projects[key]['slack'] == []:
            projects[key]['slack'] = get_slack_channels(slack_token)
        if 'discourse' in projects[key] and projects[key]['discourse'] == []:
            projects[key]['discourse'] = ["https://discuss.openedx.org"]
    return projects

def get_git_repos(org, token):
    gh = github3.login(token = token)
    repos = gh.organization(org).repositories('public')
    repo_list = []
    for repo in repos:
        if not repo.fork:
            repo_list.append(repo.html_url)
    return repo_list

def get_slack_channels(token):
    client = WebClient(token=token)
    channels = client.conversations_list(exclude_archived=True)
    channel_list = []
    for channel in channels['channels']:
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
            "git": [ 'https://github.com/openedx/publisher-frontend'],
            "github": ['https://github.com/openedx/publisher-frontend'],
            "github:repos": ['https://github.com/openedx/publisher-frontend'],
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
            "git": [ 'https://github.com/openedx/publisher-frontend'],
            "github": ['https://github.com/openedx/publisher-frontend'],
            "github:repos": ['https://github.com/openedx/publisher-frontend'],
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
    projects4 = {"Open edX": {"git": ["https://github.com/openedx/cs_comments_service", "https://github.com/openedx/xqueue", "https://github.com/openedx/django-wiki", "https://github.com/openedx/ease", "https://github.com/openedx/edx-ora", "https://github.com/openedx/loghandlersplus", "https://github.com/openedx/XBlock", "https://github.com/openedx/djeventstream", "https://github.com/openedx/insights", "https://github.com/openedx/edxanalytics", "https://github.com/openedx/archived-edx.github.io", "https://github.com/openedx/configuration", "https://github.com/openedx/codejail", "https://github.com/openedx/arch-prototype", "https://github.com/openedx/skel", "https://github.com/openedx/edx-platform", "https://github.com/openedx/xserver", "https://github.com/openedx/edx-tools", "https://github.com/openedx/js-test-tool", "https://github.com/openedx/notifier", "https://github.com/openedx/event-tracking", "https://github.com/openedx/git-client-plugin", "https://github.com/openedx/edx-demo-course", "https://github.com/openedx/patch-juggler", "https://github.com/openedx/repo-tools", "https://github.com/openedx/git-plugin", "https://github.com/openedx/edx-e2e-tests", "https://github.com/openedx/bok-choy", "https://github.com/openedx/asgard", "https://github.com/openedx/datajam", "https://github.com/openedx/datajam-analytics", "https://github.com/openedx/edx-ora2", "https://github.com/openedx/test-metrics", "https://github.com/openedx/acid-block", "https://github.com/openedx/xblock-sdk", "https://github.com/openedx/edx-certificates", "https://github.com/openedx/xqueue-watcher", "https://github.com/openedx/dogapi", "https://github.com/openedx/alton", "https://github.com/openedx/opaque-keys", "https://github.com/openedx/edx-analytics-data-api", "https://github.com/openedx/i18n-tools", "https://github.com/openedx/edx-submissions", "https://github.com/openedx/edx-analytics-dashboard", "https://github.com/openedx/django-oauth2-provider", "https://github.com/openedx/edx-val", "https://github.com/openedx/openedx-webhooks", "https://github.com/openedx/edx-analytics-configuration", "https://github.com/openedx/edx-analytics-data-api-client", "https://github.com/openedx/edx-analytics-pipeline", "https://github.com/openedx/edx-oauth2-provider", "https://github.com/openedx/django-lang-pref-middleware", "https://github.com/openedx/edx-documentation", "https://github.com/openedx/luigi", "https://github.com/openedx/xblock-utils", "https://github.com/openedx/edx-fonts", "https://github.com/openedx/edx-analytics-api-client", "https://github.com/openedx/harprofiler", "https://github.com/openedx/MongoDBProxy", "https://github.com/openedx/edx-notes-api", "https://github.com/openedx/edx-analytics-hadoop-util", "https://github.com/openedx/edx-milestones", "https://github.com/openedx/edx-django-profiler", "https://github.com/openedx/edx-notifications", "https://github.com/openedx/edx-app-ios", "https://github.com/openedx/edx-app-android", "https://github.com/openedx/edx-search", "https://github.com/openedx/ux-pattern-library", "https://github.com/openedx/pyinstrument", "https://github.com/openedx/edx-lint", "https://github.com/openedx/ecommerce", "https://github.com/openedx/auth-backends", "https://github.com/openedx/edx-app-gradle-plugin", "https://github.com/openedx/testeng-ci", "https://github.com/openedx/edx-reverification-block", "https://github.com/openedx/edx-rest-api-client", "https://github.com/openedx/thumb-stack", "https://github.com/openedx/edx-common-client", "https://github.com/openedx/edx-proctoring", "https://github.com/openedx/edx-user-state-client", "https://github.com/openedx/ecommerce-scripts", "https://github.com/openedx/edx-organizations", "https://github.com/openedx/ccx-keys", "https://github.com/openedx/discussions", "https://github.com/openedx/edx-load-tests", "https://github.com/openedx/xsy", "https://github.com/openedx/edx-ui-toolkit", "https://github.com/openedx/openedx-conference-pages", "https://github.com/openedx/django-rest-framework-oauth", "https://github.com/openedx/cookiecutter-django-ida", "https://github.com/openedx/programs", "https://github.com/openedx/demo-performance-course", "https://github.com/openedx/ecommerce-worker", "https://github.com/openedx/django-openid-auth", "https://github.com/openedx/django-pyfs", "https://github.com/openedx/django-rest-framework", "https://github.com/openedx/demo-test-course", "https://github.com/openedx/build-pipeline", "https://github.com/openedx/edx-custom-a11y-rules", "https://github.com/openedx/django-splash", "https://github.com/openedx/edx-analytics-exporter", "https://github.com/openedx/xblock-lti-consumer", "https://github.com/openedx/course-discovery", "https://github.com/openedx/credentials", "https://github.com/openedx/edx-django-extensions", "https://github.com/openedx/edx-grader-support", "https://github.com/openedx/tubular", "https://github.com/openedx/dummy-webapp", "https://github.com/openedx/edx-capa", "https://github.com/openedx/edx-django-release-util", "https://github.com/openedx/edx-drf-extensions", "https://github.com/openedx/edx-django-sites-extensions", "https://github.com/openedx/pa11ycrawler", "https://github.com/openedx/open-edx-proposals", "https://github.com/openedx/edx-icon", "https://github.com/openedx/api-manager", "https://github.com/openedx/sample-themes", "https://github.com/openedx/jenkins-job-dsl", "https://github.com/openedx/openedxstats", "https://github.com/openedx/gomatic", "https://github.com/openedx/edx-safety", "https://github.com/openedx/edx-gomatic", "https://github.com/openedx/eslint-config-edx", "https://github.com/openedx/cookiecutter-django-app", "https://github.com/openedx/vagrant-timer", "https://github.com/openedx/edx-app-android-white-label-demo", "https://github.com/openedx/cookiecutter-xblock", "https://github.com/openedx/django-user-tasks", "https://github.com/openedx/notifications", "https://github.com/openedx/notifications-pipeline-steps", "https://github.com/openedx/edx-sphinx-theme", "https://github.com/openedx/django-config-models", "https://github.com/openedx/edx-enterprise", "https://github.com/openedx/web-fragments", "https://github.com/openedx/devstack", "https://github.com/openedx/pa11ycrawler-ignore", "https://github.com/openedx/edx-celeryutils", "https://github.com/openedx/edx-salesforce", "https://github.com/openedx/credentials-themes", "https://github.com/openedx/help-tokens", "https://github.com/openedx/paragon", "https://github.com/openedx/language-negotiation-lambda", "https://github.com/openedx/edx-docker-base", "https://github.com/openedx/jenkins-configuration", "https://github.com/openedx/py-opt-cli", "https://github.com/openedx/supported-components", "https://github.com/openedx/bootstrapped", "https://github.com/openedx/edx-bootstrap", "https://github.com/openedx/edx-video-pipeline", "https://github.com/openedx/edx-video-worker", "https://github.com/openedx/ConceptXBlock", "https://github.com/openedx/AudioXBlock", "https://github.com/openedx/RecommenderXBlock", "https://github.com/openedx/AnimationXBlock", "https://github.com/openedx/RateXBlock", "https://github.com/openedx/DoneXBlock", "https://github.com/openedx/django-celery", "https://github.com/openedx/edx-ace", "https://github.com/openedx/studio-frontend", "https://github.com/openedx/stylelint-config-edx", "https://github.com/openedx/xblock-review", "https://github.com/openedx/django-oauth-plus", "https://github.com/openedx/edx-enterprise-data", "https://github.com/openedx/analytics-python", "https://github.com/openedx/edx-app-test", "https://github.com/openedx/edx-app-qa", "https://github.com/openedx/completion", "https://github.com/openedx/openedx-census", "https://github.com/openedx/frontend-cookie-cutter-application", "https://github.com/openedx/journals", "https://github.com/openedx/user-util", "https://github.com/openedx/XSS-Linter", "https://github.com/openedx/cookie-policy-banner", "https://github.com/openedx/xapi-events", "https://github.com/openedx/create-edx-react-app", "https://github.com/openedx/docs.edx.org", "https://github.com/openedx/chunkey", "https://github.com/openedx/v_videocompile", "https://github.com/openedx/edx-portal", "https://github.com/openedx/cookie-cutter-react-component-library", "https://github.com/openedx/floor-plan-connector", "https://github.com/openedx/journals-frontend", "https://github.com/openedx/django-plugins", "https://github.com/openedx/edx-toggles", "https://github.com/openedx/TinCanPython", "https://github.com/openedx/edx-django-utils", "https://github.com/openedx/frontend-cookiecutter-library", "https://github.com/openedx/vertica_docker", "https://github.com/openedx/xss-utils", "https://github.com/openedx/frontend-auth", "https://github.com/openedx/edx-developer-docs", "https://github.com/openedx/gradebook", "https://github.com/openedx/mockprock", "https://github.com/openedx/code-annotations", "https://github.com/openedx/cypress-e2e-tests", "https://github.com/openedx/publisher-frontend", "https://github.com/openedx/mdrst", "https://github.com/openedx/frontend-component-footer", "https://github.com/openedx/frontend-component-site-header", "https://github.com/openedx/frontend-app-profile", "https://github.com/openedx/hermes", "https://github.com/openedx/registrar", "https://github.com/openedx/asym-crypto-yaml", "https://github.com/openedx/edx-rbac", "https://github.com/openedx/edx-when", "https://github.com/openedx/crowdsourcehinter", "https://github.com/openedx/html-webpack-new-relic-plugin", "https://github.com/openedx/frontend-app-learner-portal", "https://github.com/openedx/frontend-analytics", "https://github.com/openedx/frontend-logging", "https://github.com/openedx/frontend-app-ecommerce", "https://github.com/openedx/openedx-calc", "https://github.com/openedx/frontend-app-account", "https://github.com/openedx/frontend-common", "https://github.com/openedx/edx-zoom", "https://github.com/openedx/portal-designer", "https://github.com/openedx/frontend-app-payment", "https://github.com/openedx/openedx-chem", "https://github.com/openedx/frontend-i18n", "https://github.com/openedx/staff_graded-xblock", "https://github.com/openedx/super-csv", "https://github.com/openedx/frontend-app-program-manager", "https://github.com/openedx/edx-bulk-grades", "https://github.com/openedx/edx4edx_lite"], "github": ["https://github.com/openedx/cs_comments_service", "https://github.com/openedx/xqueue", "https://github.com/openedx/django-wiki", "https://github.com/openedx/ease", "https://github.com/openedx/edx-ora", "https://github.com/openedx/loghandlersplus", "https://github.com/openedx/XBlock", "https://github.com/openedx/djeventstream", "https://github.com/openedx/insights", "https://github.com/openedx/edxanalytics", "https://github.com/openedx/archived-edx.github.io", "https://github.com/openedx/configuration", "https://github.com/openedx/codejail", "https://github.com/openedx/arch-prototype", "https://github.com/openedx/skel", "https://github.com/openedx/edx-platform", "https://github.com/openedx/xserver", "https://github.com/openedx/edx-tools", "https://github.com/openedx/js-test-tool", "https://github.com/openedx/notifier", "https://github.com/openedx/event-tracking", "https://github.com/openedx/git-client-plugin", "https://github.com/openedx/edx-demo-course", "https://github.com/openedx/patch-juggler", "https://github.com/openedx/repo-tools", "https://github.com/openedx/git-plugin", "https://github.com/openedx/edx-e2e-tests", "https://github.com/openedx/bok-choy", "https://github.com/openedx/asgard", "https://github.com/openedx/datajam", "https://github.com/openedx/datajam-analytics", "https://github.com/openedx/edx-ora2", "https://github.com/openedx/test-metrics", "https://github.com/openedx/acid-block", "https://github.com/openedx/xblock-sdk", "https://github.com/openedx/edx-certificates", "https://github.com/openedx/xqueue-watcher", "https://github.com/openedx/dogapi", "https://github.com/openedx/alton", "https://github.com/openedx/opaque-keys", "https://github.com/openedx/edx-analytics-data-api", "https://github.com/openedx/i18n-tools", "https://github.com/openedx/edx-submissions", "https://github.com/openedx/edx-analytics-dashboard", "https://github.com/openedx/django-oauth2-provider", "https://github.com/openedx/edx-val", "https://github.com/openedx/openedx-webhooks", "https://github.com/openedx/edx-analytics-configuration", "https://github.com/openedx/edx-analytics-data-api-client", "https://github.com/openedx/edx-analytics-pipeline", "https://github.com/openedx/edx-oauth2-provider", "https://github.com/openedx/django-lang-pref-middleware", "https://github.com/openedx/edx-documentation", "https://github.com/openedx/luigi", "https://github.com/openedx/xblock-utils", "https://github.com/openedx/edx-fonts", "https://github.com/openedx/edx-analytics-api-client", "https://github.com/openedx/harprofiler", "https://github.com/openedx/MongoDBProxy", "https://github.com/openedx/edx-notes-api", "https://github.com/openedx/edx-analytics-hadoop-util", "https://github.com/openedx/edx-milestones", "https://github.com/openedx/edx-django-profiler", "https://github.com/openedx/edx-notifications", "https://github.com/openedx/edx-app-ios", "https://github.com/openedx/edx-app-android", "https://github.com/openedx/edx-search", "https://github.com/openedx/ux-pattern-library", "https://github.com/openedx/pyinstrument", "https://github.com/openedx/edx-lint", "https://github.com/openedx/ecommerce", "https://github.com/openedx/auth-backends", "https://github.com/openedx/edx-app-gradle-plugin", "https://github.com/openedx/testeng-ci", "https://github.com/openedx/edx-reverification-block", "https://github.com/openedx/edx-rest-api-client", "https://github.com/openedx/thumb-stack", "https://github.com/openedx/edx-common-client", "https://github.com/openedx/edx-proctoring", "https://github.com/openedx/edx-user-state-client", "https://github.com/openedx/ecommerce-scripts", "https://github.com/openedx/edx-organizations", "https://github.com/openedx/ccx-keys", "https://github.com/openedx/discussions", "https://github.com/openedx/edx-load-tests", "https://github.com/openedx/xsy", "https://github.com/openedx/edx-ui-toolkit", "https://github.com/openedx/openedx-conference-pages", "https://github.com/openedx/django-rest-framework-oauth", "https://github.com/openedx/cookiecutter-django-ida", "https://github.com/openedx/programs", "https://github.com/openedx/demo-performance-course", "https://github.com/openedx/ecommerce-worker", "https://github.com/openedx/django-openid-auth", "https://github.com/openedx/django-pyfs", "https://github.com/openedx/django-rest-framework", "https://github.com/openedx/demo-test-course", "https://github.com/openedx/build-pipeline", "https://github.com/openedx/edx-custom-a11y-rules", "https://github.com/openedx/django-splash", "https://github.com/openedx/edx-analytics-exporter", "https://github.com/openedx/xblock-lti-consumer", "https://github.com/openedx/course-discovery", "https://github.com/openedx/credentials", "https://github.com/openedx/edx-django-extensions", "https://github.com/openedx/edx-grader-support", "https://github.com/openedx/tubular", "https://github.com/openedx/dummy-webapp", "https://github.com/openedx/edx-capa", "https://github.com/openedx/edx-django-release-util", "https://github.com/openedx/edx-drf-extensions", "https://github.com/openedx/edx-django-sites-extensions", "https://github.com/openedx/pa11ycrawler", "https://github.com/openedx/open-edx-proposals", "https://github.com/openedx/edx-icon", "https://github.com/openedx/api-manager", "https://github.com/openedx/sample-themes", "https://github.com/openedx/jenkins-job-dsl", "https://github.com/openedx/openedxstats", "https://github.com/openedx/gomatic", "https://github.com/openedx/edx-safety", "https://github.com/openedx/edx-gomatic", "https://github.com/openedx/eslint-config-edx", "https://github.com/openedx/cookiecutter-django-app", "https://github.com/openedx/vagrant-timer", "https://github.com/openedx/edx-app-android-white-label-demo", "https://github.com/openedx/cookiecutter-xblock", "https://github.com/openedx/django-user-tasks", "https://github.com/openedx/notifications", "https://github.com/openedx/notifications-pipeline-steps", "https://github.com/openedx/edx-sphinx-theme", "https://github.com/openedx/django-config-models", "https://github.com/openedx/edx-enterprise", "https://github.com/openedx/web-fragments", "https://github.com/openedx/devstack", "https://github.com/openedx/pa11ycrawler-ignore", "https://github.com/openedx/edx-celeryutils", "https://github.com/openedx/edx-salesforce", "https://github.com/openedx/credentials-themes", "https://github.com/openedx/help-tokens", "https://github.com/openedx/paragon", "https://github.com/openedx/language-negotiation-lambda", "https://github.com/openedx/edx-docker-base", "https://github.com/openedx/jenkins-configuration", "https://github.com/openedx/py-opt-cli", "https://github.com/openedx/supported-components", "https://github.com/openedx/bootstrapped", "https://github.com/openedx/edx-bootstrap", "https://github.com/openedx/edx-video-pipeline", "https://github.com/openedx/edx-video-worker", "https://github.com/openedx/ConceptXBlock", "https://github.com/openedx/AudioXBlock", "https://github.com/openedx/RecommenderXBlock", "https://github.com/openedx/AnimationXBlock", "https://github.com/openedx/RateXBlock", "https://github.com/openedx/DoneXBlock", "https://github.com/openedx/django-celery", "https://github.com/openedx/edx-ace", "https://github.com/openedx/studio-frontend", "https://github.com/openedx/stylelint-config-edx", "https://github.com/openedx/xblock-review", "https://github.com/openedx/django-oauth-plus", "https://github.com/openedx/edx-enterprise-data", "https://github.com/openedx/analytics-python", "https://github.com/openedx/edx-app-test", "https://github.com/openedx/edx-app-qa", "https://github.com/openedx/completion", "https://github.com/openedx/openedx-census", "https://github.com/openedx/frontend-cookie-cutter-application", "https://github.com/openedx/journals", "https://github.com/openedx/user-util", "https://github.com/openedx/XSS-Linter", "https://github.com/openedx/cookie-policy-banner", "https://github.com/openedx/xapi-events", "https://github.com/openedx/create-edx-react-app", "https://github.com/openedx/docs.edx.org", "https://github.com/openedx/chunkey", "https://github.com/openedx/v_videocompile", "https://github.com/openedx/edx-portal", "https://github.com/openedx/cookie-cutter-react-component-library", "https://github.com/openedx/floor-plan-connector", "https://github.com/openedx/journals-frontend", "https://github.com/openedx/django-plugins", "https://github.com/openedx/edx-toggles", "https://github.com/openedx/TinCanPython", "https://github.com/openedx/edx-django-utils", "https://github.com/openedx/frontend-cookiecutter-library", "https://github.com/openedx/vertica_docker", "https://github.com/openedx/xss-utils", "https://github.com/openedx/frontend-auth", "https://github.com/openedx/edx-developer-docs", "https://github.com/openedx/gradebook", "https://github.com/openedx/mockprock", "https://github.com/openedx/code-annotations", "https://github.com/openedx/cypress-e2e-tests", "https://github.com/openedx/publisher-frontend", "https://github.com/openedx/mdrst", "https://github.com/openedx/frontend-component-footer", "https://github.com/openedx/frontend-component-site-header", "https://github.com/openedx/frontend-app-profile", "https://github.com/openedx/hermes", "https://github.com/openedx/registrar", "https://github.com/openedx/asym-crypto-yaml", "https://github.com/openedx/edx-rbac", "https://github.com/openedx/edx-when", "https://github.com/openedx/crowdsourcehinter", "https://github.com/openedx/html-webpack-new-relic-plugin", "https://github.com/openedx/frontend-app-learner-portal", "https://github.com/openedx/frontend-analytics", "https://github.com/openedx/frontend-logging", "https://github.com/openedx/frontend-app-ecommerce", "https://github.com/openedx/openedx-calc", "https://github.com/openedx/frontend-app-account", "https://github.com/openedx/frontend-common", "https://github.com/openedx/edx-zoom", "https://github.com/openedx/portal-designer", "https://github.com/openedx/frontend-app-payment", "https://github.com/openedx/openedx-chem", "https://github.com/openedx/frontend-i18n", "https://github.com/openedx/staff_graded-xblock", "https://github.com/openedx/super-csv", "https://github.com/openedx/frontend-app-program-manager", "https://github.com/openedx/edx-bulk-grades", "https://github.com/openedx/edx4edx_lite"], "slack": ["CE73RNA1J", "C18DN7JDR", "C1KMGGK7B", "CBJG9K5AB", "C1GV2QCTX", "C18CP8CFQ", "C0F4KLB5Z", "C9HL8MXRU", "CHYH0BDTR", "C321C5NVB", "C0RU5BTCP", "CDLBJS6FL", "CHJV96WS3", "C7U57FJ6M", "CFKQ54XD4", "C0NKZ5NQJ", "C5HEQHD6Y", "C0P4X6SQM", "C2X8RTMAR", "CK94QNCQ0", "CE3QFEETH", "CH95Z37A5", "C8VNEGK8S", "C0F584CH0", "CDH6K8ZK3", "C4913NQCE", "C116PL2SW", "C502JJBLN", "C0HN8M50D", "C0RE99TT4", "C0F22D6D7", "C1JL4UGVA", "C2YCNUJHG", "C1H96824B", "C13NSPFSP", "C1H7GU8VD", "C12M8M5AR", "CAXGT1PDJ", "C0MGYSC6A", "CHEU1FJ4V", "CDAG4KN2C", "CH37FF4AW", "CD93YLU9M", "C0EFVC6RK", "C1LM7G955", "C114ZRBPV", "C0WL6SPRA", "CBBLN5Q92", "CHFETNX88", "CCY2WTBK7", "C4RGQL82C", "C5EFG44P5", "C0HNBT5FT", "C9K3K46CR", "C1EDFL21M", "C5FRNT74L", "C4EAVJNNQ", "C67SNSHJB", "C0F0AD1HT", "C0YPSP0P5", "CD0H6H8P5", "CBL2US2G7", "CB1APK5D5", "CHJ7GA013", "C1K0A7BFD", "C0EUBSV7D", "C1HKV3BHV", "CA0DFM0FP", "C02SNA1U4", "C02SNEPU6", "CGSFKNDMW", "C1HF0SBA7", "C1HJ07C68", "C1HHWC8S0", "C2M6V63EV", "C2L5U7J5N", "C0PFZVB0E", "C1GS0DT7F", "CFS88FU59", "C0PG1BEAU", "C0PFYU9EV", "C0PFT4EG3", "C0PG0L40H", "C1HK3B5DY", "C0PFW2WKZ", "C0PG4D5GQ", "C1HF93HNX", "C3CBY0LBE", "C0PFZTVJN", "C3C7QUYLB", "C794AG9HP", "C1HHU62KW", "C91M88HD3", "CA9BS81T7", "CE90JM6SE", "CHFEUACKS", "C1KHYD4LT", "CFSA1T268", "CGEHJQK17", "C1N0RH6LD", "CHW5JSV9P", "C8SN0NWAC", "CA183QY2Y", "CGRU5KU6A", "CHSK2T70S", "C118NHV16", "C0DQBGEN4", "CFYRF14BZ", "C36B28HE0", "C1UEPR1FF", "C469C1QJZ", "CB29ZP7NJ", "C0F0FQS7R", "CB05HAGS2", "C4C6A836U", "C1QLT1H6D", "C70EXHW01", "C0GR05YC9", "CEJKH4VBK", "C0HRHFQ49", "C02SNEYAJ", "C5JKQTKAA", "C8VN7RGRF", "C0F0NA2F5", "C5HTRMS0J", "C1YNP01MJ", "CAY3F0BPD", "C02SNDNPC", "C2Q6MDF34", "C0F2FLRQU", "C26T5JFDX", "C0HDQ1A5P", "C0RKFAQEA", "C0X181LQ1", "C109EQPM1", "C1L370YTZ", "C20D9NWCT", "C0F63UDL0", "CH9SC5PRT", "CE6LE8WD7", "CHFCRQYDV", "CF5PSNV8S", "CJW040YMT", "C1DUYU95L", "C1HKGGL1J", "C1EH2UU07", "C586BMF5H", "C57P43CSV", "C5JFGF7FC", "C5JDBQMHS", "CAFM1HU3C", "CEJF3H52L", "CH974URD5", "C02SM402H", "C08B4LZEZ", "CELRNJ84E", "C4BTM66AW", "C26BW6LJF", "CJF1K4WKF", "CFPD5ECUB", "C0S120CBG", "C6DCAACSW", "CC4GBRA4X", "C116PL3LJ", "CD506K945", "CDB7T9K6E", "C1H7FTCTZ", "C02SUL70H", "C48CG81N0", "C0WKV86TH", "C02SNA1UC", "C0PG3FUE7", "C1X358B3K", "CCUR8HM62", "CDCCM2X7Z", "C0Q4B9YKS", "C52M3RZK2", "C1LE356SY", "CGB0S3L12", "C4YS3MLE4", "C0DQ7GA6P", "CAZ7N2SSX", "C0H4U6TFS", "C0G15M90X", "C9PPC2BHP", "CGE253B7V", "CH8LJ4ESG", "C1JRTS7T4", "C1P9TFUE7", "C1JQR69L6", "C1PB8HBFS", "C1P4K0685", "CCBJURJKY", "C1HJ0BT25", "C0GF6FTHA"]}}
    create_projects(projects4, config1)
    print("Number of repos: %s" % len(projects4["Open edX"]["git"]))
    if len(projects4['Open edX']['slack']) == 154 and len(projects4['Open edX']['github']) == 224:
        print('Test 4 Passed: Not filling data for Git and Slack')
    else:
        print('Test 4 failed')
