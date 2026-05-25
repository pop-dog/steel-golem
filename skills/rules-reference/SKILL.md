# rules-reference

Answer Draw Steel rules questions with citations sourced from the steel-compendium corpus.

Compendium root: `~/.steel-golem/steel-compendium/`

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
   grep -n "^#### <Term>\|^### <Term>" ~/.steel-golem/steel-compendium/Rules/Chapters/<Chapter>.md
   ```
   Then read ~60 lines from that heading.
3. For monsters, find the group directory from the Monster Groups list and read the stat block
   file(s) inside it.

**For a conceptual question:**

1. Identify the relevant chapter(s) from the Chapter Sections list in the Index.
2. Grep for the relevant `### Section` heading to get its line number:
   ```
   grep -n "^### <Section>" ~/.steel-golem/steel-compendium/Rules/Chapters/<Chapter>.md
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

## Index

_Generated from `steel-compendium`. Re-run `python3 tools/build_rules_index.py` after `git submodule update`._

### Routing Guide

| Question type | Where to look |
|---|---|
| Named condition (Slowed, Grabbed, etc.) | `Rules/Conditions/<Name>.md` |
| Movement type or interaction (Fly, Teleport, Falling, etc.) | `Rules/Movement/<Name>.md` |
| Named common ability (Charge, Grab, Hide, etc.) | `Rules/Abilities/Common/<Tier>/<Name>.md` |
| Class-specific ability | `Rules/Abilities/<ClassName>/<Level>/<Name>.md` |
| Class overview or features | `Rules/Classes/<ClassName>.md` |
| Kit | `Rules/Kits/<Name>.md` |
| Ancestry | `Rules/Chapters/Ancestries.md` |
| Negotiation motivation or pitfall | `Rules/Negotiation/Motivations and Pitfalls.md` |
| Broad rules topic (combat, tests, downtime, etc.) | `Rules/Chapters/<Chapter>.md` — grep heading, read section |
| Monster stat block or abilities | `Bestiary/Monsters/Monsters/<Group>/` |
| Rules for running monsters, keywords, traits | `Bestiary/Monsters/Chapters/Monster Basics.md` |
| Dynamic terrain rules | `Bestiary/Monsters/Chapters/Dynamic Terrain.md` |
| Retainer rules | `Bestiary/Monsters/Chapters/Retainers.md` |

### Conditions
`Rules/Conditions/<Name>.md` — one file per condition.
Bleeding, Dazed, Frightened, Grabbed, Prone, Restrained, Slowed, Taunted, Weakened

### Movement Rules
`Rules/Movement/<Name>.md` — one file per movement topic.
Big Versus Little, Burrow, Burrowing Forced Movement, Climb or Swim, Climbing Other Creatures, Crawl, Death Effects and Forced Movement, Dig Maneuver, Falling Far, Falling Onto Another Creature, Fly, Forced Into a Fall, Hover, Hurling Through Objects, Jump, Non Burrowing Creatures, Slamming Into Objects, Slamming into Creatures, Stability, Targeting Burrowing Creatures, Teleport, Vertical, Walk, When a Creature Moves

### Classes
`Rules/Classes/<Name>.md` — one file per class.
Censor, Conduit, Elementalist, Fury, Null, Shadow, Tactician, Talent, Troubadour

### Kits
`Rules/Kits/<Name>.md` — one file per kit.
Arcane Archer, Battlemind, Cloak and Dagger, Dual Wielder, Guisarmier, Kits Table, Martial Artist, Mountain, Panther, Pugilist, Raider, Ranger, Rapid Fire, Retiarius, Shining Armor, Sniper, Spellsword, Stick and Robe, Swashbuckler, Sword and Board, Warrior Priest, Whirlwind

### Abilities
`Rules/Abilities/<Class>/<Tier>/<Name>.md`

**Censor**
- 1st-Level Features: Arrest, Back Blasphemer, Behold a Shield of Faith, Behold the Face of Justice, Censored, Driving Assault, Every Step Death, Faithful Friend, Grave Speech, Halt Miscreant, Hands of the Maker, Judgment, My Life for Yours, Purifying Fire, Repent, The Gods Punish and Defend, Your Allies Cannot Save You
- 2nd-Level Features: Blessing of the Faithful, It Is Justice You Fear, Prescient Grace, Revelator, Sentenced, With My Blessing
- 3rd-Level Features: Edict of Disruptive Isolation, Edict of Perfect Order, Edict of Purifying Pacifism, Edict of Stillness
- 4th-Level Features: Blessing of Secrets
- 5th-Level Features: Gods Grant Thee Strength, Orison of Victory, Righteous Judgment, Shield of the Righteous
- 6th-Level Features: Begone, Burden of Evil, Congregation, Edict of Peace, Intercede, Pain of Your Own Making
- 7th-Level Features: Guided to Your Side, Trinity of Trickery
- 8th-Level Features: Excommunication, Hand of the Gods, Pillar of Holy Fire, Your Allies Turn on You
- 9th-Level Features: Apostate, Banish, Blessing and a Curse, Edict of Unyielding Resolve, Fulfill Your Destiny, Terror Manifest

**Common**
- Main Actions: Charge, Defend, Free Strike, Heal
- Maneuvers: Aid Attack, Catch Breath, Escape Grab, Grab, Hide, Knockback, Make or Assist a Test, Search for Hidden Creatures, Stand Up, Use Consumable
- Move Actions: Advance, Disengage, Ride

**Conduit**
- 1st-Level Features: Blessed Light, Call the Thunder Down, Corruptions Curse, Curse of Terror, Drain, Faith Is Our Armor, Faithful Friend, Font of Wrath, Grave Speech, Hands of the Maker, Healing Grace, Holy Lash, Judgments Hammer, Lightfall, Ray of Wrath, Sacrificial Offer, Sermon of Grace, Staggering Curse, Violence Will Not Aid Thee, Warriors Prayer, Wither, Word of Guidance, Word of Judgment
- 2nd-Level Features: Blessing of Fate and Destiny, Blessing of Insight, Divine Comedy, Morning Light, Nature Judges Thee, Our Hearts Your Strength, Reap, Sacred Bond, Saints Tempest, Statue of Power, The Gods Command You Obey, Wellspring of Grace
- 3rd-Level Features: Fear of the Gods, Saints Raiment, Soul Siphon, Words of Wrath and Grace
- 4th-Level Features: Beacon of Grace, Blessing of Secrets, Penance, Sanctuary, Vessel of Retribution
- 5th-Level Features: Beacon of Grace, Penance, Sanctuary, Vessel of Retribution
- 6th-Level Features: Aura of Souls, Blade of the Heavens, Blessing of the Midday Sun, Cuirass of the Gods, Gods Machine, Invocation of Mystery, Invocation of Undoing, Lauded by God, Lightning Lord, Revitalizing Grace, Spirit Stampede, Your Story Ends Here
- 7th-Level Features: Arise, Blessing of Steel, Blessing of the Blade, Drag the Unworthy, Guided to Your Side, Trinity of Trickery
- 8th-Level Features: Arise, Blessing of Steel, Blessing of the Blade, Drag the Unworthy
- 9th-Level Features: Alacrity of the Heart, Bend Fate, Blessing of the Fortress, Divine Dragon, Godstorm, Night Falls, Radiance of Grace, Righteous Phalanx, Solar Flare, Thorn Cage, Word of Final Redemption, Word of Weakening

**Elementalist**
- 1st-Level Features: Afflict a Bountiful Decay, Behold the Mystery, Bifurcated Incineration, Breath of Dawn Remembered, Conflagration, Explosive Assistance, Grasp of Beyond, Hurl Element, Instantaneous Excavation, Invigorating Growth, Meteoric Introduction, Motivate Earth, No More Than a Breeze, Practical Magic, Ray of Agonizing Self Reflection, Return to Formlessness, Ripples in the Earth, Shared Void Sense, Skin Like Castle Walls, Subtle Relocation, Test of Rain, The Flesh a Crucible, The Green Within the Green Without, Unquiet Ground, Viscous Fire
- 2nd-Level Features: O Flower Aid O Earth Defend, Subvert the Green Within, There Is No Space Between, Translated Through Flame, Volcanos Embrace
- 3rd-Level Features: Earth Accepts Me, Erase, Maw of Earth, Remember Growth and Sun and Rain, Swarm of Spirits, Wall of Fire
- 4th-Level Features: Heart of the Wode, Muse of Fire, Return to Oblivion, Summon Source of Earth, World Torn Asunder
- 5th-Level Features: Combustion Deferred, Heart of the Wode, Luminous Champion Aloft, Magma Titan, Meteor, Muse of Fire, Return to Oblivion, Storm of Sands, Subverted Perception of Space, Summon Source of Earth, The Wode Remembers and Returns, Web of All Thats Come Before, World Torn Asunder
- 6th-Level Features: Luminous Champion Aloft, Magma Titan, Meteor, The Wode Remembers and Returns
- 8th-Level Features: Earth Rejects You, Heart of the Wode, Muse of Fire, Prism, Return to Oblivion, Summon Source of Earth, The Green Defends Its Servants, Unquenchable Fire, World Torn Asunder
- 9th-Level Features: Earth Rejects You, Prism, The Green Defends Its Servants, Unquenchable Fire

**Fury**
- 1st-Level Features: Back, Blood for Blood, Brutal Slam, Furious Change, Hit and Run, Impaled, Lines of Force, Make Peace With Your God, Out of the Way, Thunder Roar, Tide of Death, To the Death, To the Uttermost End, Unearthly Reflexes, Your Entrails Are Your Extrails
- 2nd-Level Features: Apex Predator, Death Death, Phalanx Breaker, Special Delivery, Visceral Roar, Wrecking Ball
- 3rd-Level Features: Demon Unleashed, Face the Storm, Steelbreaker, You Are Already Dead
- 5th-Level Features: Debilitating Strike, My Turn, Rebounding Storm, To Stone
- 6th-Level Features: Avalanche Impact, Death Strike, Force of Storms, Pounce, Riders on the Storm, Seek and Destroy
- 8th-Level Features: Elemental Ferocity, Overkill, Primordial Rage, Relentless Death
- 9th-Level Features: Death Comes for You All, Death Rattle, Deluge, Primordial Bane, Primordial Vortex, Shower of Blood

**Kits**
- Arcane Archer: Exploding Arrow
- Battlemind: Unmooring
- Cloak and Dagger: Fade
- Dual Wielder: Double Strike
- Guisarmier: Forward Thrust Backward Smash
- Martial Artist: Battle Grace
- Mountain: Pain for Pain
- Panther: Devastating Rush
- Pugilist: Lets Dance
- Raider: Raiders Awe
- Ranger: Hamstring Shot
- Rapid Fire: Two Shot
- Retiarius: Net and Stab
- Shining Armor: Protective Attack
- Sniper: Patient Shot
- Spellsword: Leaping Lightning
- Stick and Robe: Where I Want You
- Swashbuckler: Fancy Footwork
- Sword and Board: Shield Bash
- Warrior Priest: Weakening Brand
- Whirlwind: Extension of My Arm

**Null**
- 1st-Level Features: A Squad Unto Myself, Arcane Disruptor, Chronal Spike, Dance of Blows, Faster Than the Eye, Impart Force, Inertial Shield, Inertial Step, Joint Lock, Kinetic Strike, Magnetic Strike, Null Field, Phase Inversion Strike, Phase Strike, Pressure Points, Psychic Pulse, Relentless Nemesis, Stunning Blow
- 2nd-Level Features: Blur, Entropic Field, Force Redirected, Gravitic Strike, Heat Sink, Kinetic Shield
- 3rd-Level Features: Absorption Field, Molecular Rearrangement Field, Stabilizing Field, Synapse Field
- 5th-Level Features: Anticipating Strike, Iron Grip, Phase Leap, Synaptic Reset
- 6th-Level Features: Gravitic Charge, Ice Pillars, Interphase, Iron Body, Phase Step, Wall of Ice
- 8th-Level Features: Arcane Purge, Phase Hurl, Scalar Assault, Synaptic Anchor
- 9th-Level Features: Absolute Zero, Arrestor Cycle, Heat Drain, Inertial Absorption, Realitas, Time Loop

**Shadow**
- 1st-Level Features: Black Ash Teleport, Clever Trick, Coat the Blade, Coup de Grace, Defensive Roll, Disorienting Strike, Eviscerate, Gasping in Pain, Get In Get Out, Hesitation Is Weakness, I Work Better Alone, Im No Threat, In All This Confusion, One Hundred Throats, Setup, Shadowstrike, Teamwork Has Its Place, Two Throats at Once, You Were Watching the Wrong One
- 2nd-Level Features: In a Puff of Ash, Machinations of Sound, So Gullible, Sticky Bomb, Stink Bomb, Too Slow
- 3rd-Level Features: Careful Observation, Dancer, Misdirecting Strike, Pinning Shot, Staggering Blow
- 4th-Level Features: Night Watch
- 5th-Level Features: Blackout, Into the Shadows, Shadowfall, You Talk Too Much
- 6th-Level Features: Black Ash Eruption, Cinderstorm, Look, One Vial Makes You Better, One Vial Makes You Faster, Puppet Strings
- 8th-Level Features: Assassinate, Shadowgrasp, Speed of Shadows, They Always Line Up, Time Bomb
- 9th-Level Features: Cacophony of Cinders, Chain Reaction, Demon Door, I Am You, It Was Me All Along, To the Stars

**Tactician**
- 1st-Level Features: Advanced Tactics, Battle Cry, Concussive Strike, Hammer and Anvil, Inspiring Strike, Mark, Mind Game, Now, Overwatch, Parry, Squad Forward, Strike Now, This Is What We Planned For
- 2nd-Level Features: Fog of War, Ive Got Your Back, No Dying on My Watch, Squad On Me, Targets of Opportunity, Try Me Instead
- 3rd-Level Features: Frontal Assault, Hit Em Hard, Rout, Stay Strong and Focus
- 5th-Level Features: Squad Gear Check, Squad Remember Your Training, Win This Day, Youve Still Got Something Left
- 6th-Level Features: Battle Plan, Coordinated Execution, Hustle, Instant Retaliation, Panic in Their Lines, To Me Squad
- 8th-Level Features: Finish Them, Floodgates Open, Go Now and Speed Well, Ill Open and Youll Close
- 9th-Level Features: Blot Out the Sun, Counterstrategy, No Escape, Squad Hit and Run, That One Is Mine, Their Lack of Focus Is Their Undoing

**Talent**
- 1st-Level Features: Accelerate, Again, Awe, Choke, Entropic Bolt, Feedback Loop, Flashback, Hoarfrost, Incinerate, Inertia Soak, Iron, Kinetic Grip, Kinetic Pulse, Materialize, Mind Spike, Minor Telekinesis, Optic Blast, Perfect Clarity, Precognition, Remote Assistance, Repel, Smolder, Spirit Sword
- 2nd-Level Features: Applied Chronometrics, Gravitic Burst, Levity and Gravity, Overwhelm, Slow, Synaptic Override
- 3rd-Level Features: Fling Through Time, Force Orbs, Reflector Field, Soul Burn
- 5th-Level Features: Exothermic Shield, Hypersonic, Mind Snare, Soulbound
- 6th-Level Features: Fate, Gravitic Well, Greater Kinetic Grip, Stasis Field, Synaptic Conditioning, Synaptic Dissipation
- 8th-Level Features: Doubt, Levitation Field, Mindwipe, Rejuvenate, Stasis Shield, Steel
- 9th-Level Features: Acceleration Field, Borrow From the Future, Fulcrum, Gravitic Nova, Resonant Mind Spike, Synaptic Terror

**Troubadour**
- 1st-Level Features: Acrobatics, Artful Flourish, Ballad of the Beast, Blocking, Choreography, Cutting Sarcasm, Dramatic Monologue, Dramatic Reversal, Fake Your Death, Flip the Script, Harmonize, Harsh Critic, Hypnotic Overtones, Instigator, Method Acting, Power Chord, Quick Rewrite, Revitalizing Limerick, Riposte, Star Power, Thunder Mother, Turnabout Is Fair Play, Upstage, Witty Banter
- 2nd-Level Features: Classic Chandelier Stunt, En Garde, Encore, Guest Star, Tough Crowd, Twist at the End
- 3rd-Level Features: Extensive Rewrites, Fire Up the Night, Infernal Gavotte, Never Ending Hero, Star Solo, We Meet at Last
- 5th-Level Features: Action Hero, Continuity Error, Love Song, Patter Song, Take Two, We Cant Be Upstaged
- 6th-Level Features: Blood on the Stage, Feedback, Fight Choreography, Heres How Your Story Ends, Legendary Drum Fill, Spotlight, Youre All My Understudies
- 8th-Level Features: Dramatic Reveal, Moonlight Sonata, Power Ballad, Radical Fantasia, Saved in the Edit, The Show Must Go On
- 9th-Level Features: Epic, Expert Fencer, Jam Session, Melt Their Faces, Renegotiated Contract, Rising Tension

### Chapter Sections
`Rules/Chapters/<Chapter>.md` — grep a `### Section` heading, then read that section.

