# == urls.py ==#

BASE_URL = 'https://api.github.com'


# == user urls ==#
USERS_URL = BASE_URL + '/users/{0}'

USER_HTML_URL = 'https://github.com/users/{0}'

SELF_URL = BASE_URL + '/user'

USER_REPOS_URL = USERS_URL + '/repos'

USER_ORGS_URL = USERS_URL + '/orgs'

USER_GISTS_URL = USERS_URL + '/gists'

USER_FOLLOWERS_URL = USERS_URL + '/followers'

USER_FOLLOWING_URL = USERS_URL + '/following'


# == repo urls ==#
CREATE_REPO_URL = BASE_URL + '/user/repos'  # _auth repo create

REPOS_URL = BASE_URL + '/repos/{0}'  # repos of a user

REPO_URL = BASE_URL + '/repos/{0}/{1}'  # a specific repo

ADD_FILE_URL = BASE_URL + '/repos/{}/{}/contents/{}'

ADD_FILE_BRANCH = BASE_URL + ''

REPO_ISSUE_URL = REPO_URL + '/issues/{2}'  # a specific issue

# == gist urls ==#
GIST_URL = BASE_URL + '/gists/{0}'  # specific gist

CREATE_GIST_URL = BASE_URL + '/gists'  # create a gist

# == org urls ==#
ORG_URL = BASE_URL + '/orgs/{0}'
