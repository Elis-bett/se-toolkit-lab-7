# Repository configuration

<h2>Table of contents</h2>

- [1. Repository structure](#1-repository-structure)
- [2. Artifact inventory](#2-artifact-inventory)
  - [2.1. Documentation](#21-documentation)
  - [2.2. Version control](#22-version-control)
  - [2.3. Editor and linting](#23-editor-and-linting)
  - [2.4. Development environment](#24-development-environment)
  - [2.5. GitHub](#25-github)
  - [2.6. Docker and deployment](#26-docker-and-deployment)
  - [2.7. Agent configuration](#27-agent-configuration)
  - [2.8. Other](#28-other)
- [3. Change management](#3-change-management)
  - [3.1. Keeping artifacts in sync](#31-keeping-artifacts-in-sync)
  - [3.2. Lock files](#32-lock-files)
  - [3.3. Generated and cached files](#33-generated-and-cached-files)
  - [3.4. Modifying templates and workflows](#34-modifying-templates-and-workflows)
  - [3.5. Updating Docker configuration](#35-updating-docker-configuration)
- [4. GitHub templates](#4-github-templates)
  - [4.1. Issue templates](#41-issue-templates)
    - [4.1.1. `01-task.yml` — Lab Task](#411-01-taskyml--lab-task)
    - [4.1.2. `02-bug-report.yml` — Bug Report](#412-02-bug-reportyml--bug-report)
    - [4.1.3. `config.yml`](#413-configyml)
  - [4.2. PR template (`pull_request_template.md`)](#42-pr-template-pull_request_templatemd)
- [5. VS Code settings (`.vscode/settings.json`)](#5-vs-code-settings-vscodesettingsjson)
- [6. VS Code recommended extensions (`.vscode/extensions.json`)](#6-vs-code-recommended-extensions-vscodeextensionsjson)
  - [6.1. Rules for extensions](#61-rules-for-extensions)
- [7. Task runner and package manager config](#7-task-runner-and-package-manager-config)
  - [7.1. Rules for task runner](#71-rules-for-task-runner)
- [8. Docker and deployment pattern](#8-docker-and-deployment-pattern)
- [9. Agent configuration (`AGENTS.md`)](#9-agent-configuration-agentsmd)
  - [9.1. File layout](#91-file-layout)
  - [9.2. `AGENTS.md` structure](#92-agentsmd-structure)
  - [9.3. Creating symlinks](#93-creating-symlinks)
- [10. Checklist before publishing](#10-checklist-before-publishing)

Use this file when configuring the repository structure, templates, editor settings, and deployment infrastructure. It also covers change management — how to keep artifacts in sync when something changes, and a pre-publish checklist to verify everything is in order.

---

## 1. Repository structure

Create the following directory and file layout. Items marked *(conditional)* are included only when the lab needs them.

```text
<repo-root>/
├── README.md                          # Main entry point
├── AGENTS.md                          # Agent/AI coding assistant configuration (canonical)
├── CLAUDE.md -> AGENTS.md             # Symlink (Claude)
├── QWEN.md -> AGENTS.md               # Symlink (Qwen)
├── index.md                           # Repository index
├── LICENSE                            # License file
├── lab/
│   ├── tasks/
│   │   ├── setup.md                   # Full first-time lab setup
│   │   ├── setup-simple.md            # Lab-specific setup (returning students)
│   │   ├── required/
│   │   │   ├── task-1.md
│   │   │   ├── task-2.md
│   │   │   └── ...
│   │   └── optional/
│   │       ├── task-1.md
│   │       └── ...
│   └── images/                        # Task-specific screenshots and diagrams
│       └── ...
├── wiki/                              # Reference docs for tools & concepts
│   ├── vs-code.md
│   ├── git.md
│   ├── git-workflow.md                # Reusable Git workflow procedure
│   ├── git-vscode.md
│   ├── github.md
│   ├── shell.md
│   ├── ...                            # One file per tool/concept
│   └── images/                        # Wiki screenshots organized by tool
│       ├── vs-code/
│       ├── gitlens/
│       └── ...
├── contributing/                      # Lab authoring conventions
│   ├── configuration.md               # Repo structure, templates, settings, deployment, checklist
│   └── conventions/                   # Detailed conventions by topic
│       ├── agents/
│       ├── git/
│       ├── implementation/
│       ├── meetings/
│       └── writing/
├── docs/                              # Application architecture docs (conditional)
│   ├── design/                        # Architecture and domain model
│   └── requirements/                  # Vision and requirements
├── instructors/                       # Internal design notes (not student-facing)
│   ├── README.md
│   ├── course.md
│   ├── ideas.md
│   ├── meetings/                      # Lab meeting notes and transcripts
│   ├── file-reviews/                  # Review findings for lab files
│   └── scripts/                       # Utility scripts
├── .agents/                           # Agent skill definitions (canonical)
│   └── skills/                        # One subdirectory per skill
├── .claude -> .agents                 # Symlink (Claude)
├── .qwen -> .agents                   # Symlink (Qwen)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01-task.yml                # Lab Task issue form
│   │   ├── 02-bug-report.yml          # Bug Report issue form
│   │   └── config.yml                 # blank_issues_enabled: false
│   ├── pull_request_template.md       # PR template with checklist
│   └── workflows/                     # GitHub Actions (optional)
├── .vscode/
│   ├── settings.json                  # Editor, formatter, ToC settings
│   └── extensions.json                # Recommended VS Code extensions
├── backend/                           # Application source code (conditional)
├── frontend/                          # Application source code (conditional)
├── caddy/                             # Reverse proxy config (conditional — only if using Docker)
│   └── Caddyfile
├── .gitignore
├── .gitattributes                     # Line ending normalization and binary markers
├── .markdownlint.jsonc                # Markdown linting rules
├── .env.example                       # Template for local env vars (conditional)
├── .env.docker.example                # Template for Docker env vars (conditional)
├── .env.tests.unit.example            # Template for unit test env vars (conditional)
├── .env.tests.e2e.example             # Template for e2e test env vars (conditional)
├── .dockerignore                      # (conditional — only if using Docker)
├── Dockerfile                         # (conditional — only if using Docker)
├── docker-compose.yml                 # (conditional — only if using Docker)
└── <package-manager-config>           # e.g., pyproject.toml, package.json
```

---

## 2. Artifact inventory

This section explains what each configuration artifact exists for and why it is included in the repository.

### 2.1. Documentation

- [`README.md`](../README.md) — Lab entry point. Contains the course name, lab title, learning outcomes, and links to tasks. Students see this first when they open the repository.
- [`index.md`](../index.md) — Navigation hub. Provides a categorized index of all lab tasks, source code files, infrastructure, and wiki articles. Authors and agents use it to locate any file quickly.
- [`lab/tasks/`](../lab/tasks/) — Student-facing lab instructions. Contains setup guides ([`setup-full.md`](../lab/setup/setup-full.md), [`setup-simple.md`](../lab/setup/setup-simple.md)) and numbered task files that students follow to complete the lab.
- [`wiki/`](../wiki/) — Reference documentation. One file per tool or concept (e.g., `git.md`, `docker.md`). Tasks link here when introducing a concept; students return here to look up details.
- [`contributing/`](../contributing/) — Lab authoring conventions. Defines how authors write tasks, wiki articles, and configure the repository. Not student-facing.
- [`docs/`](../docs/) — Application architecture *(conditional)*. Contains design documents (C4 architecture, domain model) and requirements (vision statement). Included only when the lab has a code project.
- [`instructors/`](../instructors/) — Internal design notes, meeting reports, file reviews, and utility scripts. Not student-facing and not subject to lab authoring conventions.

### 2.2. Version control

- [`.gitignore`](../.gitignore) — Excludes generated files (`.venv/`, `__pycache__/`, `.direnv/`), secrets (`*.secret`), tool caches (`.ruff_cache/`, `.pytest_cache/`), and temporary files (`tmp/`) from version control.
- [`.gitattributes`](../.gitattributes) — Normalizes line endings to LF (`* text=auto eol=lf`) and marks binary files (`*.png`, `*.pdf`) so `Git` handles them correctly across operating systems.
- [`.gitmodules`](../.gitmodules) — Defines `Git` submodules (e.g., `instructors/meetings` pointing to a separate meetings repository). Included only when submodules are used.

### 2.3. Editor and linting

- [`.vscode/settings.json`](../.vscode/settings.json) — Configures auto-save, format-on-save, language-specific formatters, and Markdown preview behavior. Ensures all contributors use consistent editor settings. See [VS Code settings](#5-vs-code-settings-vscodesettingsjson) for the canonical configuration.
- [`.vscode/extensions.json`](../.vscode/extensions.json) — Lists recommended `VS Code` extensions grouped by purpose. Students install them via `Extensions` > `Filter` > `Recommended`. See [VS Code recommended extensions](#6-vs-code-recommended-extensions-vscodeextensionsjson) for the canonical list.
- [`.markdownlint.jsonc`](../.markdownlint.jsonc) — Relaxes Markdown linting rules for educational content (allows inline HTML, disables line length limit, permits flexible code fence styles).

### 2.4. Development environment

- [`flake.nix`](../flake.nix) — Defines a reproducible Nix development shell with all required tools (Node.js, `uv`, `lychee`, `markdownlint-cli2`) and lint scripts *(conditional)*. Contributors enter the environment automatically via `direnv`.
- [`flake.lock`](../flake.lock) — Locks exact versions of Nix inputs for reproducibility *(conditional)*. Generated by `nix flake update`.
- [`.envrc`](../.envrc) — Activates the Nix development shell when entering the directory (via `direnv`) *(conditional)*. Contains only `use flake`.
- `<package-manager-config>` (e.g., [`pyproject.toml`](../pyproject.toml), `package.json`) — Declares project metadata, dependencies, dev dependencies, task runner commands, and tool configurations. See [Task runner and package manager config](#7-task-runner-and-package-manager-config).
- `<lock-file>` (e.g., [`uv.lock`](../uv.lock), `package-lock.json`) — Locks exact versions of language-specific dependencies. Generated by the package manager. See [Lock files](#32-lock-files).
- [`.env.docker.example`](../.env.docker.example) — Template for `Docker Compose` environment variables *(conditional)*. Students copy to `.env.docker.secret`.
- [`.env.tests.unit.example`](../.env.tests.unit.example), [`.env.tests.e2e.example`](../.env.tests.e2e.example) — Templates for test environment variables *(conditional)*.

### 2.5. GitHub

- [`.github/ISSUE_TEMPLATE/01-task.yml`](../.github/ISSUE_TEMPLATE/01-task.yml) — Structured form for lab task issues. Requires a goal description and a plan with a checklist. See [Issue templates](#41-issue-templates).
- [`.github/ISSUE_TEMPLATE/02-bug-report.yml`](../.github/ISSUE_TEMPLATE/02-bug-report.yml) — Structured form for bug reports. Requires problem description, reproduction steps, expected result, and actual result.
- [`.github/ISSUE_TEMPLATE/config.yml`](../.github/ISSUE_TEMPLATE/config.yml) — Disables blank issues to enforce use of templates.
- [`.github/pull_request_template.md`](../.github/pull_request_template.md) — PR checklist ensuring students target their fork's `main` branch, link an issue, and self-review. See [PR template](#42-pr-template-pull_request_templatemd).
- [`.github/workflows/`](../.github/workflows/) — CI and automation workflows *(conditional)*: documentation linting, broken link checking, auto-closing fork PRs and task issues opened against the instructor repository.

### 2.6. Docker and deployment

All items in this category are conditional — include only when the lab involves containerization or remote deployment. See [Docker and deployment pattern](#8-docker-and-deployment-pattern) for the full pattern.

- [`Dockerfile`](../Dockerfile) — Multi-stage build for the application. Builder stage installs dependencies; final stage runs as a non-root user. Uses the institutional container registry for base images.
- [`docker-compose.yml`](../docker-compose.yml) — Orchestrates services (e.g., `app`, `postgres`, `pgadmin`, `caddy`). All ports and credentials are parameterized via environment variables from `.env.docker.secret`.
- [`.dockerignore`](../.dockerignore) — Excludes tests, docs, Markdown files, `.git/`, and caches from the Docker build context to keep images small.
- [`caddy/Caddyfile`](../caddy/Caddyfile) — Reverse proxy routing. Forwards API paths to the backend and serves static frontend files.

### 2.7. Agent configuration

- [`AGENTS.md`](../AGENTS.md) — Canonical agent instructions. Points agents to the correct convention files for each part of the repository. [`CLAUDE.md`](../CLAUDE.md) and [`QWEN.md`](../QWEN.md) are symlinks to this file. See [Agent configuration](#9-agent-configuration-agentsmd).
- [`.agents/skills/`](../.agents/skills/) — Skill definitions (one subdirectory per skill, each with a `SKILL.md`). [`.claude/`](../.claude/) and [`.qwen/`](../.qwen/) are symlinks to [`.agents/`](../.agents/).
- `.agents/settings.local.json` — Permission allowlist for agent tools. Machine-specific, not committed to version control.

### 2.8. Other

- [`LICENSE`](../LICENSE) — License file (e.g., MIT). Defines the terms under which the repository can be used and shared.

---

## 3. Change management

### 3.1. Keeping artifacts in sync

Several artifacts must stay in sync when changes are made:

- **Agent symlinks:** [`CLAUDE.md`](../CLAUDE.md) and [`QWEN.md`](../QWEN.md) must remain symlinks to [`AGENTS.md`](../AGENTS.md). [`.claude/`](../.claude/) and [`.qwen/`](../.qwen/) must remain symlinks to [`.agents/`](../.agents/). Never edit the symlinks directly — edit the canonical files.
- **Dependencies and lock files:** When adding or removing a dependency in the package manager config, regenerate the lock file and commit both together. See [Lock files](#32-lock-files).
- **Environment templates:** When the application reads a new environment variable, add it to all relevant `.env.*.example` files. Update [`docker-compose.yml`](../docker-compose.yml) if the variable is used in container configuration.
- **Repository structure diagram:** When adding a new top-level directory or file, update the tree in [Repository structure](#1-repository-structure).
- **Index:** When adding a new wiki article, task, or infrastructure file, add an entry to [`index.md`](../index.md).
- **VS Code extensions:** When adding a tool that benefits from an extension, add it to [`.vscode/extensions.json`](../.vscode/extensions.json) with a `//` group comment.
- **Checklist:** When adding a new category of artifact, add a verification item to the [Checklist before publishing](#10-checklist-before-publishing).

### 3.2. Lock files

Lock files pin exact dependency versions for reproducibility. They are generated — never edit them by hand.

- [`uv.lock`](../uv.lock) — regenerated by `uv sync` or `uv lock`.
- [`flake.lock`](../flake.lock) — regenerated by `nix flake update` (all inputs) or `nix flake lock --update-input <name>` (single input).
- `pnpm-lock.yaml` — regenerated by `pnpm install`.

Commit lock files alongside the config file that triggered the change.

### 3.3. Generated and cached files

These files are generated at build or runtime and must not be committed (excluded via `.gitignore`):

- `.venv/` — Python virtual environment (created by `uv sync`).
- `.direnv/` — direnv output (created by `direnv allow`).
- `__pycache__/` — Python bytecode cache.
- `.ruff_cache/`, `.pytest_cache/` — Tool caches.
- `*.secret` — Environment files with real credentials.
- `tmp/` — Temporary working files.
- `.agents/settings.local.json` — Agent permission settings (machine-specific).

### 3.4. Modifying templates and workflows

- **Issue templates:** Edit files in [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/). Keep [`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) with `blank_issues_enabled: false` unless blank issues are specifically needed.
- **PR template:** Edit [`.github/pull_request_template.md`](../.github/pull_request_template.md). Ensure the checklist remains relevant to the lab's workflow.
- **CI workflows:** Create or edit files in [`.github/workflows/`](../.github/workflows/). Use a consistent runner (e.g., `ubuntu-24.04-arm`). Cache expensive steps (Nix store, pnpm store). Test on a branch before merging to `main`.

### 3.5. Updating Docker configuration

- **[`Dockerfile`](../Dockerfile):** Keep the multi-stage build pattern. Pin base image versions. Use the institutional container registry for base images.
- **[`docker-compose.yml`](../docker-compose.yml):** Parameterize all ports and credentials via environment variables. Add `required` validation for new variables. Keep health checks on database services.
- **Caddyfile:** Add new route entries when new API endpoints are introduced.

---

## 4. GitHub templates

> The descriptions below define the canonical starting point. The actual files in [`.github/`](../.github/) may include lab-specific additions.

### 4.1. Issue templates

#### 4.1.1. [`01-task.yml`](../.github/ISSUE_TEMPLATE/01-task.yml) — Lab Task

A structured form for tracking lab task work. Configuration:

- Title prefix: `[Task] <short title>`. Label: `task`.
- `description` textarea (required) — Summarize what the task is about in own words.
- `steps` textarea (required) — Plan with a checklist of steps to complete.

#### 4.1.2. [`02-bug-report.yml`](../.github/ISSUE_TEMPLATE/02-bug-report.yml) — Bug Report

Same structure as [`01-task.yml`](../.github/ISSUE_TEMPLATE/01-task.yml). Required fields:

- `Brief problem description`
- `Steps to Reproduce`
- `Expected Result`
- `Actual Result`

#### 4.1.3. [`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)

Set `blank_issues_enabled: false` to enforce use of templates.

### 4.2. PR template ([`pull_request_template.md`](../.github/pull_request_template.md))

The PR template must include:

- A `## Summary` section with `- Closes #<issue-number>`.
- A `## Checklist` section verifying that the student:
  - Made the PR to the `main` branch of their fork (not the instructor repo).
  - Sees `base: main` ← `compare: <branch>` above the PR title.
  - Edited the `Closes #<issue-number>` line.
  - Wrote clear commit messages.
  - Reviewed their own diff before requesting review.
  - Understands the changes being submitted.

---

## 5. VS Code settings ([`.vscode/settings.json`](../.vscode/settings.json))

> The settings below define the canonical starting point. The actual file in [`.vscode/`](../.vscode/) may include lab-specific additions.

Configure the following settings:

- `git.autofetch: true` — Automatically fetch remote changes.
- `files.autoSave: "afterDelay"` with `files.autoSaveDelay: 500` — Auto-save after 500 ms.
- `editor.formatOnSave: true` — Format files on save.
- `[markdown]` default formatter: `DavidAnson.vscode-markdownlint`.
- `markdown.extension.toc.levels: "2..6"` — Exclude `h1` from auto-generated TOC.
- `workbench.sideBar.location: "right"` — Move sidebar to the right.
- Disable `markdown.preview.scrollEditorWithPreview` and `markdown.preview.scrollPreviewWithEditor`.

Add language-specific formatter settings as needed (e.g., Python with Ruff, JS with Prettier).

---

## 6. VS Code recommended extensions ([`.vscode/extensions.json`](../.vscode/extensions.json))

> The extension list below defines the canonical starting point. The actual file in [`.vscode/`](../.vscode/) may include lab-specific additions.

Group recommended extensions by purpose:

- **Language support** — Adjust per lab: Python, Node.js, Go, Rust, etc.
- **Git** — `eamodio.gitlens`.
- **Remote development** — `ms-vscode-remote.remote-ssh` (if lab uses SSH/VMs/containers).
- **Markdown** — `DavidAnson.vscode-markdownlint`, `yzhang.markdown-all-in-one`.
- **GitHub integration** — `github.vscode-pull-request-github`.
- **File format support** — Include what the lab uses (e.g., `tamasfe.even-better-toml`).
- **Utilities** — `usernamehw.errorlens`, `gruntfuggly.todo-tree`, `ms-vsliveshare.vsliveshare`.

### 6.1. Rules for extensions

- Group extensions by purpose with `//` comments.
- Include extensions for: the lab's programming language, Git, remote development, Markdown, GitHub, and relevant file formats.
- The setup doc instructs students to install these via `Extensions` > `Filter` > `Recommended` > `Install Workspace Recommended extensions`.

---

## 7. Task runner and package manager config

Define common project commands using a task runner so students run simple commands rather than remembering complex CLI invocations.

Choose a task runner appropriate for the lab's ecosystem:

- **Python**: [`pyproject.toml`](../pyproject.toml) + [`poethepoet`](https://poethepoet.natn.io/) (run via `uv run poe <task>`)
- **Node.js**: `package.json` scripts (run via `pnpm run <task>`)
- **Go / Rust / other**: `Makefile` or `Taskfile.yml` (run via `make <task>` or `task <task>`)

Define at minimum these standard tasks: `dev` (run checks then start), `start` (start the server), `check` (format + lint), `test` (run test suite). Add `format` and `lint` as separate tasks when the lab includes static analysis.

### 7.1. Rules for task runner

- Students run a single short command (e.g., `uv run poe dev`, `pnpm run dev`) — no need to memorize raw commands.
- Document task runner commands in `> [!NOTE]` blocks the first time they appear:

  ```markdown
  > [!NOTE]
  > `<runner>` can run tasks specified in the `<config-file>`.
  ```

---

## 8. Docker and deployment pattern

> Include this section only if the lab involves containerization or remote deployment. Omit the Docker/deployment files from the repository structure if not needed.

If the lab involves deployment:

1. Provide [`.env.docker.example`](../.env.docker.example) as templates.
2. Students copy them to `.env.secret` and `.env.docker.secret` (which are `.gitignore`d via the `*.secret` pattern).
3. Use [`docker-compose.yml`](../docker-compose.yml) with environment variable substitution from `.env.docker.secret` (e.g., `${APP_HOST_PORT}`). Parameterize all ports, host addresses, and credentials.
4. Include a reverse proxy service (e.g., Caddy) in [`docker-compose.yml`](../docker-compose.yml).
5. Use a multi-stage [`Dockerfile`](../Dockerfile) for production builds (builder stage + slim runtime).
6. Deployment task flow: SSH into VM → clone repo → create `.env.docker.secret` → `docker compose up --build -d`.
7. Distinguish local vs remote env differences:
   - Local: `APP_HOST_ADDRESS=127.0.0.1` (localhost only).
   - Remote: `LMS_API_HOST_ADDRESS=0.0.0.0` (accessible from outside).
8. **Use an institutional container registry** (e.g., Harbor cache proxy) for base images to avoid Docker Hub rate limits. Reference the registry in [`docker-compose.yml`](../docker-compose.yml) image fields instead of pulling directly from Docker Hub.

---

## 9. Agent configuration ([`AGENTS.md`](../AGENTS.md))

The repository uses a single canonical agent configuration file that all AI coding assistants read.

### 9.1. File layout

```text
<repo-root>/
├── AGENTS.md                  # Canonical agent configuration (edit this file)
├── CLAUDE.md -> AGENTS.md     # Symlink — Claude reads this
├── QWEN.md -> AGENTS.md       # Symlink — Qwen reads this
└── .agents/
    ├── settings.local.json    # Agent tool-permission settings (not committed)
    └── skills/
        └── <skill-name>/
            └── SKILL.md       # One skill per subdirectory
```

Agent tool directories ([`.claude/`](../.claude/), [`.qwen/`](../.qwen/)) are symlinks to [`.agents/`](../.agents/) so all agents share the same skill definitions.

### 9.2. [`AGENTS.md`](../AGENTS.md) structure

[`AGENTS.md`](../AGENTS.md) is the single source of truth for agent instructions. Structure it with:

- `##` sections keyed to the action (e.g., `When editing X`).
- Each section lists the relevant convention files to read before making changes.
- [`CLAUDE.md`](../CLAUDE.md) and [`QWEN.md`](../QWEN.md) are symlinks — never edit them directly; edit [`AGENTS.md`](../AGENTS.md).

### 9.3. Creating symlinks

```bash
ln -s AGENTS.md CLAUDE.md
ln -s AGENTS.md QWEN.md
ln -s .agents .claude
ln -s .agents .qwen
```

---

## 10. Checklist before publishing

- [ ] [`AGENTS.md`](../AGENTS.md) exists at repo root with [`CLAUDE.md`](../CLAUDE.md) and [`QWEN.md`](../QWEN.md) as symlinks to it.
- [ ] All cross-references use relative paths and are valid.
- [ ] Issue templates ([`01-task.yml`](../.github/ISSUE_TEMPLATE/01-task.yml), [`02-bug-report.yml`](../.github/ISSUE_TEMPLATE/02-bug-report.yml)) are configured.
- [ ] PR template has a checklist.
- [ ] [`.vscode/settings.json`](../.vscode/settings.json) and [`.vscode/extensions.json`](../.vscode/extensions.json) are configured.
- [ ] [`.gitignore`](../.gitignore) excludes generated files and secrets for the lab's ecosystem.
- [ ] [`.gitattributes`](../.gitattributes) normalizes line endings and marks binary files.
- [ ] [`index.md`](../index.md) links to all lab tasks, source code, infrastructure, and wiki articles.
- [ ] Branch protection rules are documented.

**Conditional (include when applicable):**

- [ ] [`.env.docker.example`](../.env.docker.example) file is provided; `.env.secret` files are gitignored (if the lab uses environment variables).
- [ ] [`.dockerignore`](../.dockerignore) excludes tests, docs, `.git/`, build caches, markdown files (if the lab uses Docker).
- [ ] Task runner commands are documented in the config file (if the lab uses a task runner).
- [ ] Docker images use an institutional container registry (if the lab uses Docker in an institutional setting).
- [ ] Lock files are committed alongside their config files (if the lab uses a package manager).
