import click


@click.group()
def main():
    """Steel Golem — Director assistant for Draw Steel."""


@main.group()
def campaigns():
    """Manage campaigns."""


@campaigns.command()
def new():
    """Create a new campaign."""


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
