
import click

@click.group()
def main():
    pass

@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("ctx", type=str)
def script(path : str, ctx : str):
    from eaglewrap.bridge import executePythonScript, CtxModel
    ctx = CtxModel(ctx)
    executePythonScript(path, ctx)