**Ancestries:** On the Origin of Species, Names by Ancestry, Measurements, Starting Size and Speed, Ancestry Traits, On Devils, Devil Traits, On Dragon Knights, Dragon Knight Traits, On Dwarves, Dwarf Traits, On Wode Elves, Wode Elf Traits, On High Elves, High Elf Traits, On Hakaan, Hakaan Traits, On Humans, Human Traits, On Memonek, Memonek Traits, On Orcs, Orc Traits, On Polders, Polder Traits, Signature Trait: Shadowmeld, On Revenants, Revenant Traits, On Time Raiders, Time Raider Traits

**Background:** Why Build a Culture?, Culture Benefits, Career Questions, Career Benefits, Inciting Incident, Careers A to Z

**Classes:** Subclasses, Abilities, Basics, 1st-Level Features, 2nd-Level Features, 3rd-Level Features, 4th-Level Features, 5th-Level Features, 6th-Level Features, 7th-Level Features, 8th-Level Features, 9th-Level Features, 10th-Level Features, Stormwight Kits

**Combat:** Set the Map, Combat Round, Taking a Turn, Movement, Move Actions, Maneuvers, Main Actions, Free Strikes, Flanking, Cover, Concealment, Damage, Stamina, Underwater Combat, Suffocating, Mounted Combat, End of Combat

