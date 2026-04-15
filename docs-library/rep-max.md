# Estimating Rep Maximums

Different repetition ranges produce different training adaptations. Broadly:

- **Endurance:** 10–15 reps
- **Hypertrophy (muscle growth):** 8–12 reps
- **Strength:** ≤ 6 reps
- **Power:** 1–6 reps

As goals shift over time, lifters need a way to quickly translate a known working weight into the right weight for a new rep target. `RM_Estimator` does this translation using the ACSM percentage-of-1RM table.

## Constructor Arguments

`RM_Estimator` takes three positional arguments:

1. **Current weight** — the load you're currently lifting, ending in `.0` or `.5`
2. **Current reps** — reps you can complete with that weight
3. **Desired reps** — the rep target you want to train for

## Example

Say you can lift 175 lbs for 10 reps and want to shift toward strength by training at 6 reps.

```python
>>> from fitness_tools.exercise.rm_estimator import RM_Estimator
>>> new_reps = RM_Estimator(175.0, 10, 6)
>>> new_reps.estimate_weight()
197.5
```

By this calculation you should be able to lift **197.5 lbs for approximately 6 reps**.

## Rounding Base

`estimate_weight()` rounds to the nearest **2.5 lbs** by default. Pass a different `base` to change rounding — useful for kilogram plates or gyms with coarser weight increments.

```python
>>> new_reps = RM_Estimator(175.0, 10, 6)
>>> new_reps.estimate_weight(base=5)
200.0
```

## Estimating Your 1RM

To estimate your one-rep maximum (instead of converting between rep ranges), use a working set of **5 reps or fewer** for best accuracy:

```python
>>> one_rm = RM_Estimator(225.0, 3, 1)
>>> one_rm.estimate_weight()
240.0
```

Percentages of 1RM from this table are accurate to within **±0.5% to 2%**, depending on training status.

## Reference

For the full ACSM rep-percentage table see the [Rep Max skill reference](/Fitness-Tools/skills/rep-max-percentage-table/).
