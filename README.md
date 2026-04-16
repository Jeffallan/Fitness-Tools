<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:03A9F4,100:FFB300&height=200&section=header&text=Fitness%20Tools&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Python%20Package%20%2B%20Agent%20Skills%20for%20Health%20%26%20Performance&descSize=20&descAlignY=55" width="100%" alt="Fitness Tools" />
</p>

<p align="center">
  Python Package · <!-- SKILL_COUNT -->3<!-- /SKILL_COUNT --> Agent Skills
</p>

<p align="center">
  <a href="https://pypi.org/project/fitness-tools/"><img src="https://img.shields.io/pypi/v/fitness-tools?style=for-the-badge&color=blue" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/fitness-tools/"><img src="https://img.shields.io/pypi/pyversions/fitness-tools?style=for-the-badge" alt="Python versions" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-green.svg?style=for-the-badge" alt="License" /></a>
  <a href="https://github.com/Jeffallan/Fitness-Tools"><img src="https://img.shields.io/badge/Claude_Code-Plugin-purple.svg?style=for-the-badge" alt="Claude Code Plugin" /></a>
  <a href="https://github.com/Jeffallan/Fitness-Tools/stargazers"><img src="https://img.shields.io/github/stars/Jeffallan/Fitness-Tools?style=for-the-badge&color=yellow" alt="GitHub Stars" /></a>
  <a href="https://github.com/Jeffallan/Fitness-Tools/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Jeffallan/Fitness-Tools/ci.yml?branch=master&style=for-the-badge&label=CI" alt="CI" /></a>
</p>

---

Fitness Tools is a Python package that facilitates healthy lifestyles using validated, research-backed equations. Whether you're a wellness professional, veteran gym rat, or just starting your fitness journey, this package will benefit you.

## Features

- **Body Composition** — Estimate body fat percentage from skinfold measurements using Durnin-Womersley and Jackson-Pollock (3/4/7-site) equations
- **Rep Max Estimation** — Convert between weight and rep ranges using a validated percentage-of-1RM table
- **Macronutrient Planning** — Calculate daily calorie ranges and macro distributions by body type, activity level, and goal

## Quick Start

No third-party dependencies. Python 3.11+ only.

```bash
pip install fitness-tools
```

### Body Composition

```python
from fitness_tools import DurninWomersley, Sex

calc = DurninWomersley(age=30, sex=Sex.MALE, skinfolds=(12, 8, 15, 10))
density = calc.body_density()
body_fat = calc.siri(density)
```

### Rep Max Estimation

```python
from fitness_tools import RM_Estimator

est = RM_Estimator(current_weight=185.0, current_reps=8, desired_reps=1)
result = est.estimate_weight(base=2.5)
```

### Macronutrient Planning

```python
from fitness_tools import MakeMeal, BodyType, ActivityLevel, Goal

meal = MakeMeal(
    weight=150,
    body_type=BodyType.MESOMORPH,
    activity_level=ActivityLevel.VERY,
    goal=Goal.MAINTENANCE,
)
daily = meal.daily_requirements()
per_meal = meal.make_meal(number_meals=5)
```

## API

All public types are importable from `fitness_tools`:

| Category | Classes |
|----------|---------|
| Body Composition | `DurninWomersley`, `JacksonPollock3Site`, `JacksonPollock4Site`, `JacksonPollock7Site` |
| Exercise | `RM_Estimator` |
| Meal Planning | `MakeMeal` |
| Enums | `Sex`, `BodyType`, `ActivityLevel`, `Goal` |
| Data Models | `BodyCompositionResult`, `MacroTargets`, `RepEstimate` |

## Agent Skills

This package includes 3 skills for AI-assisted fitness calculations:

| Skill | Description |
|-------|-------------|
| `body-composition` | Skinfold-based body fat assessment |
| `rep-max` | One-rep max estimation via validated percentage table |
| `meal-planner` | Macronutrient planning by body type |

### Install

**Claude Code plugin** — run inside a Claude Code session:

```
/plugin marketplace add Jeffallan/Fitness-Tools
/plugin install fitness-tools@fitness-tools
```

**[skills.sh](https://skills.sh)** — from any terminal:

```bash
npx skills add Jeffallan/Fitness-Tools
```

## How To Contribute

- Read the [contributing guidelines](CONTRIBUTING.md)
- Check the [changelog](CHANGELOG.md) to see where this project has been

All skill levels are welcome and our maintainers will help you in whatever way we can.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).
