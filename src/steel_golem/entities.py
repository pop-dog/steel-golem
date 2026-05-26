"""Entity creation — NPC, Villain, Location, Faction, Subplot, Handout, Item, Downtime Project."""
import datetime
from pathlib import Path

import frontmatter

from steel_golem.scaffold import slugify, read_config


def _resolve_scope_dir(
    entity_type: str,
    adventure: str | None,
    campaign: bool,
) -> tuple[Path, str]:
    """Return (target_directory, scope_value) for the given scope flags.

    Parameters
    ----------
    entity_type:
        Subdirectory name, e.g. ``"npcs"``, ``"villains"``, ``"locations"``,
        ``"factions"``.
    adventure:
        Explicit adventure slug, or ``None``.
    campaign:
        If ``True``, use campaign-level scope.

    Returns
    -------
    tuple[Path, str]
        ``(target_dir, scope)`` where *scope* is ``"adventure"`` or
        ``"campaign"``.

    Raises
    ------
    FileNotFoundError
        If config is absent (raised by :func:`read_config`).
    RuntimeError
        If no scope flag is given and ``current_adventure`` is ``null`` in the
        campaign ``index.md``.
    """
    config = read_config()
    campaign_path = Path(config["campaign_path"])

    if campaign:
        return campaign_path / entity_type, "campaign"

    if adventure is not None:
        return campaign_path / "adventures" / adventure / entity_type, "adventure"

    # Default: active adventure
    campaign_post = frontmatter.load(str(campaign_path / "index.md"))
    current_adventure = campaign_post.get("current_adventure")
    if not current_adventure:
        raise RuntimeError(
            "No active adventure. Run 'steel-golem adventures set <slug>' first."
        )
    return campaign_path / "adventures" / current_adventure / entity_type, "adventure"


