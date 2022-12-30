# `leaked-pat.py`

Analyzing impacts of a leaked Gitlab Personal Access Token and optionally notifying it to the affected user and projects.

## Why?

Sometimes, Gitlab's Personal Access Token (PAT) giving access to several projects code (or even control API) might be found in code, config files, or lie around insecurely in CI/CD bricks.
`leaked-pat.py` will make it easier to identify the impacts of a leaked PAT:

* To which user account is linked the PAT?
* What are the characteristics of the PAT(s) linked to this account? (read/write, scope, expiration date)
* On which projects this PAT might have read/write permissions?

Optionally (`-i` flag) and if the PAT has API write permissions, Gitlab issues can be raised to notify the user and the projects which are impacted by the token leak.

## Installation

```shell
git clone https://github.com/leschard/leaked-api
pip3 install -r ./requirements.txt
```

## Usage

Simple usage for Gitlab.com instance.

```shell
python3 ./leaked_pat.py -t TOKEN
```

Usage on an on-premise Gitlab instance.

```shell
python3 ./leaked_pat.py -t TOKEN -b https://gitlab.yourcompany.com
```

```shell
Usage:
    -b BASE_URL   Gitlab Base URL. Default: https://gitlab.com
    -h            Display this help page.
    -i            Insert issues in projects affected by the token leak.
    -t TOKEN      Value of the Personal Access Token to use.
```
