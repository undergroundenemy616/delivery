import pytest

from delivery.core.domain.model.courier_aggregate import Courier, CourierIsAlreadyBusyError, CourierStatus, Transport
from delivery.core.domain.model.shared_kernel.location import Location


class TestCourierShould:

    def test_success_create_when_params_is_correct(self) -> None:
        location = Location.create_random()
        name = "test-name"
        transport = Transport.car
        courier = Courier.create(name=name, location=location, transport=transport)

        assert courier
        assert courier.name == name
        assert courier.location == location
        assert courier.transport == transport
        assert courier.status == CourierStatus.free

    def test_success_set_busy(self) -> None:
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)

        courier.set_busy()

        assert courier.status == CourierStatus.busy

    def test_error_when_set_busy_to_already_busy_courier(self) -> None:
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)
        courier.set_busy()

        with pytest.raises(CourierIsAlreadyBusyError):
            courier.set_busy()

    def test_success_set_free(self) -> None:
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)

        courier.set_free()

        assert courier.status == CourierStatus.free

    @pytest.mark.parametrize(
        "courier_location, order_location, transport, expected_time",
        [
            (Location(X=5, Y=5), Location(X=10, Y=10), Transport.pedestrian, 10),
            (Location(X=5, Y=5), Location(X=10, Y=10), Transport.bicycle, 5),
            (Location(X=5, Y=5), Location(X=10, Y=10), Transport.car, 3.333),
        ],
    )
    def test_success_calculate_time_to_order_location(
        self, courier_location: Location, order_location: Location, transport: Transport, expected_time: float
    ) -> None:
        courier = Courier.create(name="name", location=courier_location, transport=transport)

        time = courier.calculate_time_to_order_location(order_location)

        assert round(time, 3) == expected_time

    @pytest.mark.parametrize(
        "courier_location, order_location, transport, expected_moves_location",
        [
            (
                Location(X=1, Y=1),
                Location(X=4, Y=1),
                Transport.pedestrian,
                (
                    Location(X=2, Y=1),
                    Location(X=3, Y=1),
                    Location(X=4, Y=1),
                ),
            ),
            (
                Location(X=1, Y=1),
                Location(X=4, Y=1),
                Transport.car,
                (
                    Location(X=4, Y=1),
                    Location(X=4, Y=1),
                ),
            ),
            (
                Location(X=1, Y=1),
                Location(X=5, Y=5),
                Transport.car,
                (
                    Location(X=4, Y=1),
                    Location(X=5, Y=3),
                    Location(X=5, Y=5),
                ),
            ),
            (
                Location(X=9, Y=8),
                Location(X=4, Y=1),
                Transport.car,
                (
                    Location(X=6, Y=8),
                    Location(X=4, Y=7),
                    Location(X=4, Y=4),
                    Location(X=4, Y=1),
                ),
            ),
        ],
    )
    def test_success_move(
        self,
        courier_location: Location,
        order_location: Location,
        transport: Transport,
        expected_moves_location: list[Location],
    ) -> None:
        courier = Courier.create(name="name", location=courier_location, transport=transport)

        for expected_move_location in expected_moves_location:
            courier.move(order_location)
            assert courier.location == expected_move_location
