"""Tests for entities.py — NPC, Villain, Location, Faction creation."""
import datetime
from pathlib import Path
from unittest.mock import patch

import frontmatter
import pytest
from click.testing import CliRunner

from steel_golem.cli import main
from steel_golem.scaffold import create_campaign, create_adventure
from steel_golem.entities import (
    create_npc,
    create_villain,
    create_location,
    create_faction,
    create_subplot,
    create_handout,
    create_item,
    create_downtime_project,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_campaign(tmp_path):
    """Create a minimal campaign + config; return (campaign_root, fake_config_dir)."""
    fake_config_dir = tmp_path / ".steel-golem"
    campaign_root = create_campaign(name="Iron Throne", path=tmp_path)
    fake_config_dir.mkdir(parents=True, exist_ok=True)
    (fake_config_dir / "config.yaml").write_text(
        f"campaign_path: {campaign_root}\n"
    )
    return campaign_root, fake_config_dir


def _make_campaign_with_adventure(tmp_path):
    """Create campaign + one active adventure; return (campaign_root, adv_root, fake_config_dir)."""
    campaign_root, fake_config_dir = _make_campaign(tmp_path)
    with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
        adv_root = create_adventure(name="The Sunken Vault")
    return campaign_root, adv_root, fake_config_dir


# ---------------------------------------------------------------------------
# create_npc — unit tests
# ---------------------------------------------------------------------------


class TestCreateNpc:
    def test_happy_path_creates_file_in_active_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                result = create_npc(name="Mira the Innkeeper")
        expected = adv_root / "npcs" / "mira-the-innkeeper.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["name"] == "Mira the Innkeeper"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["slug"] == "mira-the-innkeeper"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["description"] == ""

    def test_frontmatter_description_custom(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper", description="Friendly innkeeper at the Rusty Flagon.")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["description"] == "Friendly innkeeper at the Rusty Flagon."

    def test_frontmatter_faction_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["faction"] is None

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["location"] is None

    def test_frontmatter_scope_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
        post = frontmatter.load(str(adv_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["scope"] == "adventure"

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_npc(name="Mira the Innkeeper")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_npc(name="Mira the Innkeeper")
                with pytest.raises(FileExistsError):
                    create_npc(name="Mira the Innkeeper")

    def test_adventure_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_adventure(name="Second Arc")
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                result = create_npc(name="Mira the Innkeeper", adventure="second-arc")
        expected = campaign_root / "adventures" / "second-arc" / "npcs" / "mira-the-innkeeper.md"
        assert result == expected
        assert expected.is_file()

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_npc(name="Mira the Innkeeper", campaign=True)
        expected = campaign_root / "npcs" / "mira-the-innkeeper.md"
        assert result == expected
        assert expected.is_file()

    def test_campaign_scope_sets_scope_field(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_npc(name="Mira the Innkeeper", campaign=True)
        post = frontmatter.load(str(campaign_root / "npcs" / "mira-the-innkeeper.md"))
        assert post["scope"] == "campaign"


# ---------------------------------------------------------------------------
# create_villain — unit tests
# ---------------------------------------------------------------------------


class TestCreateVillain:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_villain(name="The Warden")
        expected = adv_root / "villains" / "the-warden.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert post["name"] == "The Warden"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert post["slug"] == "the-warden"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert post["description"] == ""

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert post["location"] is None

    def test_frontmatter_scope_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert post["scope"] == "adventure"

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_villain(name="The Warden")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
            with pytest.raises(FileExistsError):
                create_villain(name="The Warden")

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_villain(name="The Warden", campaign=True)
        expected = campaign_root / "villains" / "the-warden.md"
        assert result == expected
        assert expected.is_file()

    def test_villain_has_no_faction_field(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_villain(name="The Warden")
        post = frontmatter.load(str(adv_root / "villains" / "the-warden.md"))
        assert "faction" not in post


# ---------------------------------------------------------------------------
# create_location — unit tests
# ---------------------------------------------------------------------------


class TestCreateLocation:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_location(name="The Sunken Archive")
        expected = adv_root / "locations" / "the-sunken-archive.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
        post = frontmatter.load(str(adv_root / "locations" / "the-sunken-archive.md"))
        assert post["name"] == "The Sunken Archive"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
        post = frontmatter.load(str(adv_root / "locations" / "the-sunken-archive.md"))
        assert post["slug"] == "the-sunken-archive"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
        post = frontmatter.load(str(adv_root / "locations" / "the-sunken-archive.md"))
        assert post["description"] == ""

    def test_frontmatter_scope_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
        post = frontmatter.load(str(adv_root / "locations" / "the-sunken-archive.md"))
        assert post["scope"] == "adventure"

    def test_location_has_no_faction_or_location_fields(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
        post = frontmatter.load(str(adv_root / "locations" / "the-sunken-archive.md"))
        assert "faction" not in post
        assert "location" not in post

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_location(name="The Sunken Archive")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_location(name="The Sunken Archive")
            with pytest.raises(FileExistsError):
                create_location(name="The Sunken Archive")

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_location(name="The Sunken Archive", campaign=True)
        expected = campaign_root / "locations" / "the-sunken-archive.md"
        assert result == expected
        assert expected.is_file()

    def test_adventure_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_adventure(name="Second Arc")
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                result = create_location(name="The Sunken Archive", adventure="second-arc")
        expected = campaign_root / "adventures" / "second-arc" / "locations" / "the-sunken-archive.md"
        assert result == expected
        assert expected.is_file()


# ---------------------------------------------------------------------------
# create_faction — unit tests
# ---------------------------------------------------------------------------


class TestCreateFaction:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_faction(name="The Iron Covenant")
        expected = adv_root / "factions" / "the-iron-covenant.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["name"] == "The Iron Covenant"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["slug"] == "the-iron-covenant"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["description"] == ""

    def test_frontmatter_scope_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["scope"] == "adventure"

    def test_faction_has_no_relationship_fields(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert "faction" not in post
        assert "location" not in post

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_faction(name="The Iron Covenant")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant")
            with pytest.raises(FileExistsError):
                create_faction(name="The Iron Covenant")

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_faction(name="The Iron Covenant", campaign=True)
        expected = campaign_root / "factions" / "the-iron-covenant.md"
        assert result == expected
        assert expected.is_file()

    def test_description_custom(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_faction(name="The Iron Covenant", description="Ancient order of mercenaries.")
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["description"] == "Ancient order of mercenaries."


# ---------------------------------------------------------------------------
# CLI integration tests — npcs
# ---------------------------------------------------------------------------


class TestNpcsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["npcs", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["npcs", "new", "--name", "Mira the Innkeeper"])
        assert result.exit_code == 0, result.output
        assert (adv_root / "npcs" / "mira-the-innkeeper.md").is_file()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["npcs", "new", "--name", "Mira the Innkeeper"])
        assert "Mira the Innkeeper" in result.output

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["npcs", "new", "--name", "Mira"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_existing_file_exits_nonzero(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["npcs", "new", "--name", "Mira the Innkeeper"])
            result = runner.invoke(main, ["npcs", "new", "--name", "Mira the Innkeeper"])
        assert result.exit_code != 0

    def test_campaign_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["npcs", "new", "--name", "Mira", "--campaign"])
        assert result.exit_code == 0, result.output
        assert (campaign_root / "npcs" / "mira.md").is_file()

    def test_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
                create_adventure(name="Second Arc")
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["npcs", "new", "--name", "Mira", "--adventure", "second-arc"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "adventures" / "second-arc" / "npcs" / "mira.md").is_file()


# ---------------------------------------------------------------------------
# CLI integration tests — villains
# ---------------------------------------------------------------------------


class TestVillainsNewCLI:
    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["villains", "new", "--name", "The Warden"])
        assert result.exit_code == 0, result.output
        assert (adv_root / "villains" / "the-warden.md").is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["villains", "new", "--name", "The Warden"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_campaign_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["villains", "new", "--name", "The Warden", "--campaign"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "villains" / "the-warden.md").is_file()


# ---------------------------------------------------------------------------
# CLI integration tests — locations
# ---------------------------------------------------------------------------


class TestLocationsNewCLI:
    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["locations", "new", "--name", "The Sunken Archive"])
        assert result.exit_code == 0, result.output
        assert (adv_root / "locations" / "the-sunken-archive.md").is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["locations", "new", "--name", "The Archive"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_campaign_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["locations", "new", "--name", "The Archive", "--campaign"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "locations" / "the-archive.md").is_file()


# ---------------------------------------------------------------------------
# CLI integration tests — factions
# ---------------------------------------------------------------------------


class TestFactionsNewCLI:
    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["factions", "new", "--name", "The Iron Covenant"])
        assert result.exit_code == 0, result.output
        assert (adv_root / "factions" / "the-iron-covenant.md").is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["factions", "new", "--name", "The Iron Covenant"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_campaign_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["factions", "new", "--name", "The Iron Covenant", "--campaign"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "factions" / "the-iron-covenant.md").is_file()

    def test_description_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["factions", "new", "--name", "The Iron Covenant", "--description", "Ancient order."],
            )
        assert result.exit_code == 0, result.output
        post = frontmatter.load(str(adv_root / "factions" / "the-iron-covenant.md"))
        assert post["description"] == "Ancient order."


# ---------------------------------------------------------------------------
# create_subplot — unit tests
# ---------------------------------------------------------------------------


class TestCreateSubplot:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_subplot(name="The Missing Courier")
        expected = adv_root / "subplots" / "the-missing-courier.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["name"] == "The Missing Courier"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["slug"] == "the-missing-courier"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["description"] == ""

    def test_frontmatter_description_custom(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier", description="A courier goes missing.")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["description"] == "A courier goes missing."

    def test_frontmatter_plot_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["plot"] is None

    def test_frontmatter_scope_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert post["scope"] == "adventure"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
        post = frontmatter.load(str(adv_root / "subplots" / "the-missing-courier.md"))
        assert isinstance(post["created"], datetime.date)

    def test_campaign_flag_raises_value_error(self, tmp_path):
        """Subplots are adventure-scoped only; --campaign must raise ValueError."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(ValueError, match="campaign"):
                create_subplot(name="The Missing Courier", campaign=True)

    def test_named_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
            result = create_subplot(name="The Missing Courier", adventure="second-arc")
        expected = campaign_root / "adventures" / "second-arc" / "subplots" / "the-missing-courier.md"
        assert result == expected
        assert expected.is_file()

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_subplot(name="The Missing Courier")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_subplot(name="The Missing Courier")
            with pytest.raises(FileExistsError):
                create_subplot(name="The Missing Courier")


# ---------------------------------------------------------------------------
# create_handout — unit tests
# ---------------------------------------------------------------------------


class TestCreateHandout:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_handout(name="The Warden's Letter")
        expected = adv_root / "handouts" / "the-wardens-letter.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["name"] == "The Warden's Letter"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["slug"] == "the-wardens-letter"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["description"] == ""

    def test_frontmatter_revealed_always_false(self, tmp_path):
        """revealed must be boolean False, never None."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["revealed"] is False
        assert post["revealed"] is not None

    def test_frontmatter_scope_adventure_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["scope"] == "adventure"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert isinstance(post["created"], datetime.date)

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_handout(name="The Warden's Letter", campaign=True)
        expected = campaign_root / "handouts" / "the-wardens-letter.md"
        assert result == expected
        assert expected.is_file()
        post = frontmatter.load(str(expected))
        assert post["scope"] == "campaign"

    def test_named_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
            result = create_handout(name="The Warden's Letter", adventure="second-arc")
        expected = campaign_root / "adventures" / "second-arc" / "handouts" / "the-wardens-letter.md"
        assert result == expected
        assert expected.is_file()

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_handout(name="The Warden's Letter")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_handout(name="The Warden's Letter")
            with pytest.raises(FileExistsError):
                create_handout(name="The Warden's Letter")


# ---------------------------------------------------------------------------
# create_item — unit tests
# ---------------------------------------------------------------------------


class TestCreateItem:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_item(name="The Obsidian Key")
        expected = adv_root / "items" / "the-obsidian-key.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["name"] == "The Obsidian Key"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["slug"] == "the-obsidian-key"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["description"] == ""

    def test_frontmatter_owner_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["owner"] is None

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["location"] is None

    def test_frontmatter_scope_adventure_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["scope"] == "adventure"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert isinstance(post["created"], datetime.date)

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_item(name="The Obsidian Key", campaign=True)
        expected = campaign_root / "items" / "the-obsidian-key.md"
        assert result == expected
        assert expected.is_file()
        post = frontmatter.load(str(expected))
        assert post["scope"] == "campaign"

    def test_named_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
            result = create_item(name="The Obsidian Key", adventure="second-arc")
        expected = campaign_root / "adventures" / "second-arc" / "items" / "the-obsidian-key.md"
        assert result == expected
        assert expected.is_file()

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_item(name="The Obsidian Key")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_item(name="The Obsidian Key")
            with pytest.raises(FileExistsError):
                create_item(name="The Obsidian Key")


# ---------------------------------------------------------------------------
# create_downtime_project — unit tests
# ---------------------------------------------------------------------------


class TestCreateDowntimeProject:
    def test_happy_path_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_downtime_project(name="Decipher the Vault Inscription")
        expected = adv_root / "downtime-projects" / "decipher-the-vault-inscription.md"
        assert expected.is_file()
        assert result == expected

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["name"] == "Decipher the Vault Inscription"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["slug"] == "decipher-the-vault-inscription"

    def test_frontmatter_description_default_empty(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["description"] == ""

    def test_frontmatter_hero_null(self, tmp_path):
        """hero must be null at creation (Unowned)."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["hero"] is None

    def test_frontmatter_project_goal_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["project_goal"] is None

    def test_frontmatter_project_points_zero(self, tmp_path):
        """project_points must always start at 0."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["project_points"] == 0

    def test_frontmatter_scope_adventure_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["scope"] == "adventure"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert isinstance(post["created"], datetime.date)

    def test_campaign_scope_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_downtime_project(name="Decipher the Vault Inscription", campaign=True)
        expected = campaign_root / "downtime-projects" / "decipher-the-vault-inscription.md"
        assert result == expected
        assert expected.is_file()
        post = frontmatter.load(str(expected))
        assert post["scope"] == "campaign"

    def test_named_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
            result = create_downtime_project(
                name="Decipher the Vault Inscription", adventure="second-arc"
            )
        expected = (
            campaign_root
            / "adventures"
            / "second-arc"
            / "downtime-projects"
            / "decipher-the-vault-inscription.md"
        )
        assert result == expected
        assert expected.is_file()

    def test_no_active_adventure_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_downtime_project(name="Decipher the Vault Inscription")

    def test_existing_file_raises(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_downtime_project(name="Decipher the Vault Inscription")
            with pytest.raises(FileExistsError):
                create_downtime_project(name="Decipher the Vault Inscription")


# ---------------------------------------------------------------------------
# CLI integration tests — subplots new
# ---------------------------------------------------------------------------


class TestSubplotsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["subplots", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["subplots", "new", "--name", "The Missing Courier"]
            )
        assert result.exit_code == 0, result.output
        assert (adv_root / "subplots" / "the-missing-courier.md").is_file()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["subplots", "new", "--name", "The Missing Courier"]
            )
        assert "The Missing Courier" in result.output

    def test_campaign_flag_exits_nonzero(self, tmp_path):
        """--campaign is not valid for subplots."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["subplots", "new", "--name", "The Missing Courier", "--campaign"]
            )
        assert result.exit_code != 0

    def test_adventure_flag_targets_named_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["subplots", "new", "--name", "The Missing Courier", "--adventure", "second-arc"],
            )
        assert result.exit_code == 0, result.output
        assert (
            campaign_root / "adventures" / "second-arc" / "subplots" / "the-missing-courier.md"
        ).is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["subplots", "new", "--name", "Test"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_duplicate_exits_nonzero(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["subplots", "new", "--name", "The Missing Courier"])
            result = runner.invoke(
                main, ["subplots", "new", "--name", "The Missing Courier"]
            )
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# CLI integration tests — handouts new
# ---------------------------------------------------------------------------


class TestHandoutsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["handouts", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["handouts", "new", "--name", "The Warden's Letter"]
            )
        assert result.exit_code == 0, result.output
        assert (adv_root / "handouts" / "the-wardens-letter.md").is_file()

    def test_revealed_false_in_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["handouts", "new", "--name", "The Warden's Letter"])
        post = frontmatter.load(str(adv_root / "handouts" / "the-wardens-letter.md"))
        assert post["revealed"] is False

    def test_campaign_flag_creates_campaign_scoped_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["handouts", "new", "--name", "The Warden's Letter", "--campaign"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "handouts" / "the-wardens-letter.md").is_file()

    def test_adventure_flag_targets_named_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["handouts", "new", "--name", "The Warden's Letter", "--adventure", "second-arc"],
            )
        assert result.exit_code == 0, result.output
        assert (
            campaign_root / "adventures" / "second-arc" / "handouts" / "the-wardens-letter.md"
        ).is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["handouts", "new", "--name", "Test"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output


# ---------------------------------------------------------------------------
# CLI integration tests — items new
# ---------------------------------------------------------------------------


class TestItemsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["items", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["items", "new", "--name", "The Obsidian Key"]
            )
        assert result.exit_code == 0, result.output
        assert (adv_root / "items" / "the-obsidian-key.md").is_file()

    def test_campaign_flag_creates_campaign_scoped_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["items", "new", "--name", "The Obsidian Key", "--campaign"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "items" / "the-obsidian-key.md").is_file()

    def test_adventure_flag_targets_named_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["items", "new", "--name", "The Obsidian Key", "--adventure", "second-arc"],
            )
        assert result.exit_code == 0, result.output
        assert (
            campaign_root / "adventures" / "second-arc" / "items" / "the-obsidian-key.md"
        ).is_file()

    def test_owner_and_location_null_in_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["items", "new", "--name", "The Obsidian Key"])
        post = frontmatter.load(str(adv_root / "items" / "the-obsidian-key.md"))
        assert post["owner"] is None
        assert post["location"] is None

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["items", "new", "--name", "Test"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output


# ---------------------------------------------------------------------------
# CLI integration tests — downtime-projects new
# ---------------------------------------------------------------------------


class TestDowntimeProjectsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["downtime-projects", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["downtime-projects", "new", "--name", "Decipher the Vault Inscription"],
            )
        assert result.exit_code == 0, result.output
        assert (
            adv_root / "downtime-projects" / "decipher-the-vault-inscription.md"
        ).is_file()

    def test_hero_null_and_project_points_zero_in_file(self, tmp_path):
        """hero must be null and project_points must be 0 at creation."""
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["downtime-projects", "new", "--name", "Decipher the Vault Inscription"],
            )
        post = frontmatter.load(
            str(adv_root / "downtime-projects" / "decipher-the-vault-inscription.md")
        )
        assert post["hero"] is None
        assert post["project_points"] == 0

    def test_campaign_flag_creates_campaign_scoped_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                [
                    "downtime-projects",
                    "new",
                    "--name",
                    "Decipher the Vault Inscription",
                    "--campaign",
                ],
            )
        assert result.exit_code == 0, result.output
        assert (
            campaign_root / "downtime-projects" / "decipher-the-vault-inscription.md"
        ).is_file()

    def test_adventure_flag_targets_named_adventure(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Arc")
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                [
                    "downtime-projects",
                    "new",
                    "--name",
                    "Decipher the Vault Inscription",
                    "--adventure",
                    "second-arc",
                ],
            )
        assert result.exit_code == 0, result.output
        assert (
            campaign_root
            / "adventures"
            / "second-arc"
            / "downtime-projects"
            / "decipher-the-vault-inscription.md"
        ).is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["downtime-projects", "new", "--name", "Test"])
        assert result.exit_code != 0
        assert "No active adventure" in result.output


# ---------------------------------------------------------------------------
# create_combat_encounter — unit tests
# ---------------------------------------------------------------------------


from steel_golem.entities import (
    create_combat_encounter,
    create_negotiation_encounter,
    create_montage_encounter,
)


class TestCreateCombatEncounter:
    def test_creates_file_at_expected_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        assert path == adv_root / "encounters" / "combat" / "throne-room-battle.md"
        assert path.is_file()

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["name"] == "Throne Room Battle"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["slug"] == "throne-room-battle"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert isinstance(post["created"], datetime.date)

    def test_frontmatter_description_default_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["description"] is None

    def test_frontmatter_description_set(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle", description="A fierce battle.")
        post = frontmatter.load(str(path))
        assert post["description"] == "A fierce battle."

    def test_frontmatter_objective_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["objective"] is None

    def test_frontmatter_monsters_empty_list(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["monsters"] == []

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["location"] is None

    def test_frontmatter_villain_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        post = frontmatter.load(str(path))
        assert post["villain"] is None

    def test_uses_active_adventure_by_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_combat_encounter(name="Throne Room Battle")
        assert adv_root in path.parents

    def test_targets_specific_adventure_with_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            path = create_combat_encounter(
                name="Throne Room Battle", adventure_slug="second-adventure"
            )
        assert "second-adventure" in str(path)

    def test_raises_if_no_active_adventure(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_combat_encounter(name="Throne Room Battle")

    def test_raises_if_adventure_slug_not_found(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError, match="no-such-adventure"):
                create_combat_encounter(
                    name="Throne Room Battle", adventure_slug="no-such-adventure"
                )

    def test_raises_if_file_already_exists(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_combat_encounter(name="Throne Room Battle")
            with pytest.raises(FileExistsError):
                create_combat_encounter(name="Throne Room Battle")

    def test_returns_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_combat_encounter(name="Throne Room Battle")
        assert isinstance(result, Path)

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                create_combat_encounter(name="Throne Room Battle")


# ---------------------------------------------------------------------------
# create_negotiation_encounter — unit tests
# ---------------------------------------------------------------------------


class TestCreateNegotiationEncounter:
    def test_creates_file_at_expected_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        expected = adv_root / "encounters" / "negotiations" / "bargaining-with-the-harbormaster.md"
        assert path == expected
        assert path.is_file()

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["name"] == "Bargaining with the Harbormaster"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["slug"] == "bargaining-with-the-harbormaster"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert isinstance(post["created"], datetime.date)

    def test_frontmatter_description_default_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["description"] is None

    def test_frontmatter_description_set(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(
                name="Bargaining with the Harbormaster", description="Trade deal."
            )
        post = frontmatter.load(str(path))
        assert post["description"] == "Trade deal."

    def test_frontmatter_patience_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["patience"] is None

    def test_frontmatter_interest_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["interest"] is None

    def test_frontmatter_motivations_empty_list(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["motivations"] == []

    def test_frontmatter_pitfalls_empty_list(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["pitfalls"] == []

    def test_frontmatter_npc_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["npc"] is None

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        post = frontmatter.load(str(path))
        assert post["location"] is None

    def test_uses_active_adventure_by_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        assert adv_root in path.parents

    def test_targets_specific_adventure_with_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            path = create_negotiation_encounter(
                name="Bargaining with the Harbormaster", adventure_slug="second-adventure"
            )
        assert "second-adventure" in str(path)

    def test_raises_if_no_active_adventure(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_negotiation_encounter(name="Bargaining with the Harbormaster")

    def test_raises_if_adventure_slug_not_found(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError, match="no-such-adventure"):
                create_negotiation_encounter(
                    name="Bargaining with the Harbormaster", adventure_slug="no-such-adventure"
                )

    def test_raises_if_file_already_exists(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_negotiation_encounter(name="Bargaining with the Harbormaster")
            with pytest.raises(FileExistsError):
                create_negotiation_encounter(name="Bargaining with the Harbormaster")

    def test_returns_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_negotiation_encounter(name="Bargaining with the Harbormaster")
        assert isinstance(result, Path)

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                create_negotiation_encounter(name="Bargaining with the Harbormaster")


# ---------------------------------------------------------------------------
# create_montage_encounter — unit tests
# ---------------------------------------------------------------------------


class TestCreateMontageEncounter:
    def test_creates_file_at_expected_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        assert path == adv_root / "encounters" / "montages" / "crossing-the-storm-peaks.md"
        assert path.is_file()

    def test_frontmatter_name(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["name"] == "Crossing the Storm Peaks"

    def test_frontmatter_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["slug"] == "crossing-the-storm-peaks"

    def test_frontmatter_created_is_date(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert isinstance(post["created"], datetime.date)

    def test_frontmatter_description_default_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["description"] is None

    def test_frontmatter_description_set(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(
                name="Crossing the Storm Peaks", description="A perilous journey."
            )
        post = frontmatter.load(str(path))
        assert post["description"] == "A perilous journey."

    def test_frontmatter_goal_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["goal"] is None

    def test_frontmatter_tests_empty_list(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["tests"] == []

    def test_frontmatter_success_threshold_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["success_threshold"] is None

    def test_frontmatter_location_null(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        post = frontmatter.load(str(path))
        assert post["location"] is None

    def test_uses_active_adventure_by_default(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            path = create_montage_encounter(name="Crossing the Storm Peaks")
        assert adv_root in path.parents

    def test_targets_specific_adventure_with_slug(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            path = create_montage_encounter(
                name="Crossing the Storm Peaks", adventure_slug="second-adventure"
            )
        assert "second-adventure" in str(path)

    def test_raises_if_no_active_adventure(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(RuntimeError, match="No active adventure"):
                create_montage_encounter(name="Crossing the Storm Peaks")

    def test_raises_if_adventure_slug_not_found(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError, match="no-such-adventure"):
                create_montage_encounter(
                    name="Crossing the Storm Peaks", adventure_slug="no-such-adventure"
                )

    def test_raises_if_file_already_exists(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_montage_encounter(name="Crossing the Storm Peaks")
            with pytest.raises(FileExistsError):
                create_montage_encounter(name="Crossing the Storm Peaks")

    def test_returns_path(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_montage_encounter(name="Crossing the Storm Peaks")
        assert isinstance(result, Path)

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                create_montage_encounter(name="Crossing the Storm Peaks")


# ---------------------------------------------------------------------------
# CLI integration tests — encounters group structure
# ---------------------------------------------------------------------------


class TestEncountersGroupCLI:
    def test_main_help_lists_encounters(self):
        result = CliRunner().invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "encounters" in result.output

    def test_encounters_help_lists_combat(self):
        result = CliRunner().invoke(main, ["encounters", "--help"])
        assert result.exit_code == 0
        assert "combat" in result.output

    def test_encounters_help_lists_negotiation(self):
        result = CliRunner().invoke(main, ["encounters", "--help"])
        assert result.exit_code == 0
        assert "negotiation" in result.output

    def test_encounters_help_lists_montage(self):
        result = CliRunner().invoke(main, ["encounters", "--help"])
        assert result.exit_code == 0
        assert "montage" in result.output

    def test_encounters_combat_help_lists_new(self):
        result = CliRunner().invoke(main, ["encounters", "combat", "--help"])
        assert result.exit_code == 0
        assert "new" in result.output

    def test_encounters_negotiation_help_lists_new(self):
        result = CliRunner().invoke(main, ["encounters", "negotiation", "--help"])
        assert result.exit_code == 0
        assert "new" in result.output

    def test_encounters_montage_help_lists_new(self):
        result = CliRunner().invoke(main, ["encounters", "montage", "--help"])
        assert result.exit_code == 0
        assert "new" in result.output


# ---------------------------------------------------------------------------
# CLI integration tests — encounters combat new
# ---------------------------------------------------------------------------


class TestEncountersCombatNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["encounters", "combat", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "combat", "new", "--name", "Throne Room Battle"],
            )
        assert result.exit_code == 0, result.output
        assert (adv_root / "encounters" / "combat" / "throne-room-battle.md").is_file()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "combat", "new", "--name", "Throne Room Battle"],
            )
        assert "Throne Room Battle" in result.output

    def test_with_description(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                [
                    "encounters", "combat", "new",
                    "--name", "Throne Room Battle",
                    "--description", "A fierce battle.",
                ],
            )
        assert result.exit_code == 0, result.output
        path = adv_root / "encounters" / "combat" / "throne-room-battle.md"
        post = frontmatter.load(str(path))
        assert post["description"] == "A fierce battle."

    def test_with_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            result = runner.invoke(
                main,
                [
                    "encounters", "combat", "new",
                    "--name", "Throne Room Battle",
                    "--adventure", "second-adventure",
                ],
            )
        assert result.exit_code == 0, result.output
        second_adv_root = campaign_root / "adventures" / "second-adventure"
        assert (second_adv_root / "encounters" / "combat" / "throne-room-battle.md").is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["encounters", "combat", "new", "--name", "Throne Room Battle"]
            )
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["encounters", "combat", "new", "--name", "Throne Room Battle"]
            )
        assert result.exit_code != 0

    def test_duplicate_exits_nonzero(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["encounters", "combat", "new", "--name", "Throne Room Battle"])
            result = runner.invoke(
                main, ["encounters", "combat", "new", "--name", "Throne Room Battle"]
            )
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# CLI integration tests — encounters negotiation new
# ---------------------------------------------------------------------------


class TestEncountersNegotiationNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["encounters", "negotiation", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
        assert result.exit_code == 0, result.output
        assert (
            adv_root / "encounters" / "negotiations" / "bargaining-with-the-harbormaster.md"
        ).is_file()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
        assert "Bargaining with the Harbormaster" in result.output

    def test_with_description(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                [
                    "encounters", "negotiation", "new",
                    "--name", "Bargaining with the Harbormaster",
                    "--description", "Trade deal.",
                ],
            )
        assert result.exit_code == 0, result.output
        path = adv_root / "encounters" / "negotiations" / "bargaining-with-the-harbormaster.md"
        post = frontmatter.load(str(path))
        assert post["description"] == "Trade deal."

    def test_with_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            result = runner.invoke(
                main,
                [
                    "encounters", "negotiation", "new",
                    "--name", "Bargaining with the Harbormaster",
                    "--adventure", "second-adventure",
                ],
            )
        assert result.exit_code == 0, result.output
        second_adv_root = campaign_root / "adventures" / "second-adventure"
        assert (
            second_adv_root / "encounters" / "negotiations" / "bargaining-with-the-harbormaster.md"
        ).is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
        assert result.exit_code != 0

    def test_duplicate_exits_nonzero(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
            result = runner.invoke(
                main,
                ["encounters", "negotiation", "new", "--name", "Bargaining with the Harbormaster"],
            )
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# CLI integration tests — encounters montage new
# ---------------------------------------------------------------------------


class TestEncountersMontageNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["encounters", "montage", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_file(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
        assert result.exit_code == 0, result.output
        assert (adv_root / "encounters" / "montages" / "crossing-the-storm-peaks.md").is_file()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
        assert "Crossing the Storm Peaks" in result.output

    def test_with_description(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                [
                    "encounters", "montage", "new",
                    "--name", "Crossing the Storm Peaks",
                    "--description", "A perilous journey.",
                ],
            )
        assert result.exit_code == 0, result.output
        path = adv_root / "encounters" / "montages" / "crossing-the-storm-peaks.md"
        post = frontmatter.load(str(path))
        assert post["description"] == "A perilous journey."

    def test_with_adventure_flag(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="Second Adventure")
            result = runner.invoke(
                main,
                [
                    "encounters", "montage", "new",
                    "--name", "Crossing the Storm Peaks",
                    "--adventure", "second-adventure",
                ],
            )
        assert result.exit_code == 0, result.output
        second_adv_root = campaign_root / "adventures" / "second-adventure"
        assert (
            second_adv_root / "encounters" / "montages" / "crossing-the-storm-peaks.md"
        ).is_file()

    def test_no_active_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
        assert result.exit_code != 0
        assert "No active adventure" in result.output

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
        assert result.exit_code != 0

    def test_duplicate_exits_nonzero(self, tmp_path):
        campaign_root, adv_root, fake_config_dir = _make_campaign_with_adventure(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
            result = runner.invoke(
                main,
                ["encounters", "montage", "new", "--name", "Crossing the Storm Peaks"],
            )
        assert result.exit_code != 0
