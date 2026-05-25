"""Tests for install.sh.

install.sh honours two environment variable overrides:
- STEEL_GOLEM_HOME  (default: ~/.steel-golem)
- CLAUDE_HOME       (default: ~/.claude)

All tests redirect both to temp directories so nothing touches the real home.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Absolute path to install.sh, resolved from this file's location.
REPO_ROOT = Path(__file__).parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"


def run_install(steel_golem_home: Path, claude_home: Path) -> subprocess.CompletedProcess:
    """Run install.sh with the given home directory overrides."""
    env = os.environ.copy()
    env["STEEL_GOLEM_HOME"] = str(steel_golem_home)
    env["CLAUDE_HOME"] = str(claude_home)
    return subprocess.run(
        [str(INSTALL_SH)],
        env=env,
        capture_output=True,
        text=True,
    )


@pytest.fixture()
def homes(tmp_path):
    """Yield (steel_golem_home, claude_home) paths inside a temp directory."""
    sg_home = tmp_path / "steel-golem"
    cl_home = tmp_path / "claude"
    yield sg_home, cl_home


# ---------------------------------------------------------------------------
# 1. ~/.steel-golem/ is created
# ---------------------------------------------------------------------------

def test_creates_steel_golem_home(homes):
    sg_home, cl_home = homes
    result = run_install(sg_home, cl_home)
    assert result.returncode == 0, result.stderr
    assert sg_home.is_dir()


# ---------------------------------------------------------------------------
# 2. CONTEXT.md symlink
# ---------------------------------------------------------------------------

def test_context_md_symlink_exists(homes):
    sg_home, cl_home = homes
    result = run_install(sg_home, cl_home)
    assert result.returncode == 0, result.stderr
    link = sg_home / "CONTEXT.md"
    assert link.is_symlink()


def test_context_md_symlink_points_to_repo(homes):
    sg_home, cl_home = homes
    run_install(sg_home, cl_home)
    link = sg_home / "CONTEXT.md"
    assert link.resolve() == (REPO_ROOT / "CONTEXT.md").resolve()


# ---------------------------------------------------------------------------
# 3. steel-compendium symlink
# ---------------------------------------------------------------------------

def test_steel_compendium_symlink_exists(homes):
    sg_home, cl_home = homes
    result = run_install(sg_home, cl_home)
    assert result.returncode == 0, result.stderr
    link = sg_home / "steel-compendium"
    assert link.is_symlink()


def test_steel_compendium_symlink_points_to_repo(homes):
    sg_home, cl_home = homes
    run_install(sg_home, cl_home)
    link = sg_home / "steel-compendium"
    assert link.resolve() == (REPO_ROOT / "steel-compendium").resolve()


# ---------------------------------------------------------------------------
# 4. Agent symlink
# ---------------------------------------------------------------------------

def test_agent_symlink_exists(homes):
    sg_home, cl_home = homes
    result = run_install(sg_home, cl_home)
    assert result.returncode == 0, result.stderr
    link = cl_home / "agents" / "steel-golem.md"
    assert link.is_symlink()


def test_agent_symlink_points_to_repo(homes):
    sg_home, cl_home = homes
    run_install(sg_home, cl_home)
    link = cl_home / "agents" / "steel-golem.md"
    assert link.resolve() == (REPO_ROOT / "agents" / "steel-golem.md").resolve()


# ---------------------------------------------------------------------------
# 5. Skill symlinks
# ---------------------------------------------------------------------------

def test_each_skill_is_symlinked(homes):
    sg_home, cl_home = homes
    result = run_install(sg_home, cl_home)
    assert result.returncode == 0, result.stderr

    skills_src = REPO_ROOT / "skills"
    for skill_dir in skills_src.iterdir():
        if not skill_dir.is_dir():
            continue
        link = cl_home / "skills" / skill_dir.name
        assert link.is_symlink(), f"expected symlink for skill {skill_dir.name}"
        assert link.resolve() == skill_dir.resolve()


# ---------------------------------------------------------------------------
# 6. Idempotency — running twice does not error
# ---------------------------------------------------------------------------

def test_idempotent_second_run_succeeds(homes):
    sg_home, cl_home = homes
    first = run_install(sg_home, cl_home)
    assert first.returncode == 0, first.stderr
    second = run_install(sg_home, cl_home)
    assert second.returncode == 0, second.stderr


def test_idempotent_symlinks_still_correct_after_second_run(homes):
    sg_home, cl_home = homes
    run_install(sg_home, cl_home)
    run_install(sg_home, cl_home)

    assert (sg_home / "CONTEXT.md").resolve() == (REPO_ROOT / "CONTEXT.md").resolve()
    assert (sg_home / "steel-compendium").resolve() == (REPO_ROOT / "steel-compendium").resolve()
    assert (cl_home / "agents" / "steel-golem.md").resolve() == (
        REPO_ROOT / "agents" / "steel-golem.md"
    ).resolve()
