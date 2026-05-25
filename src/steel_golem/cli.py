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
@click.option("--name", required=True, help="Human-readable adventure name.")
def new(name: str) -> None:
    """Create a new adventure."""
    try:
        adventure_root = scaffold.create_adventure(name=name)
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    except (ValueError, FileExistsError) as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    click.echo(f"Created adventure '{name}' at {adventure_root}")


@adventures.command(name="set")
@click.argument("slug")
def set_(slug: str) -> None:
    """Set the active adventure to SLUG."""
    try:
        scaffold.set_adventure(slug=slug)
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    click.echo(f"Active adventure set to '{slug}'")


@adventures.command(name="list")
def list_() -> None:
    """List all adventures."""
    try:
        adventures_list = scaffold.list_adventures()
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)

    if not adventures_list:
        click.echo("No adventures found.")
        return

    # Determine column width for slug
    max_slug_len = max(len(a["slug"]) for a in adventures_list)

    for adv in adventures_list:
        marker = "*" if adv["current"] else " "
        click.echo(f"{marker} {adv['slug']:<{max_slug_len}}   {adv['name']}")
