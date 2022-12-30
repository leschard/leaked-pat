"""Get the projects associated with a Personal Access Token."""

import urllib
import getopt
import sys
import requests
from colorama import Fore, Style

BASE_URL = 'https://gitlab.com'
ISSUE_LABEL = 'security'


def list_pat(api_url, headers):
    """List the active Personal Access Tokens linked to a user."""

    url = api_url + '/personal_access_tokens'
    resp = requests.get(url, headers=headers)

    print('\nListing of Personal Access Token of the user:')

    # Iterate on one PAT descriped as active.
    for pat in resp.json():
        if pat['active']:
            risky = False

            for item in ['api', 'write_repository', 'write_registry']:
                if item in pat['scopes']:
                    risky = True
                    break

            if risky:
                icon = Fore.RED + '💥'
            else:
                icon = '  '
            print(f"  {icon} Name: {pat['name']} \t\t| Expires at: {pat['expires_at']} \t| Scopes: {pat['scopes']}" + Style.RESET_ALL)

    print('The red color shows a write permission to API or repository or registry.')


def list_projects(api_url, headers, user, write_issue=False):
    """List associated projects to a PAT"""

    url = api_url + '/users/%i/projects' % user['id']

    request = requests.get(url, headers=headers)

    print('\nAssociated projects:')

    # Iterate in each projects associated to the user.
    for item in request.json():
        print(f"   {item['name']}")

        if write_issue:
            msg = 'A token which has write access to this project has leaked'
            title = urllib.parse.urlencode({'title': msg})

            msg = 'Please notify the user [%s](%s) so that she/he can revoke their Personal Access Tokens.' % (user['name'], user['web_url'])
            description = urllib.parse.urlencode({'description': msg, 'assignee_ids': user['id']})

            url = api_url + '/projects/%i/issues?%s&labels=%s' % (item['id'], title, ISSUE_LABEL)
            request = requests.post(url, headers=headers, data=description)

            # If returned status code is "201 Created"
            if request.status_code == 201:
                print('  - Issue created.')


def main():
    """Main function."""

    try:
        optlist, _ = getopt.getopt(sys.argv[1:], 'iht:b:', ['help'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    write_issue = False
    token_api = None
    base_url = BASE_URL

    for option, argument in optlist:
        if option == '-t':
            token_api = argument
        elif option in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif option == "-i":
            write_issue = True
        elif option == '-b':
            base_url = argument

    if not token_api:
        print('Error no token found.')
        usage()
        sys.exit(1)

    api_url = base_url + '/api/v4'

    # Build the authorization header including the PAT.
    headers = {'PRIVATE-TOKEN': token_api}

    url = api_url + '/user'
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print('Error, HTTP code: %s' % resp.status_code)
        sys.exit(1)

    user = resp.json()

    print('\nWorking on API URL: %s' % api_url)

    print('\nAccount of the Personal Access Token:')
    print('  Name: %s' % user['name'])
    print('  Id: %i' % user['id'])
    print('  eMail: %s' % user['email'])

    # List all the PAT associated to this user.
    list_pat(api_url, headers)

    # List all the projects associated to this user.
    list_projects(api_url, headers, user, write_issue)

    print('\n')


def usage():
    """Usage function."""

    print('\nUsage:')
    print('    -b BASE_URL   Gitlab Base URL. Default: %s' % BASE_URL)
    print('    -h            Display this help page.')
    print('    -i            Insert issues in projects affected by the token leak.')
    print('    -t TOKEN      Value of the Personal Access Token to use.')
    print('')


if __name__ == "__main__":
    main()
