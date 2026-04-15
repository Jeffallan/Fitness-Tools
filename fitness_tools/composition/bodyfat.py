from __future__ import annotations

import math
from collections.abc import Sequence

from fitness_tools.types import Sex
from fitness_tools.validation import validate_positive, validate_sex


class GenericCalculator:
    """The base class that all body fat calculations inherit from.

    :param age: Age as a positive, whole number
    :param sex: Sex either 'male' or 'female' (case insensitive), or Sex enum.
    :param *args: A list of positive, whole numbers reflected as skinfold measurements in
                  millimeters. See subclass documentation for implementation details.
    """

    def __init__(self, age: int, sex: str | Sex, *args: Sequence[int]) -> None:
        self.sex: Sex = validate_sex(sex)

        if not isinstance(age, int):
            raise ValueError("Age must be a positive, whole number")
        validate_positive(age, "Age")
        self.age: int = age

        self.skinfolds: list[int] = list(*args)
        for s in self.skinfolds:
            if not isinstance(s, int) or s <= 0:
                raise ValueError("Skinfold measurements must be positive, whole numbers.")

        self.sum_folds: int = sum(self.skinfolds)
        self.log_sum: float = math.log10(self.sum_folds)
        self.square_folds: int = int(math.pow(self.sum_folds, 2))

    def siri(self, body_density: float) -> float:
        """Most popular and generic body density to bodyfat conversion equation.

        :param body_density: the results yielded from a body density equation.
        :rtype: float
        :returns: body_fat
        """
        body_fat = (495 / body_density) - 450
        return round(body_fat, 1)

    def brozek(self, body_density: float) -> float:
        """Brozek body density to bodyfat conversion equation.

        :param body_density: the results yielded from a body density equation.
        :rtype: float
        :returns: body_fat
        """
        body_fat = (457 / body_density) - 414.2
        return round(body_fat, 1)

    def schutte(self, body_density: float) -> float:
        """Schutte body density to bodyfat conversion equation.

        :param body_density: the results yielded from a body density equation.
        :rtype: float
        :returns: body_fat
        """
        body_fat = (437.4 / body_density) - 392.8
        return round(body_fat, 1)

    def wagner(self, body_density: float) -> float:
        """Wagner body density to bodyfat conversion equation.

        :param body_density: the results yielded from a body density equation.
        :rtype: float
        :returns: body_fat
        """
        body_fat = (486 / body_density) - 439
        return round(body_fat, 1)

    def ortiz(self, body_density: float) -> float:
        """Ortiz body density to bodyfat conversion equation.

        :param body_density: the results yielded from a body density equation.
        :rtype: float
        :returns: body_fat
        """
        body_fat = (483.2 / body_density) - 436.9
        return round(body_fat, 1)


class DurninWomersley(GenericCalculator):
    """Uses the Durnin Womersley equation to calculate body density.
    Use triceps, biceps, subscapular, and suprailiac skinfold measurements.

    :param age: Age as a positive, whole number
    :param sex: Sex either 'male' or 'female' (case insensitive), or Sex enum.
    :param *args: A list of positive, whole numbers reflected as skinfold measurements in
                  millimeters.
    """

    def __init__(self, age: int, sex: str | Sex, *args: Sequence[int]) -> None:
        super().__init__(age, sex, *args)

        if len(self.skinfolds) != 4:
            raise ValueError(
                "This equation requires 4 skin fold measurements "
                "triceps, biceps, subscapular, and suprailliac."
            )

    def body_density(self) -> float:
        """Converts params age, sex, and skinfolds to body density.

        :rtype: float
        :returns: body_density
        """
        if self.sex == "male":
            if self.age < 17:
                density = 1.1533 - (0.0643 * self.log_sum)
            elif self.age < 20:
                density = 1.1620 - (0.0630 * self.log_sum)
            elif self.age < 30:
                density = 1.1631 - (0.0632 * self.log_sum)
            elif self.age < 40:
                density = 1.1422 - (0.0544 * self.log_sum)
            elif self.age < 50:
                density = 1.1620 - (0.0700 * self.log_sum)
            else:
                density = 1.1715 - (0.0779 * self.log_sum)
        else:
            if self.age < 17:
                density = 1.1369 - (0.0598 * self.log_sum)
            elif self.age < 20:
                density = 1.1549 - (0.0678 * self.log_sum)
            elif self.age < 30:
                density = 1.1599 - (0.0717 * self.log_sum)
            elif self.age < 40:
                density = 1.1423 - (0.0632 * self.log_sum)
            elif self.age < 50:
                density = 1.1333 - (0.0612 * self.log_sum)
            else:
                density = 1.1339 - (0.0645 * self.log_sum)
        return density


