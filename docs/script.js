import YAML from 'https://esm.sh/yaml';

function formInputs(){
    const user = document.getElementById('userName').value;
    const repo = document.getElementById('repoName').value;
    const branch = document.getElementById('branchName').value;
    const path = document.getElementById('pathToFile').value;

    const output = document.getElementById('output');
    const urlBox = document.getElementById('url');

    return [user, repo, branch, path, output, urlBox];

}

function retriveGithubCodeblocks(user, repo, branch, path){

    const lockFilePath = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/${path}`;
    const validatorFilePath = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/src/configlock/validator.py`;

    return [lockFilePath, validatorFilePath];

}



async function fetchContents(lockFilePath, validatorFilePath){
    try{

        const pyodidePromise = loadPyodide({indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/"});

        const lockFileContentsPromise = fetch(lockFilePath).then((response) => {
            if(!response.ok){
                throw new Error(`Failed to fetch lock file: ${response.status}`);
            }
            return response.text();
        });

        const validatorCodeContentsPromise = fetch(validatorFilePath).then((response) =>{
            if(!response.ok){
                throw new Error(`Failed to fetch validator file ${response.status}`)
            }

            return response.text()
        });


        const [pyod, lockFile, validatorCodeContents] = await Promise.all([
            pyodidePromise,
            lockFileContentsPromise,
            validatorCodeContentsPromise,
        ]);

        return [pyod, lockFile, validatorCodeContents];

    } catch(error){

        console.error("One of the requests failed", error);
    }



}


async function fetchFile() {

    const [user, repo, branch, path, output, urlBox] = formInputs();

    const [lockFilePath, validatorFilePath] = retriveGithubCodeblocks(user,repo,branch,path);

    output.innerText = 'Fetching...';
    urlBox.innerText = lockFilePath;


    let timeoutId;
    const sleep_time = 1500; 



    
    try {
        
        
        const [pyodide, lockFileContents, pythonCode] = await fetchContents(lockFilePath, validatorFilePath);
        pyodide.runPython(pythonCode);

        const validatorContext = pyodide.globals.get("ValidationContext");
        const context = validatorContext(
            "config.yaml",
            "config.lock.json",
            false

        );
        const validatorFunc = pyodide.globals.get("walk_yaml_in_order");


        output.innerText = lockFileContents;
        const parsedLockFile = YAML.parse(lockFileContents);


        output.contentEditable = 'true';
        output.focus();
        output.oninput = async (event) => {
            const newContent = event.target.innerText;
            clearTimeout(timeoutId);
            
            timeoutId = setTimeout(() => {
                const parsedNewFile = YAML.parse(newContent);
                validatorFunc(
                    pyodide.toPy(parsedLockFile),
                    pyodide.toPy(parsedNewFile),
                    context
                );
                console.log("Success!")
                
            }, sleep_time);
        };
    } catch (err) {
        output.innerText = 'Error: ' + err.message;
    }
}

window.fetchFile = fetchFile;
