# Macronutrient Assignments

Proper nutrition is a personal, opinionated topic. While the information you may encounter varies widely, calculating your calorie and macronutrient requirements should not be difficult once you've settled on a paradigm that works for you.

The goal of this module is to automate those calculations so you can spend more time *following* your plan rather than computing it.

## The `MakeMeal` API

This module exposes a single class, `MakeMeal`, with two methods:

- `daily_requirements()` — returns a `MacroTargets` dataclass of recommended daily calories and macronutrients.
- `make_meal(n)` — returns a `MacroTargets` dataclass representing daily requirements divided across *n* meals.

`MacroTargets` supports attribute access (`result.min_calories`) — the preferred style — and also continues to support legacy dict access (`result["min_calories"]`) with a `DeprecationWarning`.

The only positional argument to `MakeMeal` is **weight** (in pounds). Everything else is a keyword argument. There are four ways to configure it, ordered from most opinionated to fully custom.

## 1. Preset Macros + Preset Calories

Body type dictates macro percentages; activity level and goal dictate calorie range.

```python
>>> from fitness_tools.meals.meal_maker import MakeMeal
>>> from fitness_tools.types import BodyType, ActivityLevel, Goal
>>> plan = MakeMeal(
...     180,
...     goal=Goal.MAINTENANCE,
...     activity_level=ActivityLevel.MODERATE,
...     body_type=BodyType.MESOMORPH,
... )

>>> daily = plan.daily_requirements()
>>> daily.min_calories, daily.max_calories
(2520, 2880)
>>> daily.min_protein, daily.max_protein
(189.0, 216.0)

>>> meal = plan.make_meal(4)   # four meals per day
>>> meal.min_calories, meal.max_calories
(630.0, 720.0)
```

All typed enums (`Goal`, `ActivityLevel`, `BodyType`) accept their string equivalents too — e.g., `goal="maintenance"` works the same as `goal=Goal.MAINTENANCE`.

## 2. Preset Macros + Custom Calories

Body type sets macro percentages; you provide `min_cal` and `max_cal` per pound.

```python
>>> plan = MakeMeal(180, min_cal=12, max_cal=14, body_type="ectomorph")
>>> daily = plan.daily_requirements()
>>> daily.min_calories, daily.max_calories
(2160, 2520)
>>> daily.min_carbs, daily.max_carbs
(297.0, 346.0)

>>> plan.make_meal(3).min_calories
720.0
```

## 3. Custom Macros + Preset Calories

Activity level and goal set the calorie range; you set macro percentages manually.

```python
>>> plan = MakeMeal(
...     180,
...     activity_level="sedentary",
...     goal="weight_loss",
...     fat_percent=0.2,
...     protein_percent=0.2,
...     carb_percent=0.6,
... )
>>> daily = plan.daily_requirements()
>>> daily.min_calories, daily.max_calories
(1800, 2160)

>>> plan.make_meal(6).min_calories
300.0
```

## 4. Fully Custom

You control everything. Set macro percentages and calorie ranges manually.

```python
>>> plan = MakeMeal(
...     180,
...     min_cal=10,
...     max_cal=12,
...     fat_percent=0.2,
...     protein_percent=0.25,
...     carb_percent=0.55,
... )
>>> daily = plan.daily_requirements()
>>> daily.min_calories, daily.max_calories
(1800, 2160)

>>> plan.make_meal(8).min_calories
225.0
```

## Accepted Values

| Parameter | Accepted values |
|---|---|
| `body_type` | `"ectomorph"`, `"mesomorph"`, `"endomorph"` (or `BodyType.*`) |
| `activity_level` | `"sedentary"`, `"moderate"`, `"very"` (or `ActivityLevel.*`) |
| `goal` | `"weight_loss"`, `"maintenance"`, `"weight_gain"` (or `Goal.*`) |
| `fat_percent`, `protein_percent`, `carb_percent` | Floats that must sum to `1.0` |
| `min_cal`, `max_cal` | Calories per pound of body weight |

For the underlying macro distribution and calorie-per-pound tables see the [Meal Planner skill reference](/Fitness-Tools/skills/meal-planner-macro-tables/).
