import requests
import json


def ext_fr_gh_public(
    user: str | None = "phalberg",
    repo: str | None = "configlock",
    branch: str | None = "main",
    file: str | None = "config.lock.json",
):
    """
    Extract from a public github repo in GitHub, the text content
    """
    raw_gh_url = "https://raw.githubusercontent.com"
    com_url = f"{raw_gh_url}/{user}/{repo}/{branch}/{file}"
    response = requests.get(com_url)
    data = response.json()
    return data


if __name__ == "__main__":
    json_data = json.dumps(ext_fr_gh_public(), indent=4)
    with open("test_config.json", "w", encoding="utf-8") as f:
        f.write(json_data)
