import typer
from schug.cli import load

cli = typer.Typer()


@cli.callback()
def callback():
    """
    Welcome to the CLI
    """


cli.add_typer(load.app, name="load")
