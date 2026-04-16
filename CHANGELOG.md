# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-04-15

### Fixed

- **README example** `DurninWomersley` quick-start used `skinfolds=` keyword argument, which raised `TypeError` against the `*args` signature. Switched to positional form.
- **`ActivityLevel` documentation** `docs-library/meal-planning.md` listed `"light"` and `"extra"` as accepted values; only `"sedentary"`, `"moderate"`, and `"very"` exist on the enum. Corrected the accepted-values table.

### Changed

- **Author metadata** updated to `jeffallan` (https://jeffallan.github.io); removes stale attribution from the original v0.1.x package author.
- **Package description** and marketing copy reframed from "ACSM-sourced equations" to "validated, research-backed equations" across README, PyPI description, marketplace metadata, and the docs site landing page. Deep scholarly references (equation-source citations in reference docs) kept intact.
- **README header** new capsule-render banner (sky blue → amber gradient), stats line, and shields.io badge row (PyPI version, Python versions, license, Claude Code Plugin, stars, CI). Matches style of sibling repos.
- **Docs-site landing page** real install commands (`/plugin marketplace add` + `npx skills add`) replace the stub `claude install` command.
- Terminology unified on **"Agent Skills"** (capitalized) across README and docs site.

### Infrastructure

- **Release workflow** `actions/configure-pages@v5` now passes `enablement: true` so GitHub Pages auto-initializes on first run; future releases don't require manual Pages-enable gymnastics.
- **CI** now triggers on PRs to `develop` (previously master-only) and declares `workflow_call` so `release.yml` can reuse it.
- **Package build config** explicit `[tool.setuptools.packages.find]` ensures only `fitness_tools/` ships; prevents `site/`, `skills/`, and `docs-library/` from confusing setuptools flat-layout auto-discovery.

## [1.0.0] - 2026-02-27

### Added

- **Type system:** `StrEnum` enums (`Sex`, `BodyType`, `ActivityLevel`, `Goal`) replace raw strings
- **Frozen dataclasses:** `BodyCompositionResult`, `MacroTargets`, `RepEstimate` for structured return values
- **Centralized validation module** (`fitness_tools/validation.py`) with shared input checks
- **CI pipeline:** GitHub Actions with ruff linting, mypy strict type checking, and pytest matrix (Python 3.11/3.12/3.13)
- **Claude skills plugin:** 3 specialized skills (body-composition, rep-max, meal-planner) with YAML frontmatter and reference files
- **Documentation site:** Astro + Starlight on GitHub Pages, replacing Sphinx/Read the Docs
- **`py.typed` marker** for PEP 561 typed package support

### Fixed

- **11-rep bug:** `RM_Estimator` now correctly handles 11 repetitions (was off-by-one in percentage table lookup)

### Changed

- Migrated build system from `setup.py` to `pyproject.toml`
- All documentation converted from RST to Markdown
- Minimum Python version raised to 3.11 (from 3.6)
- Package status promoted to "Production/Stable"

## [0.1.1] - 2018-07-28

### Fixed

- Links in README

## [0.1.0] - 2018-07-27

### Added

- Initial release
- Body composition calculations (Durnin-Womersley, Jackson-Pollock 3/4/7-site)
- Rep max estimation using ACSM percentage table
- Macronutrient meal planning by body type
