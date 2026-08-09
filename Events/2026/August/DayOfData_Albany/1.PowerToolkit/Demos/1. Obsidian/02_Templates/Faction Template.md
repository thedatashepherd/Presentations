---
type: faction
founded:
alignment: ""
ideology: ""
enemies: []
appears_in: []
rating:
---

# {{title}}

**Founded:**
**Alignment:**
**Ideology:**
**Enemies:**

## Overview


## Origins


## Core Beliefs


## Hierarchy


## In Games


## Technology / Resources


## Philosophy


## Conflicts


## Related


---

## ⚔️ Enemy Factions (Dataview)

```dataview
TABLE alignment, ideology, founded, rating
FROM ""
WHERE type = "faction" AND file.name != this.file.name
SORT alignment ASC
```

## 👤 Known Members

```dataview
TABLE actor, role
FROM ""
WHERE type = "character" AND contains(affiliation, this.file.name)
SORT rating DESC
```
