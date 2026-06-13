import YAML from 'https://esm.sh/yaml';
import { Octokit } from "https://esm.sh/@octokit/core";
import { createPullRequest } from "https://esm.sh/octokit-plugin-create-pull-request";

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


function setValidationContext(pyodide, current_file_path){

        // TODO Change TO file to actually be something meaningful!
        const validatorContext = pyodide.globals.get("ValidationContext");
        const context = validatorContext(
            current_file_path,
            "config.lock.json",
            true

        );

        return context

}


function initializeWebAssembly(pyodide, pythonCode, path, lockFileContents){
        // run python code
        pyodide.runPython(pythonCode);

        const context = setValidationContext(pyodide, path)
        const validatorFunc = pyodide.globals.get("walk_yaml_in_order");
        const parsedLockFile = YAML.parse(lockFileContents);

        return [pyodide, context,validatorFunc, parsedLockFile]

}


function makePRRequest(octokit){
octokit
  .createPullRequest({
    owner: "user-or-org-login",
    repo: "repo-name",
    title: "pull request title",
    body: "pull request description",
    head: "pull-request-branch-name",
    base: "main" /* optional: defaults to default branch */,
    update: false /* optional: set to `true` to enable updating existing pull requests */,
    forceFork: false /* optional: force creating fork even when user has write rights */,
    labels: [
      "bug",
    ] /* optional: applies the given labels when user has permissions. When updating an existing pull request, already present labels will not be deleted. */
    changes: [
      {
        /* optional: if `files` is not passed, an empty commit is created instead */
        files: {
          "path/to/file1.txt": "Content for file1",
          "path/to/file2.png": {
            content: "_base64_encoded_content_",
            encoding: "base64",
          },
          // deletes file if it exists,
          "path/to/file3.txt": DELETE_FILE,
          // updates file based on current content
          "path/to/file4.txt": ({ exists, encoding, content }) => {
            // do not create the file if it does not exist
            if (!exists) return null;

            return Buffer.from(content, encoding)
              .toString("utf-8")
              .toUpperCase();
          },
          "path/to/file5.sh": {
            content: "echo Hello World",
            encoding: "utf-8",
            // one of the modes supported by the git tree object
            // https://developer.github.com/v3/git/trees/#tree-object
            mode: "100755",
          },
          "path/to/file6.txt": ({ exists, encoding, content }) => {
            // do nothing if it does not exist
            if (!exists) return null;

            const fileContent = Buffer.from(content, encoding).toString(
              "utf-8"
            );

            if (fileContent.includes("octomania")) {
              // delete file
              return DELETE_FILE;
            }

            // keep file
            return null;
          },
        },
        commit:
          "creating file1.txt, file2.png, deleting file3.txt, updating file4.txt (if it exists), file5.sh",
        /* optional: if not passed, will be the authenticated user and the current date */
        author: {
          name: "Author LastName",
          email: "Author.LastName@acme.com",
          date: new Date().toISOString(), // must be ISO date string
        },
        /* optional: if not passed, will use the information set in author */
        committer: {
          name: "Committer LastName",
          email: "Committer.LastName@acme.com",
          date: new Date().toISOString(), // must be ISO date string
        },
        /* optional: if not passed, commit won't be signed*/
        signature: async function (commitPayload) {
          // import { createSignature } from 'github-api-signature'
          //
          // return createSignature(
          //   commitPayload,
          //   privateKey,
          //   passphrase
          // );
        },
      },
    ],
  })
  .then((pr) => console.log(pr.data.number));





}




async function fetchFile() {


    const TOKEN =  document.getElementById('githubToken').value.trim();
    const octokit = new Octokit({
    auth: TOKEN,
    });

    const userName = octokit.request("GET /user");
    console.log(userName);

    const [user, repo, branch, path, output, urlBox] = formInputs();

    const [lockFilePath, validatorFilePath] = retriveGithubCodeblocks(user,repo,branch,path);

    output.innerText = 'Fetching...';
    urlBox.innerText = lockFilePath;


    let timeoutId;
    const sleep_time = 1500; 
    
    try {
        const [pyodide, lockFileContents, pythonCode] = await fetchContents(lockFilePath, validatorFilePath);

        output.innerText = lockFileContents;
        output.contentEditable = 'true';
        
        
        const [pyoDide, context, validatorFunc, parsedLockFile] = initializeWebAssembly(pyodide, pythonCode, path, lockFileContents);

        output.focus();
        output.oninput = async (event) => {
            const newContent = event.target.innerText;
            clearTimeout(timeoutId);
            
            timeoutId = setTimeout(() => {
                const parsedNewFile = YAML.parse(newContent);

                try{
                validatorFunc(
                    pyoDide.toPy(parsedNewFile),
                    pyoDide.toPy(parsedLockFile),
                    context
                );
                console.log("Success!");
                errors.innerText = "Sucess!";
                } catch(err){
                    console.log('Error: ' + err.message);
                    const errorStartIndex = err.message.indexOf("ValidationError:");

                    if (errorStartIndex !== -1) {
                        const cleanMessage = err.message.substring(errorStartIndex).trim();
                            
                        errors.innerText = cleanMessage;
                        //showNotificationBanner(cleanMessage);
                        
                    }else{
                    console.log('Error: ' + err.message);
                }
            }

            }, sleep_time);
        };
    } catch (err) {
        output.innerText = 'Error: ' + err.message;

    }
}

window.fetchFile = fetchFile;
