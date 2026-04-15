# Changelog

All notable changes to this project will be documented in this file.

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
