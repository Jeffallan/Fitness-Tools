import pytest

from fitness_tools.types import ActivityLevel, BodyType, Goal, Sex


class TestSex:
    def test_male_value(self):
        assert Sex.MALE == "male"

    def test_female_value(self):
        assert Sex.FEMALE == "female"

    def test_string_equality(self):
        assert Sex.MALE == "male"
        assert Sex.FEMALE == "female"

    def test_invalid_value(self):
        with pytest.raises(ValueError):
            Sex("invalid")


class TestBodyType:
    def test_values(self):
        assert BodyType.ECTOMORPH == "ectomorph"
        assert BodyType.MESOMORPH == "mesomorph"
        assert BodyType.ENDOMORPH == "endomorph"

    def test_invalid_value(self):
        with pytest.raises(ValueError):
            BodyType("invalid")


class TestGoal:
    def test_values(self):
        assert Goal.WEIGHT_LOSS == "weight_loss"
        assert Goal.MAINTENANCE == "maintenance"
        assert Goal.WEIGHT_GAIN == "weight_gain"

    def test_invalid_value(self):
        with pytest.raises(ValueError):
            Goal("invalid")


class TestActivityLevel:
    def test_values(self):
        assert ActivityLevel.SEDENTARY == "sedentary"
        assert ActivityLevel.MODERATE == "moderate"
        assert ActivityLevel.VERY == "very"

    def test_invalid_value(self):
        with pytest.raises(ValueError):
            ActivityLevel("invalid")