**Complications:** Benefit and Drawback, Modifying the Story, Choosing a Complication

**Downtime Projects:** Tracking Projects, Project Prerequisites, Project Roll, Crafting Projects, Research Projects, Other Projects

**For the Director:** What's a Campaign?, The Director's Role, Campaign Pitch, House Rules, Building the Campaign, Creating Adventures, Creating and Running Negotiations, Create and Run Montage Tests, Running Respites, Granting Rewards, Campaign: First Session

**Gods and Religion:** Churches and Temples, Interspecies Worship, Evil Gods and Saints, Afterlife in Orden, Conduits and Censors, Val, Ord, Kul, Devil Gods, Human Gods of Vasloria, Space Gods of the Timescape

**Introduction:** Tactical, Heroic, Cinematic, Fantasy, If You're Coming From D20 Fantasy

**Kits:** Changing Your Kit, Kit Equipment, Kit Bonuses and Traits, Kit Signature Ability, Kits A to Z, Optional Rule: Losing Equipment

**Making a Hero:** Your First Session, Step-by-Step Hero Making, Adventuring Gear, Changing Character Options, Heroic Advancement

**Negotiation:** When to Negotiate, Negotiation Stats, Opening a Negotiation, Uncovering Motivations, Making Arguments, NPC Response and Offer, Keep Going or Stop, Sample Negotiation

