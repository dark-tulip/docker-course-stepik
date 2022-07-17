import requests
from datetime import datetime
from github import Github, GithubException

g = Github("YOUR_TOKEN")

SINCE = datetime(2016, 1, 1, 0, 0)
UNTIL = datetime(2017, 1, 1, 0, 0)
TOTAL_COMMITS = 0


def parse_url(url):
    """
    :param raw_url: https://github.com/username/repo_name
    :return: username/repo_name
    """
    return url.replace("https://github.com/", "")


def get_redirected_url(raw_url):
    """
    If url was changed or redirected
    :param raw_url: url
    :return: new valid url
    """
    return requests.get(raw_url.strip()).url


with open('urls.txt') as file:
    for url in file:
        try:
            url = get_redirected_url(url)  # чтобы получить redirected url
            repo = g.get_repo(parse_url(url))
            
            commits_in_repo = repo.get_commits(since=SINCE, until=UNTIL).totalCount  # master or main by default            
            print(url.ljust(75), commits_in_repo)  # format by left side
            TOTAL_COMMITS += commits_in_repo

        except GithubException:
            print("Error, master branch not found: ", url)

print("Total commits:", TOTAL_COMMITS)
