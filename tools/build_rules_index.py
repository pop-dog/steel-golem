#!/usr/bin/env python3
"""
Generate skills/rules-reference/SKILL.md from the steel-compendium submodule.

Re-run after `git submodule update` to keep the skill index current:

    python3 tools/build_rules_index.py
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPENDIUM = REPO_ROOT / "steel-compendium"
RULES = COMPENDIUM / "Rules"
BESTIARY = COMPENDIUM / "Bestiary" / "Monsters"
OUTPUT = REPO_ROOT / "skills" / "rules-reference" / "SKILL.md"

COMPENDIUM_ROOT = "~/.steel-golem/steel-compendium"

INSTRUCTIONS = f"""\
# rules-reference

Answer Draw Steel rules questions with citations sourced from the steel-compendium corpus.

Compendium root: `{COMPENDIUM_ROOT}/`

## How to answer a question

### Step 1 — Classify the question

**Named mechanic** — the question names a specific game term: an ability, condition, movement
type, kit, class, or monster. Examples: "how does Charge work?", "what is the Slowed
condition?", "what abilities does a Goblin Sniper have?"

**Conceptual** — the question asks how a system works broadly, or how two mechanics interact.
Examples: "how does the action economy work?", "walk me through a full Negotiation",
"what happens when a creature dies?"

### Step 2 — Locate the content

Consult the `## Index` section below to route to the right file(s). All paths are relative
to the compendium root.

**For a named mechanic:**

1. Check the Index for a dedicated file first. Conditions, movement rules, common abilities,
   class abilities, and kits all have one file per mechanic — read that file in full.
2. If no dedicated file exists, grep the relevant chapter file for the term as a markdown heading:
   ```
   grep -n "^#### <Term>\\|^### <Term>" {COMPENDIUM_ROOT}/Rules/Chapters/<Chapter>.md
   ```
   Then read ~60 lines from that heading.
3. For monsters, find the group directory from the Monster Groups list and read the stat block
   file(s) inside it.

**For a conceptual question:**

1. Identify the relevant chapter(s) from the Chapter Sections list in the Index.
2. Grep for the relevant `### Section` heading to get its line number:
   ```
   grep -n "^### <Section>" {COMPENDIUM_ROOT}/Rules/Chapters/<Chapter>.md
   ```
3. Read from that heading through the end of the section (typically 100–200 lines).
4. If the question spans multiple sections or chapters, read each relevant section in turn.

### Step 3 — Synthesize the answer

Write a direct prose answer. Weave citations inline as the answer draws from each source.

Citation format:
- Chapter content: `(Chapter N: Title, Section Name)`
- Dedicated file: `(Condition: Slowed)`, `(Common Ability: Charge)`, `(Kit: Panther)`
- Bestiary: `(Monsters: Goblins)`, `(Monster Basics)`

### Step 4 — If not found

If the corpus search turns up nothing relevant, do not answer from training knowledge.
Respond exactly as follows, listing what you searched:

> "I couldn't find this in the Draw Steel rules corpus. I searched: [list files/sections
> checked]. You may want to check the book directly."

