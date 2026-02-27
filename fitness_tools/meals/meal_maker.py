from __future__ import annotations

from fitness_tools.models import MacroTargets
from fitness_tools.types import ActivityLevel, BodyType, Goal


class MakeMeal:
    """Use this class to create optimal meals regardless of your body type or fitness goals.

    :param weight: Enter your current weight.
    :param goal: Select a goal: 'weight_loss', 'maintenance', 'weight_gain', Goal enum, or None.
    :param body_type: Select a body type: 'endomorph', 'ectomorph', 'mesomorph', BodyType enum,
                      or None.
    :param activity_level: Select an activity level: 'sedentary', 'moderate', 'very',
                           ActivityLevel enum, or None.
    :param min_cal: Enter the desired minimum calories per pound defaults to None.
    :param max_cal: Enter the desired maximum calories per pound defaults to None.
    :param fat_percent: Enter the desired percent of calories from fat defaults to None.
    :param protein_percent: Enter the desired percent of calories from protein defaults to None.
    :param carb_percent: Enter the desired percent of calories from carbs defaults to None.

    Usage: There are four ways to use this class:

        1) Fully custom: pass weight, min_cal, max_cal, fat_percent, protein_percent, carb_percent.
        2) Preset calories + custom macros: pass goal + activity_level for calories,
           then fat_percent, protein_percent, carb_percent manually.
        3) Preset macros + custom calories: pass body_type for macros,
           then min_cal and max_cal manually.
        4) Fully preset: pass body_type, activity_level, and goal.
    """

    def __init__(
        self,
        weight: int,
        goal: str | Goal | None = None,
        body_type: str | BodyType | None = None,
        activity_level: str | ActivityLevel | None = None,
        min_cal: int | None = None,
        max_cal: int | None = None,
        fat_percent: float | None = None,
        protein_percent: float | None = None,
        carb_percent: float | None = None,
    ) -> None:
        self.weight = weight
        self.goal = goal
        self.body_type = body_type
        self.activity_level = activity_level
        self.min_cal = min_cal
        self.max_cal = max_cal
        self.fat_percent = fat_percent
        self.protein_percent = protein_percent
        self.carb_percent = carb_percent

        self._check_weight()
        self._check_body_type()
        self._set_optimum_calories()
        self._check_macronutrient_percentages()
        self._check_min_cal()
        self._check_max_cal()

    def _check_weight(self) -> None:
        if isinstance(self.weight, int):
            if self.weight <= 0:
                raise ValueError("Weight must be a positive integer.")
        else:
            raise TypeError("Param weight must be type int.")

    def _check_min_cal(self) -> None:
        if self.min_cal is not None:
            if isinstance(self.min_cal, int):
                if self.min_cal <= 0:
                    raise ValueError("Min_cal must be a positive integer.")
            else:
                raise TypeError("Min_cal must be of type int.")

    def _check_max_cal(self) -> None:
        if self.max_cal is not None:
            if isinstance(self.max_cal, int):
                if self.max_cal <= 0:
                    raise ValueError("Max_cal must be a positive integer.")
            else:
                raise TypeError("Max_cal must be of type int.")

    def _check_body_type(self) -> None:
        """If valid body_type is passed; set the ideal fat_percent,
        protein_percent, and carb_percent in __init__."""

        if self.body_type is not None:
            if isinstance(self.body_type, BodyType):
                bt = self.body_type
            elif isinstance(self.body_type, str):
                try:
                    bt = BodyType(self.body_type.casefold())
                except ValueError:
                    raise ValueError(
                        "Please enter a valid body type: 'endomorph', 'ectomorph', "
                        "'mesomorph', or set body_type to None"
                    ) from None
            else:
                raise ValueError(
                    "Please enter a valid body type: 'endomorph', 'ectomorph', "
                    "'mesomorph', or set body_type to None"
                )

            if bt == BodyType.MESOMORPH:
                self.fat_percent = 0.3
                self.protein_percent = 0.3
                self.carb_percent = 0.4
            elif bt == BodyType.ECTOMORPH:
                self.fat_percent = 0.2
                self.protein_percent = 0.25
                self.carb_percent = 0.55
            elif bt == BodyType.ENDOMORPH:
                self.fat_percent = 0.4
                self.protein_percent = 0.35
                self.carb_percent = 0.25

    def _set_optimum_calories(self) -> None:
        """If valid activity_level and goal are passed; set the ideal
        min_cal and max_cal in __init__."""

        if self.activity_level is not None and self.goal is not None:
            # Coerce to enum if string
            if isinstance(self.activity_level, str) and not isinstance(
                self.activity_level, ActivityLevel
            ):
                try:
                    al = ActivityLevel(self.activity_level.casefold())
                except ValueError:
                    raise ValueError(
                        "Please enter a valid goal; 'weight_loss', 'maintenance', "
                        "'weight_gain' or activity_level; 'sedentary', 'moderate', "
                        "or 'very' alternatively, set these parameters to None."
                    ) from None
            elif isinstance(self.activity_level, ActivityLevel):
                al = self.activity_level
            else:
                raise ValueError(
                    "Please enter a valid goal; 'weight_loss', 'maintenance', "
                    "'weight_gain' or activity_level; 'sedentary', 'moderate', "
                    "or 'very' alternatively, set these parameters to None."
                )

            if isinstance(self.goal, str) and not isinstance(self.goal, Goal):
                try:
                    g = Goal(self.goal.casefold())
                except ValueError:
                    raise ValueError(
                        "Please enter a valid goal; 'weight_loss', 'maintenance', "
                        "'weight_gain' or activity_level; 'sedentary', 'moderate', "
                        "or 'very' alternatively, set these parameters to None."
                    ) from None
            elif isinstance(self.goal, Goal):
                g = self.goal
            else:
                raise ValueError(
                    "Please enter a valid goal; 'weight_loss', 'maintenance', "
                    "'weight_gain' or activity_level; 'sedentary', 'moderate', "
                    "or 'very' alternatively, set these parameters to None."
                )

            calorie_map: dict[tuple[ActivityLevel, Goal], tuple[int, int]] = {
                (ActivityLevel.SEDENTARY, Goal.WEIGHT_LOSS): (10, 12),
                (ActivityLevel.SEDENTARY, Goal.MAINTENANCE): (12, 14),
                (ActivityLevel.SEDENTARY, Goal.WEIGHT_GAIN): (16, 18),
                (ActivityLevel.MODERATE, Goal.WEIGHT_LOSS): (12, 14),
                (ActivityLevel.MODERATE, Goal.MAINTENANCE): (14, 16),
                (ActivityLevel.MODERATE, Goal.WEIGHT_GAIN): (18, 20),
                (ActivityLevel.VERY, Goal.WEIGHT_LOSS): (14, 16),
                (ActivityLevel.VERY, Goal.MAINTENANCE): (16, 18),
                (ActivityLevel.VERY, Goal.WEIGHT_GAIN): (20, 22),
            }

            key = (al, g)
            if key not in calorie_map:
                raise ValueError(
                    "Please enter a valid goal; 'weight_loss', 'maintenance', "
                    "'weight_gain' or activity_level; 'sedentary', 'moderate', "
                    "or 'very' alternatively, set these parameters to None."
                )

            self.min_cal, self.max_cal = calorie_map[key]

    def _check_macronutrient_percentages(self) -> None:
        """Checks if the sum of macronutrient percentages equals one hundred percent."""

        if (
            isinstance(self.fat_percent, float)
            and isinstance(self.protein_percent, float)
            and isinstance(self.carb_percent, float)
        ):
            if self.fat_percent + self.protein_percent + self.carb_percent != 1:
                raise ValueError(
                    "The sum of fat_percent, protein_percent, and carb_percent must equal 1"
                )
        else:
            raise TypeError(
                "Kwags fat_percent, protein_percent, and carb_percent must be float type."
            )

    def daily_min_calories(self) -> float:
        """Returns the total daily minimum calories."""
        min_calories = self.weight * self.min_cal  # type: ignore[operator]
        return round(min_calories, 0)

    def daily_max_calories(self) -> float:
        """Returns the total daily maximum calories."""
        max_calories = self.weight * self.max_cal  # type: ignore[operator]
        return round(max_calories, 0)

    def daily_min_fat(self) -> float:
        """Returns the total daily minimum fat in grams."""
        daily_min_fat = (self.daily_min_calories() * self.fat_percent) / 9  # type: ignore[operator]
        return round(daily_min_fat, 0)

    def daily_max_fat(self) -> float:
        """Returns the total daily maximum fat in grams."""
        daily_max_fat = (self.daily_max_calories() * self.fat_percent) / 9  # type: ignore[operator]
        return round(daily_max_fat, 0)

    def daily_min_protein(self) -> float:
        """Returns the total daily minimum protein in grams."""
        daily_min_protein = (self.daily_min_calories() * self.protein_percent) / 4  # type: ignore[operator]
        return round(daily_min_protein, 0)

    def daily_max_protein(self) -> float:
        """Returns the total daily maximum protein in grams."""
        daily_max_protein = (self.daily_max_calories() * self.protein_percent) / 4  # type: ignore[operator]
        return round(daily_max_protein, 0)

    def daily_min_carbs(self) -> float:
        """Returns the total daily minimum carbohydrates in grams."""
        daily_min_carbs = (self.daily_min_calories() * self.carb_percent) / 4  # type: ignore[operator]
        return round(daily_min_carbs, 0)

    def daily_max_carbs(self) -> float:
        """Returns the total daily maximum carbohydrates in grams."""
        daily_max_carbs = (self.daily_max_calories() * self.carb_percent) / 4  # type: ignore[operator]
        return round(daily_max_carbs, 0)

    def daily_requirements(self) -> MacroTargets:
        """Returns recommended calories and macronutrients for the day.

        :return: daily_requirements
        :rtype: MacroTargets
        """
        return MacroTargets(
            min_calories=round(self.daily_min_calories(), 0),
            max_calories=round(self.daily_max_calories(), 0),
            min_fat=round(self.daily_min_fat(), 0),
            max_fat=round(self.daily_max_fat(), 0),
            min_protein=round(self.daily_min_protein(), 0),
            max_protein=round(self.daily_max_protein(), 0),
            min_carbs=round(self.daily_min_carbs(), 0),
            max_carbs=round(self.daily_max_carbs(), 0),
        )

    def make_meal(self, number_meals: int) -> MacroTargets:
        """Returns recommended calories and macronutrients for one meal.

        :param number_meals: Number of meals to divide daily requirements into.
        :type number_meals: int
        :return: meal
        :rtype: MacroTargets
        """
        daily = self.daily_requirements()
        return MacroTargets(
            min_calories=round(daily.min_calories / number_meals, 0),
            max_calories=round(daily.max_calories / number_meals, 0),
            min_fat=round(daily.min_fat / number_meals, 0),
            max_fat=round(daily.max_fat / number_meals, 0),
            min_protein=round(daily.min_protein / number_meals, 0),
            max_protein=round(daily.max_protein / number_meals, 0),
            min_carbs=round(daily.min_carbs / number_meals, 0),
            max_carbs=round(daily.max_carbs / number_meals, 0),
        )
