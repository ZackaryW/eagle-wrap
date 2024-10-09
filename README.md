# eagle-wrap
wrapper for eagle.cool

## install
```
pip install eagle-wrap
```

## features
- `api wrapper` provides eagle api methods in `api.py` from https://api.eagle.cool/
- `cli` offers a command-line interface to bridge plugins into a Python environment

## plugin bridging
use

```bash
eaglewrap pyscript [ctx] [script path]
```

to create the ctx, use or adapt the following snippet in your plugin
```js
async function stringifyEagleContext(eagle) {
    const ctx = {};
    // await for eagle.item.getSelected();
    ctx.items = [];
    for (const item of await eagle.item.getSelected()) {
        ctx.item.push(item.id);
    }

    ctx.folders = [];
    for (const folder of await eagle.folder.getSelected()){
        ctx.folders.push(folder.id);
    }

    return JSON.stringify(ctx);
}
```