**Perks:** Perk Types, Crafting Perks, Exploration Perks, Interpersonal Perks, Intrigue Perks, Lore Perks, Supernatural Perks

**Rewards:** Found, Earned, or Crafted, Consumables, Trinkets, Leveled Treasures, Artifacts, Title Requirements, Title Echelons, Customizing Titles, How Many Titles?, Title Benefits, Granting Titles, 1st-Echelon Titles, 2nd-Echelon Titles, 3rd-Echelon Titles, 4th-Echelon Titles, Increasing Renown, Influence Negotiation, Attract Followers, Earning Wealth, Losing Wealth

**Tests:** When to Make a Test, How to Make a Test, Heroes Make Tests, Reactive Tests, Skills, Example Tests, Assist a Test, Hide and Sneak, Group Tests, Montage Tests

**The Basics:** Characteristics, Dice, Power Rolls, Hero Tokens, Game of Exceptions, Always Round Down, Creatures and Objects, Supernatural or Mundane, PCs and NPCs, Building a Heroic Narrative, Echelons of Play, Orden and the Timescape

### Monster Groups
`Bestiary/Monsters/Monsters/<Group>/` — one directory per monster group.
Ajax the Invincible, Angulotls, Animals, Arixx, Ashen Hoarder, Basilisks, Bredbeddle, Bugbears, Chimera, Count Rhodar Von Glauer, Demons, Devils, Draconians, Dragons, Dwarves, Elementals, Elves High, Elves Shadow, Elves Wode, Fossil Cryptic, Giants, Gnolls, Goblins, Griffons, Hag, Hobgoblins, Humans, Kingfissure Worm, Kobolds, Lich, Lightbenders, Lizardfolks, Lord Syuul, Manticores, Medusas, Minotaurs, Noncombatant, Ogres, Olothec, Orcs, Radenwights, Rivals, Shambling Mound, Time Raiders, Trolls, Undead, Valok, Voiceless Talkers, War Dogs, Werewolf, Wyverns, Xorannox the Tyract

### Bestiary Chapters
`Bestiary/Monsters/Chapters/<Name>.md` — rules for running monsters.
Dynamic Terrain, Monster Basics, Monsters, Retainers

