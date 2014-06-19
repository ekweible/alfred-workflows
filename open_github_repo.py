# system imports
import json
import os
import re

# internal imports
import alfred


# paths
DATA_PATH = '/Users/evanweible/dev/ekweible/alfred-workflows/data'

# workflow info
WORKFLOW_SUBTITLE = 'Open GitHub Repo'
WORKFLOW_UID = 'open-github-repo-workflow'

# icons
GITHUB_ICON = '/Users/evanweible/dev/ekweible/alfred-workflows/icons/GitHub-Mark-120px-plus.png'

# regex patterns
SEARCH_REGEX = '.*%s.*'

# local data store
DATA = {}


def main():
    load_data()
    alfred.send_results(get_results())


def load_data():
    DATA['repos'] = json.load(open(os.path.join(DATA_PATH, 'git_repos.json')))
    DATA['users'] = json.load(open(os.path.join(DATA_PATH, 'git_users.json')))


def get_results():
    query = alfred.get_query()
    search_terms = get_search_terms(query)
    repo_items = search_repos(search_terms)
    results = [alfred.Item(**item) for item in repo_items]
    return results


def get_search_terms(query):
    return [term.strip() for term in query.split(' ') if len(term.strip())]


def search_repos(search_terms):
    repo_match_sets = []
    user_match_sets = []

    # get matching result sets for each search term
    for term in search_terms:
        repos, users = search(term)
        repo_match_sets.append(repos)
        user_match_sets.append(users)

    # get union of repo and user match sets
    repos = set.union(*repo_match_sets)
    users = set.union(*user_match_sets)

    # if both sets are empty, no matches were found
    if len(repos) == 0 and len(users) == 0:
        return []

    # if only one set (repos OR users) is empty, default it to the entire list
    if len(repos) == 0:
        repos = set(DATA['repos'])
    elif len(users) == 0:
        users = set(DATA['users'])

    # combine repos and users to form result set
    results = []
    for repo in repos:
        results.extend([create_repo_result(repo, user) for user in users])

    return results


def search(search_term):
    search_pattern = re.compile(SEARCH_REGEX % search_term.lower())

    repo_matches = set(repo for repo in DATA['repos'] if search_pattern.match(repo.lower()))
    user_matches = set(user for user in DATA['users'] if search_pattern.match(user.lower()))

    return repo_matches, user_matches


def create_repo_result(repo, user):
    return {
        'uid': '%s-%s-%s' % (WORKFLOW_UID, repo, user),
        'value': '%s/%s' % (user, repo),
        'title': '%s/%s' % (user, repo),
        'subtitle': WORKFLOW_SUBTITLE,
        'icon': GITHUB_ICON
    }


if __name__ == '__main__':
    main()