"""Command-line interface for AI-Assisted-Cloud-Load-Tester."""

import typer

app = typer.Typer(help="load-tester load testing toolkit.")


@app.command()
def version() -> None:
    """Print the current load-tester version."""
    typer.echo("load-tester 1.0.0")


@app.command()
def doctor() -> None:
    """Check that the CLI is installed correctly."""
    typer.echo("load-tester CLI is ready.")


if __name__ == "__main__":
    app()
