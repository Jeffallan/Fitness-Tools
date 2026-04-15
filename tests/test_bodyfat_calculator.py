import pytest

from fitness_tools.composition import bodyfat
from fitness_tools.types import Sex


class TestGenericCalculator:

    # error testing
    @pytest.fixture(params=["", "20", "twenty", -20])
    def value_error_age(self, request):
        return request.param

    @pytest.fixture(params=[1, "mal", "FEM", ""])
    def value_error_sex(self, request):
        return request.param

    @pytest.fixture(params=[(-1, 2, 3), ("str", 2), ("one", 2, -3)])
    def value_error_skinfolds(self, request):
        return request.param
    # end error testing

    @pytest.mark.parametrize(
        "age,sex,skinfolds,expected",
        [
            (30, "male", (1, 2, 3), 6),
            (20, "female", (1, 2, 3, 4), 10),
            (45, "Male", (1, 2), 3),
            (50, "FEMALE", (1, 2, 3, 4, 5), 15),
        ],
    )
    def test_sum_folds(self, age, sex, skinfolds, expected):
        assert bodyfat.GenericCalculator(age, sex, skinfolds).sum_folds == expected

    @pytest.mark.parametrize(
        "age,sex,skinfolds,expected",
        [
            (30, "male", (1, 2, 3), 36),
            (20, "female", (1, 2, 3, 4), 100),
            (45, "Male", (1, 2), 9),
            (50, "FEMALE", (1, 2, 3, 4, 5), 225),
        ],
    )
    def test_square_folds(self, age, sex, skinfolds, expected):
        assert bodyfat.GenericCalculator(age, sex, skinfolds).square_folds == expected

    @pytest.mark.parametrize(
        "age,sex,skinfolds,expected",
        [
            (30, "male", (1, 2, 3), 0.78),
            (20, "female", (1, 2, 3, 4), 1),
            (45, "Male", (1, 2), 0.48),
            (50, "FEMALE", (1, 2, 3, 4, 5), 1.17),
        ],
    )
    def test_log_sum(self, age, sex, skinfolds, expected):
        assert bodyfat.GenericCalculator(age, sex, skinfolds).log_sum == pytest.approx(
            expected, rel=1e-2
        )

    def test_age_raises_value_error(self, value_error_age):
        with pytest.raises(ValueError):
            bodyfat.GenericCalculator(value_error_age, "male", (1, 2, 3))

    def test_sex_raises_value_error(self, value_error_sex):
        with pytest.raises(ValueError):
            bodyfat.GenericCalculator(28, value_error_sex, (1, 2, 3))

    def test_skinfolds_raises_value_error(self, value_error_skinfolds):
        with pytest.raises((ValueError, TypeError)):
            bodyfat.GenericCalculator(50, "male", value_error_skinfolds)

    # enum input tests
    def test_accepts_sex_enum(self):
        calc = bodyfat.GenericCalculator(30, Sex.MALE, (1, 2, 3))
        assert calc.sex == Sex.MALE

    def test_accepts_sex_string(self):
        calc = bodyfat.GenericCalculator(30, "female", (1, 2, 3))
        assert calc.sex == Sex.FEMALE


class TestDurninWomersley:

    @pytest.fixture
    def durnin_wormersley_object(self):
        return bodyfat.DurninWomersley(45, "MALE", (1, 2, 3, 4))

    @pytest.fixture(
        params=[
            (-1, 2, 3),
            ("str", 2),
            ("one", 2, -3),
            (1, 2, 3),
            (1, 2, 3, 4, 5),
        ]
    )
    def value_error_skinfolds(self, request):
        return request.param

    def test_skinfolds_raise_value_error(self, value_error_skinfolds):
        with pytest.raises((ValueError, TypeError)):
            bodyfat.DurninWomersley(45, "MALE", value_error_skinfolds)

    def test_siri_equation(self, durnin_wormersley_object):
        assert durnin_wormersley_object.siri(
            durnin_wormersley_object.body_density()
        ) == pytest.approx(3.3, rel=1e-1)

    def test_brozek_equation(self, durnin_wormersley_object):
        assert durnin_wormersley_object.brozek(
            durnin_wormersley_object.body_density()
        ) == pytest.approx(4.3, rel=1e-1)

    def test_schutte_equation(self, durnin_wormersley_object):
        assert durnin_wormersley_object.schutte(
            durnin_wormersley_object.body_density()
        ) == pytest.approx(7.7, rel=1e-1)

    def test_wagner_equation(self, durnin_wormersley_object):
        assert durnin_wormersley_object.wagner(
            durnin_wormersley_object.body_density()
        ) == pytest.approx(6.0, rel=1e-1)

    def test_ortiz_equation(self, durnin_wormersley_object):
        assert durnin_wormersley_object.ortiz(
            durnin_wormersley_object.body_density()
        ) == pytest.approx(5.6, rel=1e-1)


