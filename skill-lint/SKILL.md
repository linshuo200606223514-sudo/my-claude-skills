---
name: skill-lint
description: Audit installed Claude Code skills for compliance with official best practices. Use when user wants to check skill quality, validate skills, audit skills, find skill issues, or review skill compliance. Checks frontmatter, description quality, file structure, line count, and common anti-patterns.
---

# Skill Lint

Audit all installed skills in `~/.claude/skills/` against official best practices.

## Installed skills

!`ls ~/.claude/skills/ 2>/dev/null | grep -v skills-lock.json | grep -v proj | grep -v projects | grep -v skills`

## Checklist per skill

For each skill directory found, check:

### 1. Frontmatter (SKILL.md required fields)
- [ ] `name` field present (lowercase, hyphens, max 64 chars)
- [ ] `description` field present and under 1024 chars
- [ ] Description follows formula: **What** + **Use when** triggers + **capabilities**
- [ ] No unknown frontmatter keys

### 2. File structure
- [ ] `SKILL.md` exists
- [ ] SKILL.md is under 500 lines
- [ ] No extraneous files: `README.md`, `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, `QUICK_REFERENCE.md`
- [ ] Supporting files are in `scripts/`, `references/`, or `assets/` subdirs only
- [ ] All bundled files are referenced from SKILL.md body

### 3. Content quality
- [ ] No info duplicated between SKILL.md and reference files
- [ ] No wrapper scripts for single commands
- [ ] No explanation of things Claude already knows (stdlib, common tools, basic patterns)
- [ ] Context injection (`!`backtick`command``) used where dynamic data would help

### 4. Invocation config (if present)
- [ ] `allowed-tools` only lists tools the skill actually needs
- [ ] `context: fork` paired with valid `agent` value
- [ ] `disable-model-invocation` / `user-invocable` used intentionally

## How to run the audit

1. List all skill dirs: `ls ~/.claude/skills/`
2. For each skill, read its `SKILL.md`
3. Check each item in the checklist above
4. Report findings in a table

## Output format

Produce a markdown table:

| Skill | Issues | Severity |
|-------|--------|----------|
| skill-name | description missing "Use when" | warning |
| skill-name | SKILL.md is 623 lines (over 500) | error |
| skill-name | README.md present (extraneous file) | warning |

Severity levels:
- **error** — violates a hard rule (missing SKILL.md, over 500 lines, no description)
- **warning** — best practice violation (weak description, extraneous files, no context injection)
- **info** — suggestion for improvement

End with a summary: total skills audited, errors, warnings.
