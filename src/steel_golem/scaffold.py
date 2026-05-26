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


def read_config() -> dict:
    """Load ~/.steel-golem/config.yaml.

    Returns
    -------
    dict
        Parsed config values.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist, with a message directing the user
        to run ``campaigns new`` first.
    """
    import yaml

    config_path = CONFIG_DIR / CONFIG_FILE_NAME
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. "
            "Run 'steel-golem campaigns new' first to create a campaign."
        )
    return yaml.safe_load(config_path.read_text())


ADVENTURE_SUBDIRS = [
    "villains",
    "npcs",
    "factions",
    "locations",
    "subplots",
    "handouts",
    "custom-monsters",
    "downtime-projects",
    "encounters/combat",
    "encounters/negotiations",
    "encounters/montages",
]


def create_adventure(name: str) -> Path:
    """Create a new adventure directory tree under the current campaign.

    Reads the campaign path from config, creates the adventure directory and
    subdirectories under ``<campaign_path>/adventures/<slug>/``, and writes
    an ``index.md`` with frontmatter. Sets ``current_adventure`` in the
    campaign ``index.md`` if it is currently ``null``.

    Parameters
    ----------
    name:
        Human-readable adventure name.

    Returns
    -------
    Path
        The adventure root directory.

    Raises
    ------
    FileNotFoundError
        If config is absent (raised by :func:`read_config`).
    FileExistsError
        If the adventure directory already exists.
    ValueError
        If *name* produces an empty slug.
    """
    config = read_config()
    campaign_path = Path(config["campaign_path"])
    slug = slugify(name)
    adventure_root = campaign_path / "adventures" / slug

    if adventure_root.exists():
        raise FileExistsError(
            f"Adventure directory already exists: {adventure_root}"
        )

    for subdir in ADVENTURE_SUBDIRS:
        (adventure_root / subdir).mkdir(parents=True, exist_ok=False)

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
    )
    index_path = adventure_root / "index.md"
    index_path.write_text(frontmatter.dumps(post))

    # Set current_adventure in campaign index.md only if it is currently null
    campaign_index_path = campaign_path / "index.md"
    campaign_post = frontmatter.load(str(campaign_index_path))
    if campaign_post.get("current_adventure") is None:
        campaign_post["current_adventure"] = slug
        campaign_index_path.write_text(frontmatter.dumps(campaign_post))

    return adventure_root


def set_adventure(slug: str) -> None:
    """Set the active adventure in the campaign index.md.

    Parameters
    ----------
    slug:
        The slug (directory name) of the adventure to activate.

    Raises
    ------
    FileNotFoundError
        If config is absent or if the adventure directory does not exist.
    """
    config = read_config()
    campaign_path = Path(config["campaign_path"])
    adventure_dir = campaign_path / "adventures" / slug

    if not adventure_dir.is_dir():
        raise FileNotFoundError(
            f"Adventure '{slug}' not found under {campaign_path / 'adventures'}. "
            "Check the slug and try again."
        )

    campaign_index_path = campaign_path / "index.md"
    campaign_post = frontmatter.load(str(campaign_index_path))
    campaign_post["current_adventure"] = slug
    campaign_index_path.write_text(frontmatter.dumps(campaign_post))


def list_adventures() -> list[dict]:
    """Return a list of adventures for the current campaign.

    Each entry is a dict with keys: ``slug``, ``name``, ``current`` (bool).

    Returns
    -------
    list[dict]
        Sorted by slug. Empty list if no adventures exist.

    Raises
    ------
    FileNotFoundError
        If config is absent (raised by :func:`read_config`).
    """
    config = read_config()
    campaign_path = Path(config["campaign_path"])
    adventures_dir = campaign_path / "adventures"

    campaign_post = frontmatter.load(str(campaign_path / "index.md"))
    current_adventure = campaign_post.get("current_adventure")

    adventures = []
    if adventures_dir.is_dir():
        for entry in sorted(adventures_dir.iterdir()):
            if not entry.is_dir():
                continue
            index_path = entry / "index.md"
            if not index_path.exists():
                continue
            adv_post = frontmatter.load(str(index_path))
            adventures.append(
                {
                    "slug": entry.name,
                    "name": adv_post.get("name", entry.name),
                    "current": entry.name == current_adventure,
                }
            )

    return adventures
