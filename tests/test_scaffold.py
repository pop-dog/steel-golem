"""Tests for scaffold.py — campaign directory creation."""
import datetime
import os
from pathlib import Path
from unittest.mock import patch

import frontmatter
import pytest
from click.testing import CliRunner

from steel_golem.cli import main
from steel_golem.scaffold import slugify, create_campaign


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
