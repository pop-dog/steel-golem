"""Tests for scaffold.py — campaign directory creation."""
import datetime
import os
from pathlib import Path
from unittest.mock import patch

import frontmatter
import pytest
from click.testing import CliRunner

from steel_golem.cli import main
from steel_golem.scaffold import (
    slugify,
    create_campaign,
    create_adventure,
    read_config,
    set_adventure,
    list_adventures,
)


EXPECTED_SUBDIRS = [
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


# ---------------------------------------------------------------------------
# slugify unit tests
# ---------------------------------------------------------------------------

class TestSlugify:
    def test_lowercase(self):
        assert slugify("Iron Throne") == "iron-throne"

    def test_spaces_become_hyphens(self):
        assert slugify("the iron throne") == "the-iron-throne"

    def test_underscores_become_hyphens(self):
        assert slugify("iron_throne") == "iron-throne"

    def test_non_alphanumeric_stripped(self):
        assert slugify("Iron! Throne?") == "iron-throne"

    def test_consecutive_hyphens_collapsed(self):
        assert slugify("iron  throne") == "iron-throne"

    def test_leading_trailing_hyphens_stripped(self):
        assert slugify("  iron throne  ") == "iron-throne"

    def test_mixed_punctuation(self):
        assert slugify("The 'Iron' Throne!") == "the-iron-throne"

    def test_already_a_slug(self):
        assert slugify("iron-throne") == "iron-throne"

    def test_numbers_preserved(self):
        assert slugify("Campaign 2") == "campaign-2"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="slug"):
            slugify("")

    def test_only_symbols_raises(self):
        with pytest.raises(ValueError, match="slug"):
            slugify("!!! ???")


# ---------------------------------------------------------------------------
# create_campaign unit tests
# ---------------------------------------------------------------------------

