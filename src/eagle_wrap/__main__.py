import json
import os
import time
import click
from eagle_wrap.api import librarySwitch
from .model import Library, SentOverCtx

@click.group()
def cli():
    pass

@cli.command()
@click.argument("path")
def lib(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        print(f"creating at {os.path.abspath(path)}")
        os.makedirs(path, exist_ok=True)

        assert os.path.isdir(path)

        if not os.path.exists(os.path.join(path, "tags.json")):
            with open(os.path.join(path, "tags.json"), "w") as f:
                f.write('{"historyTags": [], "starredTags": []}')

        if not os.path.exists(os.path.join(path, "saved-filters.json")):
            with open(os.path.join(path, "saved-filters.json"), "w") as f:
                f.write("[]")

        if not os.path.exists(os.path.join(path, "actions.json")):
            with open(os.path.join(path, "actions.json"), "w") as f:
                f.write("[]")

        if not os.path.exists(os.path.join(path, "mtime.json")):
            with open(os.path.join(path, "mtime.json"), "w") as f:
                f.write("{}")

        metadata = {
            "folders": [],
            "smartFolders": [],
            "quickAccess": [],
            "tagsGroups": [],
            "modificationTime": int(time.time() * 1000),
            "applicationVersion": "4.0.0",
        }

        if not os.path.exists(os.path.join(path, "metadata.json")):
            with open(os.path.join(path, "metadata.json"), "w") as f:
                json.dump(metadata, f)

    print(f"switching to {path}")
    librarySwitch(path)

@cli.command()
@click.argument("jsond")
@click.argument("path")
def pyscript(jsond, path : str):
    assert isinstance(jsond, str)
    assert isinstance(path, str)

    jsoncontent : dict = json.loads(jsond)
    assert "folders" in jsoncontent
    assert "items" in jsoncontent

    assert os.path.exists(path)
    assert path.endswith(".py")

    with open(path, "r") as f:
        script = f.read()

    import eagle_wrap as eagle_wrap

    eagle_wrap.CTX = SentOverCtx(**jsoncontent)
    eagle_wrap.INIT_LIB = Library.current()

    env = {
        "eagle" : eagle_wrap
    }
    exec(script, env)

if __name__ == "__main__":
    cli()


