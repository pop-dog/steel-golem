from click.testing import CliRunner
from steel_golem.cli import main


def test_main_help_lists_campaigns():
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "campaigns" in result.output


def test_main_help_lists_adventures():
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "adventures" in result.output


def test_campaigns_help_lists_new():
    result = CliRunner().invoke(main, ["campaigns", "--help"])
    assert result.exit_code == 0
    assert "new" in result.output


def test_adventures_help_lists_new_set_list():
    result = CliRunner().invoke(main, ["adventures", "--help"])
    assert result.exit_code == 0
    assert "new" in result.output
    assert "set" in result.output
    assert "list" in result.output
