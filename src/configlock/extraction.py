import requests


def ext_fr_gh_public(user:str | None = "phalberg" , repo:str | None = "configlock", branch: str | None = "main", file:str | None = "config.lock.json"):
    """
    Extract from a public github repo in GitHub, the text content
    """
    raw_gh_url = "https://raw.githubusercontent.com"
    com_url = f"{raw_gh_url}/{user}/{repo}/{branch}/{file}"
    txt = requests.get(com_url)
    return txt.text
    

if __name__ == "__main__":
    
    print(ext_fr_gh_public())