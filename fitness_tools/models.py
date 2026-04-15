"""Result dataclasses for fitness-tools.

Replaces raw dict returns with frozen, typed dataclasses.
All results are immutable after construction.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class MacroTargets:
    """Daily or per-meal macronutrient targets.

    All values are in grams (g) except calories (kcal).
    Min/max ranges account for body type and goal variations.

    Supports dict-style access for backward compatibility:
        result["min_calories"]  # works but emits DeprecationWarning
        result.min_calories     # preferred
    """

    min_calories: float
    max_calories: float
    min_fat: float
    max_fat: float
    min_protein: float
    max_protein: float
    min_carbs: float
    max_carbs: float

    def __getitem__(self, key: str) -> float:
        warnings.warn(
            "Dict-style access on MacroTargets is deprecated. "
            "Use attribute access instead (e.g., result.min_calories).",
            DeprecationWarning,
            stacklevel=2,
        )
        for f in fields(self):
            if f.name == key:
                return getattr(self, key)  # type: ignore[no-any-return]
        raise KeyError(key)

    def keys(self) -> list[str]:
        warnings.warn(
            "Dict-style access on MacroTargets is deprecated. "
            "Use dataclasses.fields() or attribute access instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return [f.name for f in fields(self)]


@dataclass(frozen=True)
class BodyCompositionResult:
    """Result from a body fat percentage calculation.

    Attributes:
        body_density: Calculated body density (g/cm³).
        body_fat_pct: Estimated body fat percentage.
        method: Conversion equation used ("siri" or "brozek").
        equation: Skinfold equation used (e.g., "jackson_pollock_7",
            "durnin_womersley").
    """

    body_density: float
    body_fat_pct: float
    method: str
    equation: str


@dataclass(frozen=True)
class RepEstimate:
    """Result from a rep max estimation.

    Attributes:
        estimated_1rm: Predicted one-rep maximum (same unit as input weight).
        weight: Weight used in the working set.
        reps: Number of reps performed.
        percentage: The percentage of 1RM corresponding to the rep count.
    """

    estimated_1rm: float
    weight: float
    reps: int
    percentage: float
