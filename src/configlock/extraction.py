import requests


def ext_fr_gh_public(user:str, repo:str, branch: str, file:str):
    """
    Extract from a public github repo in GitHub, the text content
    """
    url = "https://raw.githubusercontent.com/phalberg/configlock/main/config.lock.json"
    txt = requests.get(url)
    return txt.text
    

if __name__ == "__main__":
    
    print(ext_fr_gh_public())