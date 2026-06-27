# Contributing to GBA-sdk

Thanks for considering a contribution. This project aims to make GameBoy Advance homebrew development accessible from Python, so contributions can range from Python tooling to low-level C/ASM bindings — both are equally valuable.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Commit Convention](#commit-convention)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs / Requesting Features](#reporting-bugs--requesting-features)
- [Release Process](#release-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

Be respectful, constructive, and patient — especially with newcomers to GBA homebrew development. Disagreements about implementation are fine; personal attacks are not.

## Getting Started

### Prerequisites

- Python 3.x
- [devenv](https://devenv.sh/) (recommended — the repo ships `devenv.nix` / `devenv.yaml` for a reproducible toolchain), or a manual ARM GCC toolchain if you prefer not to use Nix
- An emulator for testing, [mGBA](https://mgba.io/) is the project's reference emulator

### Setup

```bash
git clone https://github.com/lukas-sgx/GBA-sdk.git
cd GBA-sdk

# Option A — devenv (recommended, matches CI environment)
devenv shell

# Option B — manual
pip install -e .
```

Verify your setup works:

```bash
cartridge hdr dump tests/fixtures/<some_rom>.gba
```

## Project Structure

| Path         | Purpose                                              |
|--------------|-------------------------------------------------------|
| `cartridge/` | ROM header parsing/validation, cartridge tooling       |
| `build/`     | Compilation pipeline (Python → ARM binary → `.gba`)    |
| `assets/`    | Project assets (logo, fixtures, etc.)                  |
| `docker/`    | Containerized toolchain for reproducible builds        |
| `tests/`     | Test suite                                             |

If you're working on a new subsystem (e.g. Video/Audio/Input bindings, asset pipeline), check the [open issues](https://github.com/lukas-sgx/GBA-sdk/issues) and the roadmap in the README first — most binding work is tracked under an `Area` label (`video`, `audio`, `input`, `asset-pipeline`, `core`).

## Development Workflow

1. Fork the repo
2. Create a branch from `main`:
   ```bash
   git checkout -b feature/short-description
   # or
   git checkout -b fix/short-description
   ```
3. Make your changes, with tests where applicable
4. Run the test suite locally (see [Testing](#testing))
5. Push and open a Pull Request using the appropriate [PR template](.github/PULL_REQUEST_TEMPLATE/)

## Commit Convention

This project follows **[Conventional Commits](https://www.conventionalcommits.org/)** — it's required, since the release process (`release-config.json` / `.release-manifest.json`) depends on commit messages to determine versioning and changelog entries.

```
<type>(<scope>): <short description>

[optional body]
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`

Examples:
```
feat(video): add draw_circle primitive for Mode 3/4/5
fix(input): correct edge detection for simultaneous key presses
docs(readme): clarify devenv setup steps
```

## Testing

- Tests live in `tests/`. Run them with your project's standard test runner before opening a PR.
- For anything touching Video/Audio/Input bindings or generated ROM behavior, **verify on mGBA** — this is a required checkbox in the PR templates and not optional for binding-related changes.
- If you're fixing a bug, add a regression test where feasible.
- Before submitting, confirm a clean local build:
  ```bash
  pipx run build
  ```

## Submitting Changes

Open your PR using the template that matches your change:

| Change type        | Template                                              |
|---------------------|--------------------------------------------------------|
| New feature          | `?template=feature.md`                                |
| Bug fix               | `?template=hotfix.md`                                  |
| Release (maintainers) | `?template=release.md`                                 |

A PR is ready for review once every checkbox in its template is checked. Reviewers may ask for changes before merging — that's normal, not a rejection.

## Reporting Bugs / Requesting Features

Please use the issue templates rather than a blank issue — they exist so triage doesn't require back-and-forth for basic info:

- **Bug report**: include reproduction steps, expected vs. actual behavior, and your environment (toolchain, emulator, Python version, hardware vs. emulator)
- **Feature request**: include scope (in/out), proposed tasks, and any dependency on existing issues

Both are available from **Issues → New issue** on GitHub.

## Release Process

*(Maintainers only — included for transparency.)*

1. Ensure all merged commits on `main` follow Conventional Commits
2. Confirm `release-config.json` / `.release-manifest.json` are up to date
3. Confirm the **Cartridge App** workflow is green on `stable`
4. Open a release PR using the `release.md` template
5. If a published release breaks downstream usage: publish a patch (`vX.Y.Z+1`) and yank the broken version on PyPI rather than force-pushing history

## Style Guidelines

- **Python**: follow the conventions already present in `cartridge/` and `build/` — match existing naming and structure rather than introducing a new style in a single PR
- **C bindings**: when interfacing directly with GBA hardware registers, use `volatile` for memory-mapped I/O, and `__attribute__((packed))` / `__attribute__((aligned(n)))` where exact memory layout matters (see existing register definitions for examples)
- **Assembly**: keep GBA-specific assembly isolated and commented — explain *why*, not just *what*, since ARM/THUMB GBA code is rarely self-explanatory to newcomers
- Keep PRs focused: one feature or fix per PR. Bundle unrelated changes only if there's no other reasonable way to split them.

---

Questions that aren't a bug or feature request can go in [Discussions](https://github.com/lukas-sgx/GBA-sdk/discussions) instead of an issue.