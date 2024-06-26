import pytest
from pydantic import ValidationError
from delivery.core.domain.model.shared_kernel.location import Location


class TestLocationShould:
    @pytest.mark.parametrize(
        "x, y",
        [
            (1, 4),
            (1, 1),
            (10, 10),
        ],
    )
    def test_success_create_when_params_is_correct(self, x: int, y: int):
        location = Location(X=x, Y=y)
        assert location.X == x
        assert location.Y == y

    @pytest.mark.parametrize(
        "x, y",
        [
            (-1, 4),
            (4, -1),
            (11, 4),
            (4, 11),
            (-1, -1),
            (-11, -11)
        ],
    )
    def test_return_error_when_params_is_incorrect_on_creation(self, x: int, y: int):
        with pytest.raises(ValidationError):
            Location(X=x, Y=y)

    @pytest.mark.parametrize(
        "x, y",
        [
            (4, None),
            (None, 4),
            (None, None),

        ],
    )
    def test_return_error_when_init_without_required_coordinates(self, x: int, y: int):
        with pytest.raises(ValidationError):
            Location(X=x, Y=y)

    @pytest.mark.parametrize(
        "x1, y1, x2, y2, distance",
        [
            (1, 2, 5, 6, 8),
            (10, 5, 1, 1, 13),
            (1, 1, 10, 10, 18),

        ],
    )
    def test_calculate_distance_with_another_location_right(self, x1: int, y1: int, x2: int, y2: int, distance: int):
        location1 = Location(X=x1, Y=y1)
        location2 = Location(X=x2, Y=y2)
        location_distance = location1.distance_to(location2)
        assert location_distance == distance

    def test_can_not_change_fields_values(self):
        location = Location(X=2, Y=3)
        with pytest.raises(ValidationError):
            location.X = 5