"""


def stem_list(path: Path, suffix: str = ".md") -> list[str]:
    return sorted(
        p.stem for p in path.glob(f"*{suffix}") if p.is_file() and not p.stem.startswith("_")
    )


def dir_list(path: Path) -> list[str]:
    return sorted(p.name for p in path.iterdir() if p.is_dir() and not p.name.startswith("_"))


def chapter_sections(chapter_file: Path) -> list[str]:
    seen: set[str] = set()
    sections = []
    pattern = re.compile(r"^### (.+)")
    with open(chapter_file, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.rstrip())
            if m:
                title = m.group(1)
                if title not in seen:
                    seen.add(title)
                    sections.append(title)
    return sections


def ability_tree(abilities_root: Path) -> dict[str, dict[str, list[str]]]:
    """Return {class_name: {tier: [ability_names]}} for all ability files."""
    tree: dict[str, dict[str, list[str]]] = {}
    for class_dir in sorted(abilities_root.iterdir()):
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        tiers: dict[str, list[str]] = {}
        for tier_dir in sorted(class_dir.iterdir()):
            if not tier_dir.is_dir():
                continue
            abilities = stem_list(tier_dir)
            if abilities:
                tiers[tier_dir.name] = abilities
        if tiers:
            tree[class_name] = tiers
        direct = stem_list(class_dir)
        if direct:
            tree.setdefault(class_name, {})["(top-level)"] = direct
    return tree


def build_index() -> str:
    lines = ["## Index\n\n"]
    lines.append("_Generated from `steel-compendium`. Re-run `python3 tools/build_rules_index.py` after `git submodule update`._\n\n")

    # Routing table
    lines.append("### Routing Guide\n\n")
    lines.append("| Question type | Where to look |\n")
    lines.append("|---|---|\n")
    lines.append("| Named condition (Slowed, Grabbed, etc.) | `Rules/Conditions/<Name>.md` |\n")
    lines.append("| Movement type or interaction (Fly, Teleport, Falling, etc.) | `Rules/Movement/<Name>.md` |\n")
    lines.append("| Named common ability (Charge, Grab, Hide, etc.) | `Rules/Abilities/Common/<Tier>/<Name>.md` |\n")
    lines.append("| Class-specific ability | `Rules/Abilities/<ClassName>/<Level>/<Name>.md` |\n")
    lines.append("| Class overview or features | `Rules/Classes/<ClassName>.md` |\n")
    lines.append("| Kit | `Rules/Kits/<Name>.md` |\n")
    lines.append("| Ancestry | `Rules/Chapters/Ancestries.md` |\n")
    lines.append("| Negotiation motivation or pitfall | `Rules/Negotiation/Motivations and Pitfalls.md` |\n")
    lines.append("| Broad rules topic (combat, tests, downtime, etc.) | `Rules/Chapters/<Chapter>.md` — grep heading, read section |\n")
    lines.append("| Monster stat block or abilities | `Bestiary/Monsters/Monsters/<Group>/` |\n")
    lines.append("| Rules for running monsters, keywords, traits | `Bestiary/Monsters/Chapters/Monster Basics.md` |\n")
    lines.append("| Dynamic terrain rules | `Bestiary/Monsters/Chapters/Dynamic Terrain.md` |\n")
    lines.append("| Retainer rules | `Bestiary/Monsters/Chapters/Retainers.md` |\n\n")

    # Conditions
    conditions = stem_list(RULES / "Conditions")
    lines.append("### Conditions\n")
    lines.append("`Rules/Conditions/<Name>.md` — one file per condition.\n")
    lines.append(", ".join(conditions) + "\n\n")

    # Movement
    movement = stem_list(RULES / "Movement")
    lines.append("### Movement Rules\n")
    lines.append("`Rules/Movement/<Name>.md` — one file per movement topic.\n")
    lines.append(", ".join(movement) + "\n\n")

    # Classes
    classes = stem_list(RULES / "Classes")
    lines.append("### Classes\n")
    lines.append("`Rules/Classes/<Name>.md` — one file per class.\n")
    lines.append(", ".join(classes) + "\n\n")

    # Kits
    kits = stem_list(RULES / "Kits")
    lines.append("### Kits\n")
    lines.append("`Rules/Kits/<Name>.md` — one file per kit.\n")
    lines.append(", ".join(kits) + "\n\n")

    # Abilities
    lines.append("### Abilities\n")
    lines.append("`Rules/Abilities/<Class>/<Tier>/<Name>.md`\n\n")
    tree = ability_tree(RULES / "Abilities")
    for class_name, tiers in tree.items():
        lines.append(f"**{class_name}**\n")
        for tier, abilities in tiers.items():
            lines.append(f"- {tier}: {', '.join(abilities)}\n")
        lines.append("\n")

    # Chapter section map
    lines.append("### Chapter Sections\n")
    lines.append("`Rules/Chapters/<Chapter>.md` — grep a `### Section` heading, then read that section.\n\n")
    chapter_dir = RULES / "Chapters"
    for chapter_file in sorted(chapter_dir.glob("*.md")):
        if chapter_file.stem.startswith("_"):
            continue
        sections = chapter_sections(chapter_file)
        if sections:
            lines.append(f"**{chapter_file.stem}:** {', '.join(sections)}\n\n")

    # Monster groups
    monsters_dir = BESTIARY / "Monsters"
    groups = dir_list(monsters_dir)
    lines.append("### Monster Groups\n")
    lines.append("`Bestiary/Monsters/Monsters/<Group>/` — one directory per monster group.\n")
    lines.append(", ".join(groups) + "\n\n")

    # Bestiary chapters
    bestiary_chapters = stem_list(BESTIARY / "Chapters")
    lines.append("### Bestiary Chapters\n")
    lines.append("`Bestiary/Monsters/Chapters/<Name>.md` — rules for running monsters.\n")
    lines.append(", ".join(bestiary_chapters) + "\n\n")

    return "".join(lines)


def main() -> None:
    if not COMPENDIUM.exists():
        raise SystemExit(
            "steel-compendium not found. Run: git submodule update --init --recursive"
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = INSTRUCTIONS + build_index()
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Written: {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
