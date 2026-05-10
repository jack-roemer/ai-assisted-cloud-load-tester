import typer

app = typer.Typer(help="load-tester load testing toolkit.")


@app.command()
def version() -> None:
    typer.echo("load-tester 1.0.0")


@app.command()
def doctor() -> None:
    typer.echo("load-tester CLI is ready.")


if __name__ == "__main__":
    app()
