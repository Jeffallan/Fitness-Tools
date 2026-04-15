# Fitness Tools

**Healthy Lifestyles With Python**

Fitness Tools is a Python package that facilitates healthy lifestyles using ACSM-sourced equations. Whether you're a wellness professional, veteran gym rat, or just starting your fitness journey, this package will benefit you.

## Features

- **Body Composition** — Estimate body fat percentage from skinfold measurements using Durnin-Womersley and Jackson-Pollock (3/4/7-site) equations
- **Rep Max Estimation** — Convert between weight and rep ranges using the ACSM percentage-of-1RM table
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
| `rep-max` | One-rep max estimation via ACSM table |
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
