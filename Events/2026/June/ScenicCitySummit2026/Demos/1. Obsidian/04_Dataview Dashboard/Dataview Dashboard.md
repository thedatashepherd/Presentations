---
type: dashboard
tags:
  - dashboard
  - dataview
---

# 🗂️ Fallout Vault — Dataview Dashboard

---



## 🎮 Games & Media

```dataview
TABLE release_year AS "Year", developer AS "Developer", setting AS "Setting", rating AS "⭐"
FROM ""
WHERE type = "game" OR type = "tv-series"
SORT release_year ASC
```

---

## 🏛️ Factions

```dataview
TABLE alignment AS "Alignment", ideology AS "Ideology", founded AS "Founded", rating AS "⭐"
FROM ""
WHERE type = "faction"
SORT rating DESC
```

---

## 📍 Locations

```dataview
TABLE location_type AS "Type", state AS "State", appears_in AS "Appears In", rating AS "⭐"
FROM ""
WHERE type = "location"
SORT rating DESC
```

---

## 👥 All Characters

```dataview
TABLE actor AS "Actor", affiliation AS "Affiliation", role AS "Role", rating AS "⭐"
FROM ""
WHERE type = "character"
SORT rating DESC
```

---

## 🧬 Species

```dataview
TABLE origin AS "Origin", alignment AS "Alignment", rating AS "⭐"
FROM ""
WHERE type = "species"
SORT rating DESC
```

---

## 🔧 Items & Technology

```dataview
TABLE item_type AS "Type", manufacturer AS "Manufacturer", rating AS "⭐"
FROM ""
WHERE type = "item"
SORT rating DESC
```

---

## ⚡ Top Rated Notes

```dataview
TABLE type AS "Type", rating AS "⭐"
FROM ""
WHERE rating >= 5 AND type != "dashboard" AND type != "overview"
SORT type ASC
```

---

## 📅 Timeline of Events

```dataview
TABLE date AS "Date", outcome AS "Outcome"
FROM ""
WHERE type = "event"
SORT date ASC
```

---

## 🌐 Full Vault Index

```dataview
TABLE type AS "Type", rating AS "⭐"
FROM ""
WHERE type != "dashboard"
SORT type ASC, file.name ASC
```