class TestJacksonPollock7Site:

    @pytest.fixture
    def jackson_pollock_7_site_object(self):
        return bodyfat.JacksonPollock7Site(45, "MALE", (1, 2, 3, 4, 5, 6, 7))

    @pytest.fixture(
        params=[
            (-1, 2, 3),
            ("str", 2),
            ("one", 2, -3),
            (1, 2, 3),
            (1, 2, 3, 4, 5),
            (1, 2, 3, 4, 5, 6),
            (1, 2, 3, 4, 5, 6, 7, 8),
        ]
    )
    def value_error_skinfolds(self, request):
        return request.param

    def test_skinfolds_raise_value_error(self, value_error_skinfolds):
        with pytest.raises((ValueError, TypeError)):
            bodyfat.JacksonPollock7Site(45, "MALE", value_error_skinfolds)

    def test_siri_equation(self, jackson_pollock_7_site_object):
        assert jackson_pollock_7_site_object.siri(
            jackson_pollock_7_site_object.body_density()
        ) == pytest.approx(5.3, rel=1e-1)

    def test_brozek_equation(self, jackson_pollock_7_site_object):
        assert jackson_pollock_7_site_object.brozek(
            jackson_pollock_7_site_object.body_density()
        ) == pytest.approx(6.1, rel=1e-1)

    def test_schutte_equation(self, jackson_pollock_7_site_object):
        assert jackson_pollock_7_site_object.schutte(
            jackson_pollock_7_site_object.body_density()
        ) == pytest.approx(9.5, rel=1e-1)

    def test_wagner_equation(self, jackson_pollock_7_site_object):
        assert jackson_pollock_7_site_object.wagner(
            jackson_pollock_7_site_object.body_density()
        ) == pytest.approx(8.0, rel=1e-1)

    def test_ortiz_equation(self, jackson_pollock_7_site_object):
        assert jackson_pollock_7_site_object.ortiz(
            jackson_pollock_7_site_object.body_density()
        ) == pytest.approx(7.5, rel=1e-1)


class TestJacksonPollock4Site:

    @pytest.fixture(
        params=[
            (-1, 2, 3),
            ("str", 2),
            ("one", 2, -3),
            (1, 2, 3),
            (1, 2, 3, 4, 5),
            (1, 2, 3, 4, 5, 6),
            (1, 2, 3, 4, 5, 6, 7, 8),
        ]
    )
    def value_error_skinfolds(self, request):
        return request.param

    def test_skinfolds_raise_value_error(self, value_error_skinfolds):
        with pytest.raises((ValueError, TypeError)):
            bodyfat.JacksonPollock4Site(45, "MALE", value_error_skinfolds)

    @pytest.mark.parametrize(
        "age,sex,skinfolds,expected",
        [
            (45, "male", (1, 2, 3, 4), 4.2),
            (45, "female", (1, 2, 3, 4), 5.7),
        ],
    )
    def test_body_fat(self, age, sex, skinfolds, expected):
        assert bodyfat.JacksonPollock4Site(age, sex, skinfolds).body_fat() == expected


class TestJacksonPollock3Site:
    @pytest.fixture
    def jackson_pollock_3_site_object(self):
        return bodyfat.JacksonPollock3Site(45, "MALE", (1, 2, 3))

    @pytest.fixture(
        params=[
            (-1, 2, 3),
            ("str", 2),
            ("one", 2, -3),
            (1, 2, 3, 4),
            (1, 2, 3, 4, 5),
            (1, 2, 3, 4, 5, 6),
            (1, 2, 3, 4, 5, 6, 7, 8),
        ]
    )
    def value_error_skinfolds(self, request):
        return request.param

    def test_skinfolds_raise_value_error(self, value_error_skinfolds):
        with pytest.raises((ValueError, TypeError)):
            bodyfat.JacksonPollock3Site(45, "male", value_error_skinfolds)

    def test_siri_equation(self, jackson_pollock_3_site_object):
        assert jackson_pollock_3_site_object.siri(
            jackson_pollock_3_site_object.body_density()
        ) == pytest.approx(2.6, rel=1e-1)

    def test_brozek_equation(self, jackson_pollock_3_site_object):
        assert jackson_pollock_3_site_object.brozek(
            jackson_pollock_3_site_object.body_density()
        ) == pytest.approx(3.7, rel=1e-1)

    def test_schutte_equation(self, jackson_pollock_3_site_object):
        assert jackson_pollock_3_site_object.schutte(
            jackson_pollock_3_site_object.body_density()
        ) == pytest.approx(7.1, rel=1e-1)

    def test_wagner_equation(self, jackson_pollock_3_site_object):
        assert jackson_pollock_3_site_object.wagner(
            jackson_pollock_3_site_object.body_density()
        ) == pytest.approx(5.4, rel=1e-1)

    def test_ortiz_equation(self, jackson_pollock_3_site_object):
        assert jackson_pollock_3_site_object.ortiz(
            jackson_pollock_3_site_object.body_density()
        ) == pytest.approx(4.9, rel=1e-1)
