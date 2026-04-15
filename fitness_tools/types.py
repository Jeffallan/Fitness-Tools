"""Enumerated types for fitness-tools.

Replaces raw string comparisons with type-safe StrEnum members.
Backward compatible: Sex.MALE == "male" evaluates to True.
"""

from enum import StrEnum


class Sex(StrEnum):
    """Biological sex for body composition equations."""

    MALE = "male"
    FEMALE = "female"


class BodyType(StrEnum):
    """Somatotype classification for macronutrient distribution."""

    ECTOMORPH = "ectomorph"
    MESOMORPH = "mesomorph"
    ENDOMORPH = "endomorph"


class Goal(StrEnum):
    """Nutritional goal for caloric and macro target calculation."""

    WEIGHT_LOSS = "weight_loss"
    MAINTENANCE = "maintenance"
    WEIGHT_GAIN = "weight_gain"


class ActivityLevel(StrEnum):
    """Physical activity level for TDEE estimation."""

    SEDENTARY = "sedentary"
    MODERATE = "moderate"
    VERY = "very"
