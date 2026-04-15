import pytest

from fitness_tools.meals import meal_maker
from fitness_tools.models import MacroTargets
from fitness_tools.types import ActivityLevel, BodyType, Goal


class TestMakeMeal:

    # Error Checking

    @pytest.fixture(params=["mesomorf", 3, ""])
    def value_error_body_type(self, request):
        return request.param

    def test_body_type_raises_value_error(self, value_error_body_type):
        with pytest.raises((ValueError, AttributeError)):
            meal_maker.MakeMeal(150, body_type=value_error_body_type)

    @pytest.mark.parametrize(
        "fat_percent, carb_percent, protein_percent",
        [
            (None, 0.1, 0.2),
            (None, None, 0.1),
            (0.3, None, None),
            (None, None, None),
            (0.4, None, 0.3),
            (0.6, 0.4, None),
            ("six", "four", 0.1),
        ],
    )
    def test_macronutrient_percent_raises_type_error(
        self, fat_percent, carb_percent, protein_percent
    ):
        with pytest.raises(TypeError):
            meal_maker.MakeMeal(
                150,
                body_type=None,
                fat_percent=fat_percent,
                carb_percent=carb_percent,
                protein_percent=protein_percent,
            )

    @pytest.mark.parametrize(
        "fat_percent, carb_percent, protein_percent",
        [
            (0.9, 0.1, 0.2),
            (0.1, 0.2, 0.3),
        ],
    )
    def test_macronutrient_percent_raises_value_error(
        self, fat_percent, carb_percent, protein_percent
    ):
        with pytest.raises(ValueError):
            meal_maker.MakeMeal(
                150,
                body_type=None,
                fat_percent=fat_percent,
                carb_percent=carb_percent,
                protein_percent=protein_percent,
            )

    @pytest.fixture(params=[-150, 0])
    def value_error_check_weight(self, request):
        return request.param

    @pytest.fixture(params=["", "one-hundred", 150.5, 100.0])
    def type_error_check_weight(self, request):
        return request.param

    def test_check_weight_type_error(self, type_error_check_weight):
        with pytest.raises(TypeError):
            meal_maker.MakeMeal(type_error_check_weight)

    def test_check_weight_value_error(self, value_error_check_weight):
        with pytest.raises(ValueError):
            meal_maker.MakeMeal(value_error_check_weight)

    def test_set_optimum_calories_raises_value_error(self):
        with pytest.raises((ValueError, AttributeError)):
            meal_maker.MakeMeal(150, activity_level="vry", goal="weight_gain")

    @pytest.fixture(params=[0, -3, -10])
    def value_error_cal(self, request):
        return request.param

    def test_check_min_cal_raises_value_error(self, value_error_cal):
        with pytest.raises(ValueError):
            meal_maker.MakeMeal(150, body_type="mesomorph", min_cal=value_error_cal)

    def test_check_max_cal_raises_value_error(self, value_error_cal):
        with pytest.raises(ValueError):
            meal_maker.MakeMeal(150, body_type="mesomorph", max_cal=value_error_cal)

    @pytest.fixture(params=["", "three", 10.5])
    def type_error_cal(self, request):
        return request.param

    def test_check_min_cal_raises_type_error(self, type_error_cal):
        with pytest.raises(TypeError):
            meal_maker.MakeMeal(150, body_type="mesomorph", min_cal=type_error_cal)

    def test_check_max_cal_raises_type_error(self, type_error_cal):
        with pytest.raises(TypeError):
            meal_maker.MakeMeal(150, body_type="mesomorph", max_cal=type_error_cal)

    # Test assigned macronutrient percentages by body type

    @pytest.mark.parametrize(
        "body_type, expected",
        [
            ("MESOMORPH", 0.3),
            ("Ectomorph", 0.2),
            ("endomorph", 0.4),
        ],
    )
    def test_fat_percent(self, body_type, expected):
        assert meal_maker.MakeMeal(150, body_type=body_type).fat_percent == expected

    @pytest.mark.parametrize(
        "body_type, expected",
        [
            ("MESOMORPH", 0.3),
            ("Ectomorph", 0.25),
            ("endomorph", 0.35),
        ],
    )
    def test_protein_percent(self, body_type, expected):
        assert meal_maker.MakeMeal(150, body_type=body_type).protein_percent == expected

    @pytest.mark.parametrize(
        "body_type, expected",
        [
            ("MESOMORPH", 0.4),
            ("Ectomorph", 0.55),
            ("endomorph", 0.25),
        ],
    )
    def test_carb_percent(self, body_type, expected):
        assert meal_maker.MakeMeal(150, body_type=body_type).carb_percent == expected

    # Test calorie range by activity level and goal

    @pytest.mark.parametrize(
        "body_type, activity_level, goal, expected_min_cal",
        [
            ("mesomorph", "sedentary", "weight_loss", 10),
            ("mesomorph", "sedentary", "maintenance", 12),
            ("mesomorph", "sedentary", "weight_gain", 16),
            ("endomorph", "moderate", "weight_loss", 12),
            ("endomorph", "moderate", "maintenance", 14),
            ("endomorph", "moderate", "weight_gain", 18),
            ("ectomorph", "very", "weight_loss", 14),
            ("ectomorph", "very", "maintenance", 16),
            ("ectomorph", "very", "weight_gain", 20),
        ],
    )
    def test_expected_min_cal(self, body_type, activity_level, goal, expected_min_cal):
        assert (
            meal_maker.MakeMeal(
                150, body_type=body_type, activity_level=activity_level, goal=goal
            ).min_cal
            == expected_min_cal
        )

    @pytest.mark.parametrize(
        "body_type, activity_level, goal, expected_max_cal",
        [
            ("mesomorph", "sedentary", "weight_loss", 12),
            ("mesomorph", "sedentary", "maintenance", 14),
            ("mesomorph", "sedentary", "weight_gain", 18),
            ("endomorph", "moderate", "weight_loss", 14),
            ("endomorph", "moderate", "maintenance", 16),
            ("endomorph", "moderate", "weight_gain", 20),
            ("ectomorph", "very", "weight_loss", 16),
            ("ectomorph", "very", "maintenance", 18),
            ("ectomorph", "very", "weight_gain", 22),
        ],
    )
    def test_expected_max_cal(self, body_type, activity_level, goal, expected_max_cal):
        assert (
            meal_maker.MakeMeal(
                150, body_type=body_type, activity_level=activity_level, goal=goal
            ).max_cal
            == expected_max_cal
        )

    # test daily requirements returns MacroTargets dataclass

    @pytest.mark.parametrize(
        "weight, body_type, activity_level, goal, min_cal, max_cal, "
        "fat_percent, carb_percent, protein_percent, expected",
        [
            (
                150, "mesomorph", "very", "maintenance", None, None, None, None, None,
                MacroTargets(
                    min_calories=2400, max_calories=2700, min_fat=80.0,
                    max_fat=90.0, min_protein=180.0, max_protein=202.0,
                    min_carbs=240.0, max_carbs=270.0,
                ),
            ),
            (
                200, None, "sedentary", "weight_loss", None, None, 0.3, 0.2, 0.5,
                MacroTargets(
                    min_calories=2000, max_calories=2400, min_fat=67.0,
                    max_fat=80.0, min_protein=250.0, max_protein=300.0,
                    min_carbs=100.0, max_carbs=120.0,
                ),
            ),
            (
                175, "ectomorph", None, None, 10, 14, None, None, None,
                MacroTargets(
                    min_calories=1750, max_calories=2450, min_fat=39.0,
                    max_fat=54.0, min_protein=109.0, max_protein=153.0,
                    min_carbs=241.0, max_carbs=337.0,
                ),
            ),
            (
                250, None, None, None, 12, 14, 0.25, 0.55, 0.2,
                MacroTargets(
                    min_calories=3000, max_calories=3500, min_fat=83.0,
                    max_fat=97.0, min_protein=150.0, max_protein=175.0,
                    min_carbs=413.0, max_carbs=481.0,
                ),
            ),
        ],
    )
    def test_daily_requirements(
        self, weight, body_type, activity_level, goal, min_cal,
        max_cal, fat_percent, carb_percent, protein_percent, expected,
    ):
        result = meal_maker.MakeMeal(
            weight,
            body_type=body_type,
            activity_level=activity_level,
            goal=goal,
            min_cal=min_cal,
            max_cal=max_cal,
            fat_percent=fat_percent,
            carb_percent=carb_percent,
            protein_percent=protein_percent,
        ).daily_requirements()
        assert result == expected

    # test make_meal returns MacroTargets dataclass

    @pytest.mark.parametrize(
        "weight, meals, body_type, activity_level, goal, min_cal, max_cal, "
        "fat_percent, carb_percent, protein_percent, expected",
        [
            (
                150, 5, "mesomorph", "very", "maintenance", None, None, None, None, None,
                MacroTargets(
                    min_calories=480.0, max_calories=540.0, min_fat=16.0,
                    max_fat=18.0, min_protein=36.0, max_protein=40.0,
                    min_carbs=48.0, max_carbs=54.0,
                ),
            ),
            (
                200, 6, None, "sedentary", "weight_loss", None, None, 0.3, 0.2, 0.5,
                MacroTargets(
                    min_calories=333.0, max_calories=400.0, min_fat=11.0,
                    max_fat=13.0, min_protein=42.0, max_protein=50.0,
                    min_carbs=17.0, max_carbs=20.0,
                ),
            ),
            (
                175, 4, "ectomorph", None, None, 10, 14, None, None, None,
                MacroTargets(
                    min_calories=438.0, max_calories=612.0, min_fat=10.0,
                    max_fat=14.0, min_protein=27.0, max_protein=38.0,
                    min_carbs=60.0, max_carbs=84.0,
                ),
            ),
            (
                250, 3, None, None, None, 12, 14, 0.25, 0.55, 0.2,
                MacroTargets(
                    min_calories=1000.0, max_calories=1167.0, min_fat=28.0,
                    max_fat=32.0, min_protein=50.0, max_protein=58.0,
                    min_carbs=138.0, max_carbs=160.0,
                ),
            ),
        ],
    )
    def test_make_meal(
        self, weight, meals, body_type, activity_level, goal, min_cal,
        max_cal, fat_percent, carb_percent, protein_percent, expected,
    ):
        result = meal_maker.MakeMeal(
            weight,
            body_type=body_type,
            activity_level=activity_level,
            goal=goal,
            min_cal=min_cal,
            max_cal=max_cal,
            fat_percent=fat_percent,
            carb_percent=carb_percent,
            protein_percent=protein_percent,
        ).make_meal(meals)
        assert result == expected

    # Test enum inputs

    def test_enum_body_type(self):
        m = meal_maker.MakeMeal(150, body_type=BodyType.MESOMORPH)
        assert m.fat_percent == 0.3
        assert m.protein_percent == 0.3
        assert m.carb_percent == 0.4

    def test_enum_activity_level_and_goal(self):
        m = meal_maker.MakeMeal(
            150,
            body_type=BodyType.MESOMORPH,
            activity_level=ActivityLevel.VERY,
            goal=Goal.MAINTENANCE,
        )
        assert m.min_cal == 16
        assert m.max_cal == 18

    # Test MacroTargets dict-compat

    def test_daily_requirements_dict_access(self):
        m = meal_maker.MakeMeal(
            150,
            body_type="mesomorph",
            activity_level="very",
            goal="maintenance",
        )
        result = m.daily_requirements()
        with pytest.warns(DeprecationWarning):
            assert result["min_calories"] == 2400
        assert result.min_calories == 2400

    def test_daily_requirements_is_macro_targets(self):
        m = meal_maker.MakeMeal(
            150,
            body_type="mesomorph",
            activity_level="very",
            goal="maintenance",
        )
        result = m.daily_requirements()
        assert isinstance(result, MacroTargets)

    def test_make_meal_is_macro_targets(self):
        m = meal_maker.MakeMeal(
            150,
            body_type="mesomorph",
            activity_level="very",
            goal="maintenance",
        )
        result = m.make_meal(5)
        assert isinstance(result, MacroTargets)

    def test_invalid_body_type_enum_value(self):
        with pytest.raises(ValueError):
            meal_maker.MakeMeal(150, body_type="invalid_type")