def create_npc(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new NPC file.

    Parameters
    ----------
    name:
        Human-readable NPC name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``npcs/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the NPC file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("npcs", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"NPC file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        description=description,
        faction=None,
        location=None,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_villain(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Villain file.

    Parameters
    ----------
    name:
        Human-readable villain name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``villains/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Villain file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("villains", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Villain file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        description=description,
        location=None,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_location(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Location file.

    Parameters
    ----------
    name:
        Human-readable location name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``locations/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Location file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("locations", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Location file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        description=description,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_faction(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Faction file.

    Parameters
    ----------
    name:
        Human-readable faction name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``factions/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Faction file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("factions", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Faction file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        description=description,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_subplot(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Subplot file.

    Subplots are Adventure-scoped only. Passing ``campaign=True`` raises
    :exc:`ValueError`.

    Parameters
    ----------
    name:
        Human-readable subplot name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        Must be ``False``; subplots cannot be campaign-scoped.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    ValueError
        If ``campaign=True`` is passed, or if *name* produces an empty slug.
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Subplot file already exists.
    """
    if campaign:
        raise ValueError(
            "Subplots are Adventure-scoped only; the --campaign flag is not supported."
        )

    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("subplots", adventure, False)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Subplot file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        plot=None,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_handout(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Handout file.

    Parameters
    ----------
    name:
        Human-readable handout name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``handouts/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Handout file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("handouts", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Handout file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        revealed=False,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_item(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Notable Item file.

    Parameters
    ----------
    name:
        Human-readable item name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``items/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Item file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("items", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Item file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        owner=None,
        location=None,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def _resolve_encounter_dir(encounter_subdir: str, adventure_slug: str | None) -> Path:
    """Return the target directory for an encounter entity.

    Encounters are always adventure-scoped. Resolves to
    ``<campaign>/adventures/<slug>/encounters/<subdir>/``.

    Parameters
    ----------
    encounter_subdir:
        One of ``"combat"``, ``"negotiations"``, ``"montages"``.
    adventure_slug:
        Explicit adventure slug, or ``None`` to use the active adventure.

    Returns
    -------
    Path
        The target directory.

    Raises
    ------
    FileNotFoundError
        If config is absent, or if an explicit *adventure_slug* directory does
        not exist.
    RuntimeError
        If *adventure_slug* is ``None`` and no adventure is currently active.
    """
    config = read_config()
    campaign_path = Path(config["campaign_path"])

    if adventure_slug is not None:
        adv_dir = campaign_path / "adventures" / adventure_slug
        if not adv_dir.is_dir():
            raise FileNotFoundError(
                f"Adventure '{adventure_slug}' not found under "
                f"{campaign_path / 'adventures'}. Check the slug and try again."
            )
        return adv_dir / "encounters" / encounter_subdir

    # Default: active adventure
    campaign_post = frontmatter.load(str(campaign_path / "index.md"))
    current_adventure = campaign_post.get("current_adventure")
    if not current_adventure:
        raise RuntimeError(
            "No active adventure. Run 'steel-golem adventures set <slug>' first."
        )
    return campaign_path / "adventures" / current_adventure / "encounters" / encounter_subdir


def create_combat_encounter(
    name: str,
    description: str | None = None,
    adventure_slug: str | None = None,
) -> Path:
    """Create a new Combat Encounter file.

    Parameters
    ----------
    name:
        Human-readable encounter name.
    description:
        Optional director-facing summary (default ``None``).
    adventure_slug:
        Explicit adventure slug to write into (overrides active adventure).

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent, or the named adventure does not exist.
    RuntimeError
        If no adventure is active and *adventure_slug* is not given.
    FileExistsError
        If the encounter file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir = _resolve_encounter_dir("combat", adventure_slug)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Combat encounter file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        objective=None,
        monsters=[],
        location=None,
        villain=None,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_negotiation_encounter(
    name: str,
    description: str | None = None,
    adventure_slug: str | None = None,
) -> Path:
    """Create a new Negotiation Encounter file.

    Parameters
    ----------
    name:
        Human-readable encounter name.
    description:
        Optional director-facing summary (default ``None``).
    adventure_slug:
        Explicit adventure slug to write into (overrides active adventure).

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent, or the named adventure does not exist.
    RuntimeError
        If no adventure is active and *adventure_slug* is not given.
    FileExistsError
        If the encounter file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir = _resolve_encounter_dir("negotiations", adventure_slug)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Negotiation encounter file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        patience=None,
        interest=None,
        motivations=[],
        pitfalls=[],
        npc=None,
        location=None,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_montage_encounter(
    name: str,
    description: str | None = None,
    adventure_slug: str | None = None,
) -> Path:
    """Create a new Montage Encounter file.

    Parameters
    ----------
    name:
        Human-readable encounter name.
    description:
        Optional director-facing summary (default ``None``).
    adventure_slug:
        Explicit adventure slug to write into (overrides active adventure).

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent, or the named adventure does not exist.
    RuntimeError
        If no adventure is active and *adventure_slug* is not given.
    FileExistsError
        If the encounter file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir = _resolve_encounter_dir("montages", adventure_slug)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Montage encounter file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        goal=None,
        tests=[],
        success_threshold=None,
        location=None,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path


def create_downtime_project(
    name: str,
    description: str = "",
    adventure: str | None = None,
    campaign: bool = False,
) -> Path:
    """Create a new Downtime Project file.

    Parameters
    ----------
    name:
        Human-readable downtime project name.
    description:
        Optional director-facing summary (default ``""``).
    adventure:
        Explicit adventure slug to write into (overrides active adventure).
    campaign:
        If ``True``, write to campaign-level ``downtime-projects/`` directory.

    Returns
    -------
    Path
        Path to the created ``.md`` file.

    Raises
    ------
    FileNotFoundError
        If config is absent.
    RuntimeError
        If no adventure is active and no scope flag is given.
    FileExistsError
        If the Downtime Project file already exists.
    ValueError
        If *name* produces an empty slug.
    """
    slug = slugify(name)
    target_dir, scope = _resolve_scope_dir("downtime-projects", adventure, campaign)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{slug}.md"

    if target_path.exists():
        raise FileExistsError(f"Downtime Project file already exists: {target_path}")

    post = frontmatter.Post(
        content="",
        name=name,
        slug=slug,
        created=datetime.date.today(),
        description=description,
        hero=None,
        project_goal=None,
        project_points=0,
        scope=scope,
    )
    target_path.write_text(frontmatter.dumps(post))
    return target_path
