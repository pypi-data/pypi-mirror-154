"""This module provides the CLI."""
# cli-module/cli.py


from typing import List, Optional
import typer
from polygon import rest_connect
app = typer.Typer()


@app.command()
def search(phrase: str = typer.Option("--phrase",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: search  results """
        f"""pass phrase to search""",
        fg=typer.colors.GREEN,
    )
    print(phrase)
    searchResult=rest_connect.search_details(phrase)
    print(searchResult)
#it is just one command now so taken care in the cli.py

if __name__ == "__main__":
    app()
