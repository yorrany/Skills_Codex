# Codex Skills Library

[![Validate Skills Index](https://github.com/yorrany/Skills_Codex/actions/workflows/skills-index.yml/badge.svg)](https://github.com/yorrany/Skills_Codex/actions/workflows/skills-index.yml)
[![Lint & Format](https://github.com/yorrany/Skills_Codex/actions/workflows/lint.yml/badge.svg)](https://github.com/yorrany/Skills_Codex/actions/workflows/lint.yml)

A curated catalog of reusable `SKILL.md` instructions for Codex/agent workflows. Each folder is a self-contained skill that teaches a specific capability, workflow, or domain.

**What this repo contains**
- A large collection of skill folders, one per capability
- A `SKILL.md` inside each folder with trigger rules and usage guidance
- Optional supporting files (references, examples, assets)

**What this repo does not contain**
- Application source code
- Runtime tooling or executables

## Quick Start

**1. Find a skill**
- Open `SKILLS_INDEX.md` for the categorized catalog
- Or search by name with `rg --files -g '*/SKILL.md'`

**2. Use a skill**
- Mention the skill name in your request (exact name or close match)
- Or phrase your request using the skill’s trigger keywords

**3. Read the skill**
- Open the skill’s `SKILL.md` for its full instructions

## Repository Structure

```
<category>/
  <subcategory>/
    <skill-name>/
      SKILL.md
      README.md              # optional
      references/            # optional
      assets/                # optional
```

## Catalog Organization

To make this library easy to navigate, skills are grouped into categories and subcategories. The full, auto-organized list lives in `SKILLS_INDEX.md`.

**Category Summary**

| Category | Skills |
| --- | ---: |
| AI & Agents | 107 |
| Backend & APIs | 91 |
| Cloud & Infra | 167 |
| Data & ML | 44 |
| Domain | 39 |
| Engineering Process | 71 |
| Frontend & UI | 106 |
| Integrations & Automation | 114 |
| Media & Creative | 16 |
| Meta | 69 |
| Mobile | 10 |
| Product & Growth | 45 |
| Security | 78 |
| Other / Uncategorized | 288 |

**Notes**
- Some skills overlap multiple domains; they are placed in the most likely discovery category.
- If you cannot find a skill by category, use text search in `SKILLS_INDEX.md`.

## Conventions

- Folder names are kebab-case and must match the `name` field inside `SKILL.md`.
- `SKILL.md` is required for every skill folder.
- Descriptions should start with “Use when...” to improve discoverability.

## Adding a New Skill

- Create a folder named after the skill: `my-skill-name/`
- Add `SKILL.md` with a clear description, triggers, and instructions
- Keep the scope focused and under 200 lines when possible
- If the skill is large, add a `references/` directory

## Suggested Workflow

- Use `writing-skills` when creating or improving skills
- Use `skill-check` to validate naming and metadata
- Use `skill-scanner` for security review when needed

## Maintenance

If you add or remove skills, update `SKILLS_INDEX.md` to keep the catalog accurate.

### Regenerate the Index

```bash
python scripts/generate_skills_index.py
```

This script scans the category/subcategory hierarchy and rebuilds `SKILLS_INDEX.md` using the current categorization rules.

## Contributing

See `CONTRIBUTING.md` for the full workflow. Quick checklist below.

- Ensure the folder name matches the `name` in `SKILL.md`
- Start the description with “Use when...”
- Keep the skill focused and under ~200 lines when possible
- Add `references/` only when necessary
- Run `python scripts/generate_skills_index.py` after changes
- Use `skill-check` and `skill-scanner` when applicable

## License

MIT. See `LICENSE`.
