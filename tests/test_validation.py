import pytest

from fitness_tools.types import Sex
from fitness_tools.validation import (
    validate_positive,
    validate_range,
    validate_sex,
    validate_skinfolds,
)


class TestValidatePositive:
    def test_valid_int(self):
        validate_positive(5, "test")

    def test_valid_float(self):
        validate_positive(3.14, "test")

    def test_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_positive(0, "test")

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_positive(-1, "test")

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_positive("five", "test")  # type: ignore[arg-type]


class TestValidateRange:
    def test_valid_in_range(self):
        validate_range(5, 1, 10, "test")

    def test_at_min(self):
        validate_range(1, 1, 10, "test")

    def test_at_max(self):
        validate_range(10, 1, 10, "test")

    def test_below_range_raises(self):
        with pytest.raises(ValueError):
            validate_range(0, 1, 10, "test")

    def test_above_range_raises(self):
        with pytest.raises(ValueError):
            validate_range(11, 1, 10, "test")

    def test_non_numeric_raises_type_error(self):
        with pytest.raises(TypeError):
            validate_range("five", 1, 10, "test")  # type: ignore[arg-type]


class TestValidateSex:
    def test_enum_male(self):
        assert validate_sex(Sex.MALE) == Sex.MALE

    def test_enum_female(self):
        assert validate_sex(Sex.FEMALE) == Sex.FEMALE

    def test_string_male(self):
        assert validate_sex("male") == Sex.MALE

    def test_string_female(self):
        assert validate_sex("female") == Sex.FEMALE

    def test_case_insensitive(self):
        assert validate_sex("MALE") == Sex.MALE
        assert validate_sex("Female") == Sex.FEMALE

    def test_invalid_string(self):
        with pytest.raises(ValueError):
            validate_sex("invalid")

    def test_non_string(self):
        with pytest.raises(ValueError):
            validate_sex(42)


class TestValidateSkinfolds:
    def test_valid(self):
        validate_skinfolds([1, 2, 3], 3, "test")

    def test_wrong_count(self):
        with pytest.raises(ValueError, match="requires 3 skinfold sites"):
            validate_skinfolds([1, 2], 3, "test")

    def test_non_positive(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_skinfolds([1, -2, 3], 3, "test")

    def test_zero_value(self):
        with pytest.raises(ValueError, match="must be positive"):
            validate_skinfolds([1, 0, 3], 3, "test")

    def test_non_numeric(self):
        with pytest.raises(TypeError, match="must be numeric"):
            validate_skinfolds([1, "two", 3], 3, "test")  # type: ignore[list-item]
