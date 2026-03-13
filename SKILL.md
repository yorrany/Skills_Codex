---
name: skills
description: Use when you need to navigate, understand, or maintain the Codex skills catalog in this repository.
metadata:
  category: reference
  triggers: skills index, skills catalog, skills repo, SKILL.md list, add skill
---

# Skills Catalog

A lightweight guide for navigating and maintaining the skills library in this repository.

## When to Use

- You need to find a skill by category or keyword
- You want to understand how skills are organized here
- You are adding or updating skills in this repository

## Quick Navigation

- Full categorized index: `SKILLS_INDEX.md`
- Per-skill instructions: `<skill-name>/SKILL.md`

## How Skills Are Organized

- Each skill is a folder containing a required `SKILL.md`
- Optional supporting files can live in `references/` or `assets/`
- Names use kebab-case and must match the `name` field in `SKILL.md`

## Adding or Updating Skills

- Keep the scope narrow and actionable
- Start descriptions with “Use when...”
- Prefer single-file skills under ~200 lines
- For large skills, split detail into `references/`

## Common Commands

```bash
rg --files -g '*/SKILL.md'
```

```bash
rg "Use when" -g '*/SKILL.md'
```
