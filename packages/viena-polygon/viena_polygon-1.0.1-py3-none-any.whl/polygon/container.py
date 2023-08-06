"""This module provides the CLI."""
# cli-module/cli.py


from typing import List, Optional
from polygon import rest_connect

import typer

app = typer.Typer()


@app.command()
def list():
    typer.echo(f"list")
    #call the endpoint to get list of clod containers
    #rest-connect with the json
    datasetList=rest_connect.containerList()
    print(datasetList)


@app.command()
def add(name: str):
    typer.echo(f"add: {name}")


@app.command()
def delete(name: str):
    typer.echo(f"delete: {name}")


@app.command()
def details(name: str):
    typer.echo(f"details: {name}")


if __name__ == "__main__":
    app()
