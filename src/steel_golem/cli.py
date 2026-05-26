import sys
from pathlib import Path

import click

from steel_golem import scaffold
from steel_golem import entities


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


# ---------------------------------------------------------------------------
# Entity commands — shared options helper
# ---------------------------------------------------------------------------

_SCOPE_OPTIONS = [
    click.option("--description", default="", help="Director-facing summary."),
    click.option("--adventure", default=None, help="Write to this adventure slug instead of the active one."),
    click.option("--campaign", is_flag=True, default=False, help="Write to campaign scope instead of adventure scope."),
]


def _add_scope_options(func):
    """Decorator that adds --description, --adventure, and --campaign options."""
    for option in reversed(_SCOPE_OPTIONS):
        func = option(func)
    return func


def _entity_new_command(entity_type: str, create_fn):
    """Build a Click 'new' command for an entity type."""

    @click.option("--name", required=True, help=f"Human-readable {entity_type[:-1]} name.")
    @_add_scope_options
    def _new(name: str, description: str, adventure: str | None, campaign: bool) -> None:
        try:
            path = create_fn(
                name=name,
                description=description,
                adventure=adventure,
                campaign=campaign,
            )
        except (FileNotFoundError, ValueError) as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        except RuntimeError as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        except FileExistsError as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        click.echo(f"Created {entity_type[:-1]} '{name}' at {path}")

    _new.__doc__ = f"Create a new {entity_type[:-1]}."
    return _new


# ---------------------------------------------------------------------------
# npcs
# ---------------------------------------------------------------------------

@main.group()
def npcs():
    """Manage NPCs."""


npcs.command(name="new")(_entity_new_command("npcs", entities.create_npc))


# ---------------------------------------------------------------------------
# villains
# ---------------------------------------------------------------------------

@main.group()
def villains():
    """Manage villains."""


villains.command(name="new")(_entity_new_command("villains", entities.create_villain))


# ---------------------------------------------------------------------------
# locations
# ---------------------------------------------------------------------------

@main.group()
def locations():
    """Manage locations."""


locations.command(name="new")(_entity_new_command("locations", entities.create_location))


# ---------------------------------------------------------------------------
# factions
# ---------------------------------------------------------------------------

@main.group()
def factions():
    """Manage factions."""


factions.command(name="new")(_entity_new_command("factions", entities.create_faction))


# ---------------------------------------------------------------------------
# subplots — adventure-scoped only (no --campaign flag)
# ---------------------------------------------------------------------------

@main.group()
def subplots():
    """Manage subplots."""


@subplots.command(name="new")
@click.option("--name", required=True, help="Human-readable subplot name.")
@click.option("--description", default="", help="Director-facing summary.")
@click.option(
    "--adventure",
    default=None,
    help="Write to this adventure slug instead of the active one.",
)
@click.option(
    "--campaign",
    is_flag=True,
    default=False,
    hidden=True,
    help="(Not supported for subplots.)",
)
def subplots_new(
    name: str, description: str, adventure: str | None, campaign: bool
) -> None:
    """Create a new subplot."""
    try:
        path = entities.create_subplot(
            name=name,
            description=description,
            adventure=adventure,
            campaign=campaign,
        )
    except ValueError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    except (FileNotFoundError, FileExistsError) as exc:
        click.echo(f"Error: {exc}")
        sys.exit(1)
    click.echo(f"Created subplot '{name}' at {path}")


# ---------------------------------------------------------------------------
# handouts
# ---------------------------------------------------------------------------

@main.group()
def handouts():
    """Manage handouts."""


handouts.command(name="new")(_entity_new_command("handouts", entities.create_handout))


# ---------------------------------------------------------------------------
# items (notable items)
# ---------------------------------------------------------------------------

@main.group()
def items():
    """Manage notable items."""


items.command(name="new")(_entity_new_command("items", entities.create_item))


# ---------------------------------------------------------------------------
# downtime-projects
# ---------------------------------------------------------------------------

@main.group(name="downtime-projects")
def downtime_projects():
    """Manage downtime projects."""


downtime_projects.command(name="new")(
    _entity_new_command("downtime-projects", entities.create_downtime_project)
)


# ---------------------------------------------------------------------------
# encounters — adventure-scoped only (no --campaign flag)
# combat → encounters/combat/<slug>.md
# negotiation → encounters/negotiations/<slug>.md
# montage → encounters/montages/<slug>.md
# ---------------------------------------------------------------------------


def _encounter_new_command(encounter_type: str, create_fn):
    """Build a Click 'new' command for an encounter type (adventure-scoped only)."""

    @click.option("--name", required=True, help=f"Human-readable {encounter_type} encounter name.")
    @click.option("--description", default=None, help="Director-facing summary.")
    @click.option(
        "--adventure",
        default=None,
        help="Write to this adventure slug instead of the active one.",
    )
    def _new(name: str, description: str | None, adventure: str | None) -> None:
        try:
            path = create_fn(
                name=name,
                description=description,
                adventure_slug=adventure,
            )
        except (FileNotFoundError, ValueError) as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        except RuntimeError as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        except FileExistsError as exc:
            click.echo(f"Error: {exc}")
            sys.exit(1)
        click.echo(f"Created {encounter_type} encounter '{name}' at {path}")

    _new.__doc__ = f"Create a new {encounter_type} encounter."
    return _new


@main.group()
def encounters():
    """Manage encounters."""


@encounters.group()
def combat():
    """Manage combat encounters."""


combat.command(name="new")(_encounter_new_command("combat", entities.create_combat_encounter))


@encounters.group()
def negotiation():
    """Manage negotiation encounters."""


negotiation.command(name="new")(
    _encounter_new_command("negotiation", entities.create_negotiation_encounter)
)


@encounters.group()
def montage():
    """Manage montage encounters."""


montage.command(name="new")(
    _encounter_new_command("montage", entities.create_montage_encounter)
)
