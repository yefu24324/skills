# Personal Codex Skills

Language: **English** | [中文](README.zh-CN.md)

This repository maintains personal Codex skills. Each skill is a standalone directory with a required `SKILL.md` file and optional resources such as `agents/`, `scripts/`, `references/`, and `assets/`.

## Repository Layout

```text
skills/
  uutils-coreutils/
    SKILL.md
    agents/
      openai.yaml
```

When adding new personal skills, place them under `skills/<skill-name>/`. Skill names should use lowercase letters, digits, and hyphens.

## Included Skills

- `git-commit-staged`: Analyze staged changes, generate a Chinese Conventional Commit message, and commit only after confirmation.
- `git-rebase-pull`: Fetch a selected remote branch and safely rebase the current branch onto it.
- `git-push-feature`: Push HEAD to a new personal `feature/<username>` branch and open the Gitea compare page.
- `uutils-coreutils`: Prefer uutils/coreutils and related POSIX-style tools on Windows when writing or running common shell, file, and text-processing commands.

## Install With `npx skills`

Install the available skills interactively:

```bash
npx skills add https://github.com/yefu24324/skills
```

Install a specific skill:

```bash
npx skills add https://github.com/yefu24324/skills --skill uutils-coreutils
```

Restart your agent after installation so the new skill is loaded.

## Maintenance Notes

- Keep each skill directory limited to the content an agent needs to use that skill. Repository-level documentation, installation notes, and release notes belong at the repository root.
- Keep `SKILL.md` frontmatter limited to `name` and `description` for compatibility.
- After changing a skill, validate its trigger behavior and execution flow with realistic tasks in a fresh session.
