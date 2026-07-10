---
description: "Prepare a new release: bump version in pyproject.toml, run linters, update deployment image tag, and draft a GitHub Release summary."
name: "Prepare Release"
argument-hint: "new version (e.g. 0.5.0)"
agent: "agent"
---

Prepare a release for the **apod-nasa** project. The new version is: **${{input}}**.

## Steps

### 1. Bump version
Update the `version` field in [pyproject.toml](../../pyproject.toml) to `${{input}}`, then run:

```sh
poetry lock
```

### 2. Run linters
Run the following commands and report any errors. Fix any issues found before proceeding.

```sh
poetry run black .
poetry run flake8 --extend-ignore=E501 $(git ls-files '*.py')
poetry run pylint --disable=C0301 $(git ls-files '*.py')
```

### 3. Update the deployment image tag
In [deploy/deployment.yml](../../deploy/deployment.yml), update the `flask-app` container image tag from its current value to `ghcr.io/ayresfonseca/apod-nasa:${{input}}`.

### 4. Draft a GitHub Release summary
Review the git log since the last tag. Group commits by their Conventional Commits prefix (`feat`, `fix`, `chore`, `refactor`, `docs`, `ci`, `build`, `perf`). Produce a concise release summary in this format:

```
## What's Changed

### ✨ Features (`feat`)
- <bullet per feat: commit>

### 🐛 Bug Fixes (`fix`)
- <bullet per fix: commit>

### 🔧 Chores & Maintenance (`chore`, `build`, `ci`, `refactor`, `docs`, `perf`)
- <bullet per remaining commit>

**Full Changelog**: https://github.com/ayresfonseca/apod-nasa/compare/<previous-tag>...v${{input}}
```

- Omit any section that has no commits.
- Strip the `type(scope):` prefix from bullet text; keep it readable.
- If a commit message does not follow Conventional Commits, place it under Chores.

## Reminder
- After this prompt completes, create a GitHub Release tagged `v${{input}}` — the [publishing-image workflow](../../.github/workflows/publishing-image.yml) triggers on `release: published` and will build and push `ghcr.io/ayresfonseca/apod-nasa:${{input}}` automatically.
- Do **not** edit `poetry.lock` or `requirements.txt` manually — Poetry manages them.
