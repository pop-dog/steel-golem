# Steel Golem — Product Requirements Document

## Problem Statement

Running a Draw Steel campaign requires a Director to manage a growing body of interconnected information: Heroes and their goals, Villains and their plans, Adventures with their NPCs and Encounters, Plots spanning the whole Campaign, Downtime Projects, Handouts, and more. This information currently lives across scattered notes, PDFs, and memory. Before each Session, the Director must manually gather and synthesize all of it to run a good game. The Draw Steel rules are also dense and nuanced — quick rules lookups during prep or play have no authoritative, citable source readily available.

## Solution

Steel Golem is a personal Director assistant implemented as a set of Claude Skills, Agents, and helper scripts, backed by a structured Campaign Database of markdown files with YAML frontmatter. The Director interacts with steel-golem in natural language. Steel-golem reads and writes the Campaign Database to track all Campaign entities, assists with Session planning through structured workflows (including the Lazy DM eight-step method), and answers rules questions authoritatively by searching the steel-compendium markdown corpus.

## User Stories

### Rules Reference

1. As a Director, I want to ask a rules question in natural language and get an authoritative answer, so that I don't have to flip through the rulebook during prep or play.
2. As a Director, I want every rules answer to cite the specific file and section in steel-compendium, so that I can verify and read further context.
3. As a Director, I want to ask about Negotiation mechanics and get the Patience, Interest, motivations, and pitfalls structure explained, so that I can prep a Negotiation Encounter correctly.
4. As a Director, I want to ask about Montage mechanics and understand what a successful skill test sequence looks like, so that I can design engaging group challenges.
5. As a Director, I want to ask about Downtime Projects and have the rules for Project Points, Project Rolls, and Breakthroughs explained, so that I can design Director-created projects as narrative hooks.
6. As a Director, I want to ask about any class, ancestry, kit, or ability from the Heroes book, so that I understand what my players' Heroes can do.
7. As a Director, I want to look up any monster from the bestiary and get its stat block, so that I can plan Encounters accurately.

### Campaign Database

8. As a Director, I want to create a new Campaign with a scaffolded directory structure, so that I have a consistent starting point for all Campaign entities.
9. As a Director, I want to create a new Adventure within a Campaign, so that the adventure-scoped entity directories are ready to populate.
10. As a Director, I want to create Hero files for each player character, so that I have a canonical reference for their goals, connections, and current state.
11. As a Director, I want to create Villain files at Campaign or Adventure scope, so that I can track each antagonist's plans, motivations, and current status.
12. As a Director, I want to create NPC files at Campaign or Adventure scope, so that I can track names, roles, and relationships without losing detail between Sessions.
13. As a Director, I want to create Faction files at Campaign or Adventure scope, so that I can track each group's goals, members, and relationship with the Heroes.
14. As a Director, I want to create Location files at Campaign or Adventure scope, so that I have a spatial anchor for Sessions, Encounters, and NPCs.
15. As a Director, I want to embed sub-locations within a parent Location file, so that I don't over-engineer the structure until a location warrants its own file.
16. As a Director, I want to Promote a sub-location to its own first-class Entity, so that it can be referenced independently when an Adventure or Campaign revolves around it.
17. As a Director, I want to create Plot files for Campaign-level narrative arcs, so that I can track overarching story threads across Adventures.
18. As a Director, I want to create Subplot files within an Adventure, so that I can track the local narrative threads and link them to parent Plots.
19. As a Director, I want to write Session files with Beats embedded as prose, so that I have a chronological adventure log.
20. As a Director, I want each Session file to reference its current Adventure, so that I can reconstruct the timeline without nesting Sessions under Adventures.
21. As a Director, I want to create Notable Item files for named items with history and ownership, so that significant loot is tracked independently from encounter notes.
22. As a Director, I want to create Lore files for cross-cutting world-building content, so that setting material that doesn't belong to any single Entity has a home.
23. As a Director, I want to create Handout files with a `revealed` status field, so that I know which artifacts have been shown to the players.
24. As a Director, I want to Promote an Adventure-scoped Entity (NPC, Villain, Faction, Location) to Campaign scope, so that a recurring character or place is referenceable across all Adventures.
25. As a Director, I want to create Director-designed Downtime Project files assigned to a Hero, so that I can use crafting and research as narrative hooks and track progress across Respites.

### Encounters

