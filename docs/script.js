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


async function fetchFile() {

    const [user, repo, branch, path, output, urlBox] = formInputs()


    output.innerText = 'Fetching...';
    const lockFile = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/${path}`;
    const validatorFile = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/src/configlock/validator.py`;
    urlBox.innerText = lockFile;


    let timeoutId;
    const sleep_time = 1500; 


    try {

        
        let pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/"});

        const lockFileContents = await fetch(lockFile);

        const validatorCodeContents = await fetch(validatorFile);
        const pythonCode = await validatorCodeContents.text();
        pyodide.runPython(pythonCode);

        const validatorContext = pyodide.globals.get("ValidationContext");
        const context = validatorContext(
            "config.yaml",
            "config.lock.json",
            false

        );
        const validatorFunc = pyodide.globals.get("walk_yaml_in_order");

        if (!lockFileContents.ok) throw new Error(`GitHub error: ${lockFileContents.status}`);
        if (!validatorCodeContents.ok) throw new Error(`GitHub error: ${validatorCodeContents.status}`);

        const currentLockContent = await lockFileContents.text();
        output.innerText = currentLockContent;
        const parsedLockFile = YAML.parse(currentLockContent);


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
