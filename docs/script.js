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

    try {
        const lockFileContents = await fetch(lockFile);
        const validatorCodeContents = await fetch(validatorFile);

        if (!lockFileContents.ok) throw new Error(`GitHub error: ${lockFileContents.status}`);
        if (!validatorCodeContents.ok) throw new Error(`GitHub error: ${validatorCodeContents.status}`);

        const currentLockContent = await lockFileContents.text();
        output.innerText = currentLockContent;
        output.contentEditable = 'true';
        output.focus();
        output.oninput = (event) => {
            const newContent = event.target.innerText;
            console.log('Latest output:', newContent);
        };
    } catch (err) {
        output.innerText = 'Error: ' + err.message;
    }
}

window.fetchFile = fetchFile;