26. As a Director, I want to create Combat Encounter files with a monster roster, terrain notes, and an objective, so that I can prep tactical fights efficiently.
27. As a Director, I want to create Negotiation files with an NPC reference, Patience, Interest, motivations, and pitfalls, so that I have everything I need to run the social mechanics.
28. As a Director, I want to create Montage files with a goal, required tests, and a success threshold, so that I can design group challenges with clear stakes.
29. As a Director, I want the build-encounter skill to read the current Adventure context and the Heroes' capabilities before scaffolding a file, so that the encounter is appropriately calibrated.
30. As a Director, I want to reference Custom Monster files from my Encounter files, so that homebrew creatures are tracked with the same structure as compendium monsters.

### Session Planning

31. As a Director, I want to invoke the lazy-dm skill and be walked through the eight Lazy DM prep steps interactively, so that I produce a thorough session file without starting from a blank page.
32. As a Director, I want the lazy-dm skill to read Hero files before Step 1 and propose character hooks, so that I don't have to manually recall each Hero's goals.
33. As a Director, I want the lazy-dm skill to read active Plots and Subplots before Step 4 and propose secrets and clues, so that narrative threads remain connected across Sessions.
34. As a Director, I want the lazy-dm skill to read Location files before Step 5 and propose relevant locations for the upcoming Session, so that the spatial context is pre-populated.
35. As a Director, I want the lazy-dm skill to read NPC and Villain files before Step 6 and propose the relevant cast, so that I only have to add or remove rather than recall from memory.
36. As a Director, I want the lazy-dm skill to reference the steel-compendium bestiary before Step 7 and suggest monsters appropriate to the Adventure context, so that encounter selection is informed by the rules.
37. As a Director, I want to approve, reject, or refine each lazy-dm step's proposed answer before the next step proceeds, so that the output reflects my creative judgment.
38. As a Director, I want the completed lazy-dm output written as a Session file in the Campaign Database, so that prep is immediately persisted and referenceable.
39. As a Director, I want a campaign-briefing skill that synthesizes recent Sessions, active Plots, upcoming Encounters, and in-progress Downtime Projects into a summary, so that I can re-orient quickly before a Session.

### Import

40. As a Director, I want to import a published adventure PDF into steel-golem, so that I can use a commercial module without manually entering all its entities.
41. As a Director, I want the import-adventure skill to scaffold the Adventure directory structure, so that the module's entities have the correct home.
42. As a Director, I want the import-adventure skill to extract and create NPC files from the module, so that I can reference and annotate them immediately.
43. As a Director, I want the import-adventure skill to extract and create Location files from the module, so that the spatial structure of the adventure is browsable.
44. As a Director, I want the import-adventure skill to extract and create Encounter files (Combat, Negotiation, Montage) from the module, so that I can review and modify them before play.
45. As a Director, I want the import-adventure skill to create Handout files with `revealed: false` for all player-facing artifacts in the module, so that I control what the players see.
46. As a Director, I want the import-adventure skill to match extracted monsters against the steel-compendium bestiary and only create Custom Monster files for creatures not found there, so that the bestiary remains the canonical source.

### HTTP Serving

47. As a Director, I want to start a local HTTP server that renders the Campaign Database as browsable HTML, so that I have a richer reading experience than raw markdown.
48. As a Director, I want a Director-facing server route that shows all Campaign entities, so that I can browse the full Campaign state.
49. As a Director, I want a player-facing server route that shows only Handouts where `revealed: true`, so that players can access clues and artifacts on their own devices during a Session.
50. As a Director, I want to mark a Handout as `revealed: true` and have it appear immediately on the player-facing route, so that revealing information at the table is a single frontmatter edit.

### Configuration

51. As a Director, I want steel-golem to read a configuration file specifying the path to my Campaign Database, so that the Campaign Database can live anywhere on my filesystem.
52. As a Director, I want the configuration to be version-controlled with steel-golem, so that my setup is reproducible.

## Implementation Decisions

### Campaign Database Schema

- All entities are markdown files with YAML frontmatter.
- The directory tree follows the structure defined in `CONTEXT.md`: campaign-scoped entities live at `campaign/<type>/`; adventure-scoped entities live at `campaign/adventures/<adventure-name>/<type>/`.
- Encounter subtypes use subdirectories: `encounters/combat/`, `encounters/negotiations/`, `encounters/montages/`.
- Sessions live flat at `campaign/sessions/` with an `adventure` frontmatter field referencing the active Adventure.
- Handouts carry a `revealed` boolean frontmatter field; default is `false`.
- Sub-locations are embedded as prose within a parent Location file until Promoted to their own file with a `parent_location` frontmatter field.
- Entity Promotion (adventure → campaign scope) is a file move plus frontmatter update; no data is lost.
- Campaign Database location is external to steel-golem and specified via a configuration file.

