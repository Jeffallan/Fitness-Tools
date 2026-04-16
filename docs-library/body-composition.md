# Calculating Body Composition

This module is a collection of the most popular body fat percentage equations, calculated by measuring various skinfold sites in millimeters.

## Workflow

The typical workflow for calculating body fat from skinfolds:

1. Collect measurements from the skinfold sites required by your chosen equation.
2. Calculate body density.
3. Convert body density to body fat using one of the provided equations.

## Density-to-Body-Fat Conversions

Every subclass in this module inherits from `GenericCalculator`, which exposes five methods that convert body density (g/cm³) to body fat percentage. These are **not interchangeable alternatives**. Each was validated on a specific population, and picking the wrong one introduces systematic bias.

| Method | Intended population | Formula |
|---|---|---|
| `siri()` | General. The standard default | `%BF = 495/ρ − 450` |
| `brozek()` | General. The alternative default with refined fat-free-mass assumptions | `%BF = 457/ρ − 414.2` |
| `schutte()` | African-American men | `%BF = 437.4/ρ − 392.8` |
| `wagner()` | Black male athletes | `%BF = 486/ρ − 439` |
| `ortiz()` | Black women | `%BF = 483.2/ρ − 436.9` |

These conversions are required for every equation in this module *except* `JacksonPollock4Site`, which computes body fat directly from skinfolds via its own `body_fat()` method.

> **If your subject doesn't fit one of the specialized populations, use `siri()`**. It is the widely used default (ACSM, Heyward). Use `brozek()` when a refined fat-free-mass model is preferred. Only use `schutte()`, `wagner()`, or `ortiz()` when the subject matches the target population for that equation.

## Constructor Arguments

All skinfold classes take the same three positional arguments:

1. **Age**: positive integer
2. **Sex**: `"male"` / `"female"` string, or the typed `Sex.MALE` / `Sex.FEMALE` enum
3. **Skinfold measurements**: tuple of integers in millimeters. Order does not matter.

The `Sex` enum is a `StrEnum`, so `Sex.MALE == "male"`. You can mix either form.

## Example: Durnin–Womersley (4-site)

A 40-year-old female with skinfolds:

- triceps = 7 mm
- biceps = 5 mm
- subscapular = 4 mm
- suprailiac = 10 mm

```python
>>> from fitness_tools.composition.bodyfat import DurninWomersley
>>> from fitness_tools.types import Sex
>>> calc = DurninWomersley(40, Sex.FEMALE, (7, 5, 4, 10))
>>> calc.body_density()
1.046703631104186

>>> calc.siri(calc.body_density())
22.9
```

By the Durnin–Womersley equation, our hypothetical subject's body fat is **22.9%**.

## Example: Jackson–Pollock 4-site (direct body fat)

As noted above, `JacksonPollock4Site` is the one equation in the module that converts skinfolds directly into body fat without an intermediate density-to-BF step.

A 25-year-old male with skinfolds:

- abdominal = 6 mm
- triceps = 5 mm
- thigh = 8 mm
- suprailiac = 6 mm

```python
>>> from fitness_tools.composition.bodyfat import JacksonPollock4Site
>>> from fitness_tools.types import Sex
>>> calc = JacksonPollock4Site(25, Sex.MALE, (6, 5, 8, 6))
>>> calc.body_fat()
5.2
```

Our hypothetical subject has a body fat of **5.2%**.

## Available Equations

| Class | Sites | Conversion |
|---|---|---|
| `DurninWomersley` | 4 (triceps, biceps, subscapular, suprailiac) | density → `siri()` etc. |
| `JacksonPollock7Site` | 7 | density → `siri()` etc. |
| `JacksonPollock4Site` | 4 (abdominal, triceps, thigh, suprailiac) | **direct body fat via `body_fat()`** |
| `JacksonPollock3Site` | 3 (sex-specific sites) | density → `siri()` etc. |

For the underlying formulas, age brackets, and sex-specific coefficients see the [Body Composition skill reference](/Fitness-Tools/skills/body-composition-equations/).
