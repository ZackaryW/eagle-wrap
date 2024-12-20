const fs = require('fs');
const { exec } = require('child_process');

async function createCtxString(eagle, obj = {}) {
    const ctx = {};
    // await for eagle.item.getSelected();
    ctx.selectedItems = [];
    for (const item of await eagle.item.getSelected()) {
        ctx.selectedItems.push(item.id);
    }

    ctx.selectedFolders = [];
    for (const folder of await eagle.folder.getSelected()){
        ctx.selectedFolders.push(folder.id);
    }
    console.log("ctx: ", ctx);

    //handle obj
    for (const key in obj) {
        ctx[key] = obj[key];
    }

    const ctxString = Buffer.from(JSON.stringify(ctx)).toString('base64');
    console.log("ctxString: ", ctxString);
    return ctxString;
}

async function executePythonScript(eagle, scriptPath, ctxString) {
    
    // check if scriptPath is a file
    console.log("recived scriptPath: ", scriptPath);
    if (!fs.existsSync(scriptPath)) {
        throw new Error(`Script file not found: ${scriptPath}`);
    }

    // check if os command eaglewrap exists
    const whichCommand = process.platform === 'win32' ? 'where' : 'which';
    try {
        require('child_process').execSync(`${whichCommand} eaglewrap`);
    } catch (error) {
        throw new Error(`eaglewrap command not found`);
    }

    // run the script and capture stdout
    return new Promise((resolve, reject) => {
        const childProcess = exec(`eaglewrap script "${scriptPath}" ${ctxString}`);
        let stdout = '';
        let stderr = '';

        childProcess.stdout.on('data', (data) => {
            stdout += data;
        });

        childProcess.stderr.on('data', (data) => {
            stderr += data;
        });

        childProcess.on('close', (code) => {
            if (code !== 0) {
                console.log("stderr: ", stderr);
                reject(new Error(`Script execution error: ${stderr}`));
            } else {
                resolve(stdout);
            }
        });
    });
}

async function runJsScript(eagle, scriptPath){
    const ctx = await createCtxString(eagle);
    const script = await fs.promises.readFile(scriptPath, "utf8");
    const result = await eval(`(async () => { const ctx = ${ctx}; ${script} })()`);
    return result;
}

module.exports = { executePythonScript, runJsScript, createCtxString };