### Configuration

- A `config.yaml` at the steel-golem repo root specifies `campaign_path: /absolute/path/to/campaign`.
- All skills and scripts read this file to locate the Campaign Database.

### rules-reference Skill

- Implements search-then-read: grep/find against `steel-compendium/` for relevant files, read the matched file, answer with a citation to the file path and section.
- No vector database or embedding layer; the steel-compendium directory structure is the index.
- The skill covers `Rules/`, `Bestiary/`, and `Adventures/` subdirectories of steel-compendium.

### lazy-dm Skill

- Implements the eight Lazy DM steps sequentially, one step at a time.
- Before each step, the skill searches the Campaign Database for relevant entities and proposes a pre-populated answer.
- The Director approves, refines, or rejects each answer before the skill proceeds to the next step.
- On completion, the skill writes a Session file to `campaign/sessions/` with all eight steps as sections.
- The Session file's `adventure` frontmatter field is set to the current Adventure at invocation time.

### build-encounter Skill

- Accepts a type parameter: `combat`, `negotiation`, or `montage`.
- Reads the current Adventure's index, active Subplots, and Hero files before scaffolding.
- Produces a file in the appropriate `encounters/<type>/` subdirectory with type-specific frontmatter fields.
- For Negotiations: scaffolds `patience`, `interest`, `motivations`, `pitfalls`, and an `npc` reference.
- For Montages: scaffolds `goal`, `tests`, and `success_threshold`.
- For Combat: scaffolds `monsters`, `terrain`, and `objective`.

### import-adventure Skill

- Ingests a PDF of a published adventure module.
- Extracts entities (NPCs, Locations, Encounters, Handouts, Villains) from the module text.
- Scaffolds the Adventure directory structure and writes entity files with appropriate frontmatter.
- Cross-references extracted monster names against the steel-compendium bestiary; creates Custom Monster files only for unmatched creatures.
- Sets `revealed: false` on all Handout files at import time.

### HTTP Server

- A lightweight local server (implementation TBD) that renders Campaign Database markdown files as HTML.
- Two routes: Director-facing (all content) and player-facing (only Handouts where `revealed: true`).
- Access control is driven entirely by frontmatter; no separate ACL configuration.
- Detailed design deferred — no structural decisions are made now that would close off this option.

### promote Script

- A helper script that moves an entity file from its adventure-scoped path to the campaign-scoped equivalent directory.
- Updates any `scope` or `adventure` frontmatter fields on the moved file.
- Does not update cross-references in other files automatically (that is a future enhancement).

## Testing Decisions

- Good tests verify observable behavior from the outside: does the correct directory structure get created? Does the correct file exist with the correct frontmatter? Tests should not inspect internal script logic.
- The following modules are testable in isolation and should have tests:
  - **Campaign scaffold scripts** (`new-campaign`, `new-adventure`): assert the expected directory tree and stub files are created.
  - **promote script**: assert the file appears at the campaign-scoped path, is absent from the adventure-scoped path, and the frontmatter is updated.
  - **HTTP server access control**: assert the player-facing route returns only `revealed: true` Handouts; assert the Director-facing route returns all content.
- Skills (lazy-dm, build-encounter, rules-reference, import-adventure) are LLM-driven and not suitable for deterministic unit tests. Integration testing for these is manual: invoke the skill with a known Campaign Database fixture and verify the output file is structurally correct.

## Out of Scope

- Player-initiated Downtime Projects (tracked on character sheets outside steel-golem).
- A graphical UI or web application beyond the read-only HTTP server.
- Multi-Director or collaborative Campaign management.
- Automated sync with any external platform (Foundry VTT, Roll20, D&D Beyond, etc.).
- Real-time Session tracking (e.g., live initiative order, HP tracking during play).
- Publishing or sharing Campaign content publicly.
- Support for TTRPG systems other than Draw Steel.

## Further Notes

- The steel-compendium is a git submodule at `steel-compendium/`. It is read-only from steel-golem's perspective; rules content is never written back to it.
- The CONTEXT.md glossary at the repo root is the canonical source for all domain terminology. All skills, scripts, and agents should use this vocabulary.
- The HTTP serving layer must not be designed in a way that requires Handout files to live in a separate directory from other entity files. Access control is driven by `revealed` frontmatter, not by filesystem location.
- The import-adventure skill may produce imperfect results for densely formatted PDFs; it is intended as a starting point for Director review, not a complete automated import.
- Draw Steel uses "Director" rather than "DM" or "GM". All steel-golem user-facing language should use "Director" consistently.
