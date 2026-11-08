from datetime import date, timedelta
from decimal import Decimal

from django.utils import timezone
import pytest

from hotels.models import Booking, Room

pytestmark = pytest.mark.django_db


def test_create_room(api_client):
    response = api_client.post(
        "/rooms/create",
        {
            "description": "Standard double room",
            "price_per_night": "3500.00",
        },
        format="json",
    )

    assert response.status_code == 201

    room_id = response.json()["room_id"]
    room = Room.objects.get(pk=room_id)

    assert room.description == "Standard double room"
    assert room.price_per_night == Decimal("3500.00")


def test_create_room_with_zero_price(api_client):
    response = api_client.post(
        "/rooms/create",
        {
            "description": "Free room",
            "price_per_night": "0.00",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Room.objects.get(pk=response.json()["room_id"]).price_per_night == Decimal("0.00")


@pytest.mark.parametrize(
    "price",
    ["-1.00", "invalid", "1.001", "100000000.00"],
)
def test_create_room_invalid_price(api_client, price):
    initial_count = Room.objects.count()

    response = api_client.post(
        "/rooms/create",
        {
            "description": "Standard room",
            "price_per_night": price,
        },
        format="json",
    )

    assert response.status_code == 400
    assert Room.objects.count() == initial_count


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"description": "Standard room"},
        {"price_per_night": "3500.00"},
        {"description": "", "price_per_night": "3500.00"},
        {"description": "Standard room", "price_per_night": ""},
    ],
)
def test_create_room_invalid_payload(api_client, payload):
    initial_count = Room.objects.count()

    response = api_client.post(
        "/rooms/create",
        payload,
        format="json",
    )

    assert response.status_code == 400
    assert Room.objects.count() == initial_count


def test_list_rooms_empty(api_client):
    response = api_client.get("/rooms/list")

    assert response.status_code == 200
    assert response.json() == []


def test_list_rooms_returns_room_data(api_client, room_factory):
    room = room_factory()

    response = api_client.get("/rooms/list")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == room.id
    assert data[0]["description"] == room.description
    assert data[0]["price_per_night"] == "3500.00"
    assert "created_at" in data[0]


@pytest.mark.parametrize(
    ("order", "expected_indexes"),
    [
        ("asc", [0, 2, 1]),
        ("desc", [1, 0, 2]),
    ],
)
def test_list_rooms_sort_by_price(
    api_client,
    room_factory,
    order,
    expected_indexes,
):
    rooms = [
        room_factory(price_per_night="100.00"),
        room_factory(price_per_night="300.00"),
        room_factory(price_per_night="100.00"),
    ]

    response = api_client.get(f"/rooms/list?sort_by=price&order={order}")

    assert response.status_code == 200

    actual_ids = [item["id"] for item in response.json()]
    expected_ids = [rooms[index].id for index in expected_indexes]

    assert actual_ids == expected_ids


@pytest.mark.parametrize(
    ("order", "expected_indexes"),
    [
        ("asc", [0, 2, 1]),
        ("desc", [1, 2, 0]),
    ],
)
def test_list_rooms_sort_by_created_at(
    api_client,
    room_factory,
    order,
    expected_indexes,
):
    rooms = [
        room_factory(),
        room_factory(),
        room_factory(),
    ]

    now = timezone.now()

    timestamps = [
        now - timedelta(days=2),
        now,
        now - timedelta(days=1),
    ]

    for room, created_at in zip(rooms, timestamps, strict=True):
        Room.objects.filter(pk=room.pk).update(created_at=created_at)

    response = api_client.get(f"/rooms/list?sort_by=created_at&order={order}")

    assert response.status_code == 200

    actual_ids = [item["id"] for item in response.json()]
    expected_ids = [rooms[index].id for index in expected_indexes]

    assert actual_ids == expected_ids


@pytest.mark.parametrize(
    "query",
    [
        "?sort_by=unknown",
        "?order=sideways",
    ],
)
def test_list_rooms_invalid_sort_parameters(api_client, query):
    response = api_client.get(f"/rooms/list{query}")

    assert response.status_code == 400


def test_delete_room(api_client, room_factory):
    room = room_factory()

    response = api_client.delete(f"/rooms/delete?room_id={room.id}")

    assert response.status_code == 200
    assert response.json() == {"deleted": True}
    assert not Room.objects.filter(pk=room.id).exists()


def test_delete_room_not_found(api_client):
    response = api_client.delete("/rooms/delete?room_id=999999999")

    assert response.status_code == 404


@pytest.mark.parametrize("room_id", ["0", "abc"])
def test_delete_room_invalid_id(api_client, room_id):
    response = api_client.delete(f"/rooms/delete?room_id={room_id}")

    assert response.status_code == 400


def test_delete_room_without_id(api_client):
    response = api_client.delete("/rooms/delete")

    assert response.status_code == 400


def test_delete_room_with_bookings(
    api_client,
    room_factory,
    booking_factory,
):
    room = room_factory()

    bookings = [
        booking_factory(
            room,
            date_start=date(2027, 1, 10),
            date_end=date(2027, 1, 15),
        ),
        booking_factory(
            room,
            date_start=date(2027, 1, 10),
            date_end=date(2027, 1, 15),
        ),
    ]

    response = api_client.delete(f"/rooms/delete?room_id={room.id}")

    assert response.status_code == 200
    assert not Room.objects.filter(pk=room.id).exists()

    for booking in bookings:
        assert not Booking.objects.filter(pk=booking.id).exists()