class TestCreateCampaign:
    def test_creates_expected_subdirectories(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        campaign_root = tmp_path / "iron-throne"
        for subdir in EXPECTED_SUBDIRS:
            assert (campaign_root / subdir).is_dir(), f"Missing subdir: {subdir}"

    def test_no_extra_items_in_root(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        campaign_root = tmp_path / "iron-throne"
        items = {p.name for p in campaign_root.iterdir()}
        expected = set(EXPECTED_SUBDIRS) | {"index.md"}
        assert items == expected

    def test_index_md_exists(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        index = tmp_path / "iron-throne" / "index.md"
        assert index.is_file()

    def test_index_md_frontmatter_name(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        post = frontmatter.load(str(tmp_path / "iron-throne" / "index.md"))
        assert post["name"] == "Iron Throne"

    def test_index_md_frontmatter_slug(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        post = frontmatter.load(str(tmp_path / "iron-throne" / "index.md"))
        assert post["slug"] == "iron-throne"

    def test_index_md_frontmatter_status(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        post = frontmatter.load(str(tmp_path / "iron-throne" / "index.md"))
        assert post["status"] == "active"

    def test_index_md_frontmatter_current_adventure_null(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        post = frontmatter.load(str(tmp_path / "iron-throne" / "index.md"))
        assert post["current_adventure"] is None

    def test_index_md_frontmatter_created_is_iso_date(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        post = frontmatter.load(str(tmp_path / "iron-throne" / "index.md"))
        created = post["created"]
        # Should be parseable as an ISO date
        datetime.date.fromisoformat(str(created))

    def test_slug_edge_case_underscores(self, tmp_path):
        create_campaign(name="iron_throne", path=tmp_path)
        assert (tmp_path / "iron-throne").is_dir()

    def test_slug_edge_case_mixed_symbols(self, tmp_path):
        create_campaign(name="The 'Iron' Throne!", path=tmp_path)
        assert (tmp_path / "the-iron-throne").is_dir()

    def test_existing_directory_raises(self, tmp_path):
        create_campaign(name="Iron Throne", path=tmp_path)
        with pytest.raises(FileExistsError):
            create_campaign(name="Iron Throne", path=tmp_path)

    def test_empty_slug_raises_value_error(self, tmp_path):
        with pytest.raises(ValueError, match="slug"):
            create_campaign(name="!!!", path=tmp_path)

    def test_returns_campaign_root_path(self, tmp_path):
        result = create_campaign(name="Iron Throne", path=tmp_path)
        assert result == tmp_path / "iron-throne"

    def test_subdirs_contain_no_files(self, tmp_path):
        """No stub files or .gitkeep files in entity subdirs."""
        create_campaign(name="Iron Throne", path=tmp_path)
        campaign_root = tmp_path / "iron-throne"
        for subdir in EXPECTED_SUBDIRS:
            contents = list((campaign_root / subdir).iterdir())
            assert contents == [], f"Subdir {subdir} should be empty, got: {contents}"


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

class TestCampaignsNewCLI:
    def test_missing_name_fails(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(main, ["campaigns", "new", "--path", str(tmp_path)])
        assert result.exit_code != 0
        assert "name" in result.output.lower() or "name" in (result.stderr or "").lower()

    def test_missing_path_fails(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(main, ["campaigns", "new", "--name", "Iron Throne"])
        assert result.exit_code != 0
        assert "path" in result.output.lower() or "path" in (result.stderr or "").lower()

    def test_successful_run_creates_campaign(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "iron-throne").is_dir()

    def test_successful_run_writes_config(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        import yaml
        config = yaml.safe_load((fake_config_dir / "config.yaml").read_text())
        assert config["campaign_path"] == str(tmp_path / "iron-throne")

    def test_successful_run_creates_config_dir_if_absent(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        assert not fake_config_dir.exists()
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        assert fake_config_dir.is_dir()

    def test_successful_run_prints_success_message(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        assert result.exit_code == 0
        assert "Iron Throne" in result.output
        assert "iron-throne" in result.output

    def test_existing_directory_exits_nonzero(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
            result = runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        assert result.exit_code != 0
        assert "iron-throne" in result.output.lower() or "already exists" in result.output.lower()

    def test_config_path_is_absolute(self, tmp_path):
        runner = CliRunner(mix_stderr=False)
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(
                main,
                ["campaigns", "new", "--name", "Iron Throne", "--path", str(tmp_path)],
            )
        import yaml
        config = yaml.safe_load((fake_config_dir / "config.yaml").read_text())
        assert Path(config["campaign_path"]).is_absolute()


# ---------------------------------------------------------------------------
# Helpers shared by adventure tests
# ---------------------------------------------------------------------------

EXPECTED_ADVENTURE_SUBDIRS = [
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


def _make_campaign(tmp_path):
    """Create a minimal campaign and config; return (campaign_root, fake_config_dir)."""
    fake_config_dir = tmp_path / ".steel-golem"
    campaign_root = create_campaign(name="Iron Throne", path=tmp_path)
    fake_config_dir.mkdir(parents=True, exist_ok=True)
    (fake_config_dir / "config.yaml").write_text(
        f"campaign_path: {campaign_root}\n"
    )
    return campaign_root, fake_config_dir


# ---------------------------------------------------------------------------
# read_config tests
# ---------------------------------------------------------------------------

class TestReadConfig:
    def test_absent_config_raises_file_not_found(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError, match="campaigns new"):
                read_config()

    def test_returns_campaign_path(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            config = read_config()
        assert config["campaign_path"] == str(campaign_root)


# ---------------------------------------------------------------------------
# create_adventure unit tests
# ---------------------------------------------------------------------------

class TestCreateAdventure:
    def test_creates_expected_subdirectories(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        adv_root = campaign_root / "adventures" / "the-sunken-vault"
        for subdir in EXPECTED_ADVENTURE_SUBDIRS:
            assert (adv_root / subdir).is_dir(), f"Missing: {subdir}"

    def test_subdirs_contain_no_files(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        adv_root = campaign_root / "adventures" / "the-sunken-vault"
        for subdir in EXPECTED_ADVENTURE_SUBDIRS:
            assert list((adv_root / subdir).iterdir()) == []

    def test_index_md_frontmatter_name(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        post = frontmatter.load(
            str(campaign_root / "adventures" / "the-sunken-vault" / "index.md")
        )
        assert post["name"] == "The Sunken Vault"

    def test_index_md_frontmatter_slug(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        post = frontmatter.load(
            str(campaign_root / "adventures" / "the-sunken-vault" / "index.md")
        )
        assert post["slug"] == "the-sunken-vault"

    def test_index_md_frontmatter_status_active(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        post = frontmatter.load(
            str(campaign_root / "adventures" / "the-sunken-vault" / "index.md")
        )
        assert post["status"] == "active"

    def test_index_md_frontmatter_created_is_date_object(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        post = frontmatter.load(
            str(campaign_root / "adventures" / "the-sunken-vault" / "index.md")
        )
        assert isinstance(post["created"], datetime.date)

    def test_sets_current_adventure_when_null(self, tmp_path):
        """First adventure sets current_adventure in campaign index.md."""
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
        campaign_post = frontmatter.load(str(campaign_root / "index.md"))
        assert campaign_post["current_adventure"] == "the-sunken-vault"

    def test_does_not_change_current_adventure_when_already_set(self, tmp_path):
        """Second adventure does not overwrite current_adventure."""
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            create_adventure(name="The Black Moor")
        campaign_post = frontmatter.load(str(campaign_root / "index.md"))
        assert campaign_post["current_adventure"] == "the-sunken-vault"

    def test_existing_directory_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            with pytest.raises(FileExistsError):
                create_adventure(name="The Sunken Vault")

    def test_empty_slug_raises_value_error(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(ValueError, match="slug"):
                create_adventure(name="!!!")

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                create_adventure(name="The Sunken Vault")

    def test_returns_adventure_root_path(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = create_adventure(name="The Sunken Vault")
        assert result == campaign_root / "adventures" / "the-sunken-vault"


# ---------------------------------------------------------------------------
# set_adventure unit tests
# ---------------------------------------------------------------------------

class TestSetAdventure:
    def test_updates_current_adventure(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            create_adventure(name="The Black Moor")
            set_adventure(slug="the-black-moor")
        campaign_post = frontmatter.load(str(campaign_root / "index.md"))
        assert campaign_post["current_adventure"] == "the-black-moor"

    def test_preserves_other_frontmatter(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            set_adventure(slug="the-sunken-vault")
        campaign_post = frontmatter.load(str(campaign_root / "index.md"))
        assert campaign_post["name"] == "Iron Throne"
        assert campaign_post["slug"] == "iron-throne"
        assert campaign_post["status"] == "active"

    def test_preserves_body(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        # Inject some body text
        index_path = campaign_root / "index.md"
        post = frontmatter.load(str(index_path))
        post.content = "Some body text."
        index_path.write_text(frontmatter.dumps(post))

        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            set_adventure(slug="the-sunken-vault")
        campaign_post = frontmatter.load(str(index_path))
        assert campaign_post.content == "Some body text."

    def test_nonexistent_slug_raises(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError, match="no-such-slug"):
                set_adventure(slug="no-such-slug")

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                set_adventure(slug="the-sunken-vault")


# ---------------------------------------------------------------------------
# list_adventures unit tests
# ---------------------------------------------------------------------------

class TestListAdventures:
    def test_empty_returns_empty_list(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = list_adventures()
        assert result == []

    def test_returns_all_adventures(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            create_adventure(name="The Black Moor")
            result = list_adventures()
        slugs = {a["slug"] for a in result}
        assert slugs == {"the-sunken-vault", "the-black-moor"}

    def test_current_adventure_marked(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            create_adventure(name="The Black Moor")
            result = list_adventures()
        current = [a for a in result if a["current"]]
        assert len(current) == 1
        assert current[0]["slug"] == "the-sunken-vault"

    def test_non_current_not_marked(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            create_adventure(name="The Sunken Vault")
            create_adventure(name="The Black Moor")
            result = list_adventures()
        non_current = [a for a in result if not a["current"]]
        assert any(a["slug"] == "the-black-moor" for a in non_current)

    def test_absent_config_raises(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            with pytest.raises(FileNotFoundError):
                list_adventures()


# ---------------------------------------------------------------------------
# adventures CLI integration tests
# ---------------------------------------------------------------------------

class TestAdventuresNewCLI:
    def test_missing_name_fails(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["adventures", "new"])
        assert result.exit_code != 0

    def test_successful_run_creates_adventure(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["adventures", "new", "--name", "The Sunken Vault"]
            )
        assert result.exit_code == 0, result.output
        assert (campaign_root / "adventures" / "the-sunken-vault").is_dir()

    def test_successful_run_prints_message(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["adventures", "new", "--name", "The Sunken Vault"]
            )
        assert "The Sunken Vault" in result.output

    def test_existing_adventure_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["adventures", "new", "--name", "The Sunken Vault"])
            result = runner.invoke(
                main, ["adventures", "new", "--name", "The Sunken Vault"]
            )
        assert result.exit_code != 0
        assert "already exists" in result.output.lower()

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(
                main, ["adventures", "new", "--name", "The Sunken Vault"]
            )
        assert result.exit_code != 0
        assert "campaigns new" in result.output


class TestAdventuresSetCLI:
    def test_successful_set_prints_message(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["adventures", "new", "--name", "The Sunken Vault"])
            runner.invoke(main, ["adventures", "new", "--name", "The Black Moor"])
            result = runner.invoke(main, ["adventures", "set", "the-black-moor"])
        assert result.exit_code == 0, result.output
        assert "the-black-moor" in result.output

    def test_nonexistent_slug_exits_nonzero(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["adventures", "set", "no-such-slug"])
        assert result.exit_code != 0
        assert "no-such-slug" in result.output

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["adventures", "set", "something"])
        assert result.exit_code != 0


class TestAdventuresListCLI:
    def test_no_adventures_prints_message(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["adventures", "list"])
        assert result.exit_code == 0
        assert "no adventures" in result.output.lower()

    def test_lists_slug_and_name(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["adventures", "new", "--name", "The Sunken Vault"])
            runner.invoke(main, ["adventures", "new", "--name", "The Black Moor"])
            result = runner.invoke(main, ["adventures", "list"])
        assert "the-sunken-vault" in result.output
        assert "The Sunken Vault" in result.output
        assert "the-black-moor" in result.output
        assert "The Black Moor" in result.output

    def test_current_adventure_marked_with_asterisk(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["adventures", "new", "--name", "The Sunken Vault"])
            runner.invoke(main, ["adventures", "new", "--name", "The Black Moor"])
            result = runner.invoke(main, ["adventures", "list"])
        # Use splitlines() without strip() so line markers are preserved
        lines = result.output.splitlines()
        current_lines = [l for l in lines if l.startswith("*")]
        assert len(current_lines) == 1
        assert "the-sunken-vault" in current_lines[0]

    def test_non_current_adventure_has_space_marker(self, tmp_path):
        campaign_root, fake_config_dir = _make_campaign(tmp_path)
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            runner.invoke(main, ["adventures", "new", "--name", "The Sunken Vault"])
            runner.invoke(main, ["adventures", "new", "--name", "The Black Moor"])
            result = runner.invoke(main, ["adventures", "list"])
        # Use splitlines() without strip() so leading space markers are preserved
        lines = result.output.splitlines()
        space_lines = [l for l in lines if l and not l.startswith("*")]
        assert any("the-black-moor" in l for l in space_lines)

    def test_absent_config_exits_nonzero(self, tmp_path):
        fake_config_dir = tmp_path / ".steel-golem"
        runner = CliRunner(mix_stderr=False)
        with patch("steel_golem.scaffold.CONFIG_DIR", fake_config_dir):
            result = runner.invoke(main, ["adventures", "list"])
        assert result.exit_code != 0
