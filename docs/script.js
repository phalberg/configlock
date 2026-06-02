import YAML from 'https://esm.sh/yaml';


async function fetchFile() {
    const user = document.getElementById('user').value;
    const repo = document.getElementById('repo').value;
    const branch = document.getElementById('branch').value;
    const path = document.getElementById('path').value;
    const output = document.getElementById('output');
    const urlBox = document.getElementById('url');

    output.innerText = 'Fetching...';
    const lockFile = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/${path}`;
    const validatorFile = `https://raw.githubusercontent.com/${user}/${repo}/${branch}/src/configlock/validator.py`;
    urlBox.innerText = lockFile;


    let timeoutId;
    const sleep_time = 1500; 

    async function startPython(runCode){
            let pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/"
            });
            pyodide.runPython(runCode);
            console.log("Finihsed running!");
    }


    try {



        const lockFileContents = await fetch(lockFile);

        const validatorCodeContents = await fetch(validatorFile);
        const pythonCode = await validatorCodeContents.text();

        startPython(pythonCode);

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
                console.log("Pased YAML file here::", YAML.parse(newContent));
            }, sleep_time);
        };
    } catch (err) {
        output.innerText = 'Error: ' + err.message;
    }
}

window.fetchFile = fetchFile;
