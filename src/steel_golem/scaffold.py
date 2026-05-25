"""Campaign scaffolding — directory creation, index.md, and config writing."""
import datetime
import re
from pathlib import Path

import frontmatter

CONFIG_DIR = Path.home() / ".steel-golem"
CONFIG_FILE_NAME = "config.yaml"

CAMPAIGN_SUBDIRS = [
    "heroes",
    "villains",
    "npcs",
    "factions",
    "locations",
    "plots",
    "items",
    "lore",
    "sessions",
    "downtime-projects",
    "adventures",
]


def slugify(name: str) -> str:
    """Convert a campaign name to a URL-safe slug.

    Rules:
    - Lowercase
    - Spaces and underscores become hyphens
    - Non-alphanumeric characters (other than hyphens) are stripped
    - Consecutive hyphens are collapsed to one
    - Leading and trailing hyphens are stripped
    - An empty result raises ValueError
    """
    slug = name.lower()
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")
    if not slug:
        raise ValueError(f"Cannot derive a valid slug from name: {name!r}")
    return slug


def create_campaign(name: str, path: Path) -> Path:
    """Create the campaign directory tree and index.md under *path/<slug>/*.

    Parameters
    ----------
    name:
        Human-readable campaign name.
    path:
        Parent directory under which the campaign root will be created.

    Returns
    -------
    Path
        The campaign root directory (``path / slug``).

    Raises
    ------
    ValueError
        If *name* produces an empty slug.
    FileExistsError
        If the campaign directory already exists.
    """
    slug = slugify(name)  # raises ValueError if slug is empty
    campaign_root = Path(path) / slug

    if campaign_root.exists():
        raise FileExistsError(
            f"Campaign directory already exists: {campaign_root}"
        )

    # Create subdirectories (no stub files, no .gitkeep)
    for subdir in CAMPAIGN_SUBDIRS:
        (campaign_root / subdir).mkdir(parents=True, exist_ok=False)

    # Write index.md with frontmatter
    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        status="active",
        current_adventure=None,
    )
    index_path = campaign_root / "index.md"
    index_path.write_text(frontmatter.dumps(post))

    return campaign_root


def write_config(campaign_root: Path) -> None:
    """Create (or overwrite) ~/.steel-golem/config.yaml with the campaign path.

    Parameters
    ----------
    campaign_root:
        Absolute path to the campaign root directory.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config_path = CONFIG_DIR / CONFIG_FILE_NAME
    config_path.write_text(f"campaign_path: {campaign_root.resolve()}\n")