class JacksonPollock7Site(GenericCalculator):
    """Uses the Jackson Pollock 7 site equation to calculate body density.
    Use chest, axilla, tricep, subscapular, abdominal, suprailiac, and thigh measurements.

    :param age: Age as a positive, whole number
    :param sex: Sex either 'male' or 'female' (case insensitive), or Sex enum.
    :param *args: A list of positive, whole numbers reflected as skinfold measurements in
                  millimeters.
    """

    def __init__(self, age: int, sex: str | Sex, *args: Sequence[int]) -> None:
        super().__init__(age, sex, *args)

        if len(self.skinfolds) != 7:
            raise ValueError(
                "This equation requires 7 skin fold measurements "
                "biceps, chest, subscapular, abdominal, suprailiac, thigh, and axilla."
            )

    def body_density(self) -> float:
        """Converts params age, sex, and skinfolds to body density.

        :rtype: float
        :returns: body_density
        """
        if self.sex == "male":
            density = (
                1.112
                - (0.00043499 * self.sum_folds)
                + (0.00000055 * self.square_folds)
                - (0.00028826 * self.age)
            )
        else:
            density = (
                1.097
                - (0.00046971 * self.sum_folds)
                + (0.00000056 * self.square_folds)
                - (0.00012828 * self.age)
            )
        return density


class JacksonPollock4Site(GenericCalculator):
    """Uses the Jackson Pollock 4 site equation to calculate body fat.
    Use abdominal, triceps, thigh, and suprailiac skinfolds.

    :param age: Age as a positive, whole number
    :param sex: Sex either 'male' or 'female' (case insensitive), or Sex enum.
    :param *args: A list of positive, whole numbers reflected as skinfold measurements in
                  millimeters.
    """

    def __init__(self, age: int, sex: str | Sex, *args: Sequence[int]) -> None:
        super().__init__(age, sex, *args)

        if len(self.skinfolds) != 4:
            raise ValueError(
                "This equation requires 4 skinfold measurements "
                "abdominal, triceps, thigh, and suprailiac."
            )

    def body_fat(self) -> float:
        """Converts params age, sex, and skinfolds directly to body fat.

        :rtype: float
        :returns: body_fat
        """
        if self.sex == "male":
            body_fat = (
                (0.29288 * self.sum_folds)
                - (0.0005 * self.square_folds)
                + (0.15845 * self.age)
                - 5.76377
            )
        else:
            body_fat = (
                (0.29669 * self.sum_folds)
                - (0.00043 * self.square_folds)
                + (0.02963 * self.age)
                + 1.4072
            )
        return round(body_fat, 1)


class JacksonPollock3Site(GenericCalculator):
    """Uses the Jackson Pollock 3 site equation to calculate body density.
    Use chest, triceps, and subscapular skinfolds for men and triceps,
    thigh and suprailiac for women.

    :param age: Age as a positive, whole number
    :param sex: Sex either 'male' or 'female' (case insensitive), or Sex enum.
    :param *args: A list of positive, whole numbers reflected as skinfold measurements in
                  millimeters.
    """

    def __init__(self, age: int, sex: str | Sex, *args: Sequence[int]) -> None:
        super().__init__(age, sex, *args)

        if len(self.skinfolds) != 3:
            raise ValueError(
                "This equation requires 3 skinfold measurements "
                "chest, triceps and subscapular for men and "
                "triceps, thigh and suprailiac in women."
            )

    def body_density(self) -> float:
        """Converts params age, sex, and skinfolds to body density.

        :rtype: float
        :returns: body_density
        """
        if self.sex == "male":
            body_density = (
                1.10938
                - (0.0008267 * self.sum_folds)
                + (0.0000055 * self.square_folds)
                - (0.000244 * self.age)
            )
        else:
            body_density = (
                1.0994921
                - (0.0009929 * self.sum_folds)
                + (0.0000023 * self.square_folds)
                - (0.0001392 * self.age)
            )
        return body_density
