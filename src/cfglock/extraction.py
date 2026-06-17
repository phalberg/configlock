import requests


def extract_fr_gh_public(
    user: str,
    repo: str,
    branch: str,
    file: str,
):
    """
    Extract from a public github repo in GitHub, the text content
    """
    raw_gh_url = "https://raw.githubusercontent.com"
    com_url = f"{raw_gh_url}/{user}/{repo}/{branch}/{file}"
    response = requests.get(com_url)
    data = response.json()
    return data


def extract_fr_gh_private(some_value: str):
    # placeholder for now
    pass
