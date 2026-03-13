# Contributing

Thanks for improving the skills library. This guide covers the minimal workflow for adding or updating skills.

## Quick Checklist

- Folder name matches the `name` in `SKILL.md`
- Description starts with “Use when...”
- Scope is focused and under ~200 lines when possible
- Large skills use `references/` for extended material
- Regenerate the index: `python scripts/generate_skills_index.py`
- Run `skill-check` and `skill-scanner` when applicable

## Adding a New Skill

1. Create the folder: `my-skill-name/`
2. Add `SKILL.md` with name, description, and usage instructions
3. Add `references/` only if the skill is too large for one file
4. Run the index script to update `SKILLS_INDEX.md`

## Updating an Existing Skill

1. Keep naming consistent (folder name and `name` field)
2. Keep the description in the “Use when...” format
3. Update references only when needed
4. Regenerate the index after any skill changes

## Index Maintenance

Run this from the repo root:

```bash
python scripts/generate_skills_index.py
```

This rebuilds `SKILLS_INDEX.md` using the current categorization rules.

## CI Validation

The workflow in `.github/workflows/skills-index.yml` validates that `SKILLS_INDEX.md` is up to date. If it fails, re-run the index script and commit the updated file.

The workflow in `.github/workflows/lint.yml` validates Python lint/format (Ruff) and Markdown lint for the main docs.
