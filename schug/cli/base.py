import typer
import uvicorn
from schug.config import settings

cli = typer.Typer()


@cli.callback()
def callback():
    """
    Welcome to the CLI
    """


@cli.command("serve")
def serve_app(reload: bool = typer.Option(False, "--reload")):
    """Start a dev server for the schug app"""
    typer.echo("Serving schug")
    app = "schug.main:app"
    uvicorn.run(app=app, host=settings.host, port=settings.port, reload=reload)
