import sys
from pathlib import Path

import click

from steel_golem import scaffold


@click.group()
def main():
    """Steel Golem — Director assistant for Draw Steel."""


@main.group()
def campaigns():
    """Manage campaigns."""


@campaigns.command()
@click.option("--name", required=True, help="Human-readable campaign name.")
@click.option(
    "--path",
    required=True,
    type=click.Path(file_okay=False, resolve_path=True),
    help="Parent directory in which the campaign root will be created.",
)
def new(name: str, path: str) -> None:
    """Create a new campaign."""
    parent = Path(path)
    try:
        campaign_root = scaffold.create_campaign(name=name, path=parent)
    except ValueError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    except FileExistsError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)

    scaffold.write_config(campaign_root)
    click.echo(f"Created campaign '{name}' at {campaign_root}")


@main.group()
def adventures():
    """Manage adventures."""


@adventures.command()
def new():
    """Create a new adventure."""


@adventures.command(name="set")
def set_():
    """Set the active adventure."""


@adventures.command(name="list")
def list_():
    """List all adventures."""
