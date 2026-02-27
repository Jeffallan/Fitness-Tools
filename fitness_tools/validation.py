"""Centralized validation functions for fitness-tools.

Replaces scattered if/raise chains across modules with
reusable, consistently-messaged validators.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from fitness_tools.types import Sex


def validate_positive(value: float | int, name: str) -> None:
    """Ensure a value is strictly positive.

    Args:
        value: The numeric value to check.
        name: Human-readable parameter name for error messages.

    Raises:
        ValueError: If value is not positive.
        TypeError: If value is not numeric.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_range(
    value: float | int,
    min_val: float | int,
    max_val: float | int,
    name: str,
) -> None:
    """Ensure a value falls within an inclusive range.

    Args:
        value: The numeric value to check.
        min_val: Minimum allowed value (inclusive).
        max_val: Maximum allowed value (inclusive).
        name: Human-readable parameter name for error messages.

    Raises:
        ValueError: If value is outside the range.
        TypeError: If value is not numeric.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric, got {type(value).__name__}")
    if not min_val <= value <= max_val:
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")


def validate_sex(value: Any) -> Sex:
    """Coerce a string or Sex enum to a Sex member.

    Accepts both Sex.MALE and "male" for backward compatibility.

    Args:
        value: A Sex enum member or string ("male"/"female").

    Returns:
        The corresponding Sex enum member.

    Raises:
        ValueError: If the value cannot be coerced to a Sex member.
    """
    if isinstance(value, Sex):
        return value
    if isinstance(value, str):
        try:
            return Sex(value.lower())
        except ValueError:
            pass
    raise ValueError(f"Invalid sex: {value!r}. Expected 'male' or 'female'.")


def validate_skinfolds(
    measurements: Sequence[float | int],
    expected_count: int,
    equation_name: str,
) -> None:
    """Validate a sequence of skinfold measurements.

    Args:
        measurements: Sequence of skinfold thickness values (mm).
        expected_count: Number of sites required by the equation.
        equation_name: Name of the equation for error messages.

    Raises:
        ValueError: If count is wrong or any measurement is non-positive.
        TypeError: If any measurement is not numeric.
    """
    if len(measurements) != expected_count:
        raise ValueError(
            f"{equation_name} requires {expected_count} skinfold sites, "
            f"got {len(measurements)}"
        )
    for i, m in enumerate(measurements, 1):
        if not isinstance(m, (int, float)):
            raise TypeError(f"Skinfold site {i} must be numeric, got {type(m).__name__}")
        if m <= 0:
            raise ValueError(f"Skinfold site {i} must be positive, got {m}")
