from datetime import date

import pytest

from hotels.models import Booking

pytestmark = pytest.mark.django_db


def test_create_booking(api_client, room_factory):
    room = room_factory()

    response = api_client.post(
        "/bookings/create",
        {
            "room_id": room.id,
            "date_start": "2027-01-10",
            "date_end": "2027-01-15",
        },
        format="json",
    )

    assert response.status_code == 201

    booking_id = response.json()["booking_id"]
    booking = Booking.objects.get(pk=booking_id)

    assert booking.room_id == room.id
    assert booking.date_start == date(2027, 1, 10)
    assert booking.date_end == date(2027, 1, 15)


def test_create_booking_allows_past_and_overlapping_dates(
    api_client,
    room_factory,
):
    room = room_factory()

    payload = {
        "room_id": room.id,
        "date_start": "2020-01-30",
        "date_end": "2020-02-02",
    }

    first_response = api_client.post(
        "/bookings/create",
        payload,
        format="json",
    )

    second_response = api_client.post(
        "/bookings/create",
        payload,
        format="json",
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    assert Booking.objects.filter(room_id=room.id).count() == 2


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        ("2026-12-15", "2026-12-10"),
        ("2026-12-10", "2026-12-10"),
        ("2026-02-30", "2026-03-02"),
        ("2026-12-10", "2026-02-30"),
        ("30-01-2027", "2027-02-02"),
    ],
)
def test_create_booking_invalid_dates(
    api_client,
    room_factory,
    date_start,
    date_end,
):
    room = room_factory()
    initial_count = Booking.objects.count()

    response = api_client.post(
        "/bookings/create",
        {
            "room_id": room.id,
            "date_start": date_start,
            "date_end": date_end,
        },
        format="json",
    )

    assert response.status_code == 400
    assert Booking.objects.count() == initial_count


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"room_id": 1},
        {"room_id": 1, "date_start": "2027-01-10"},
        {
            "room_id": 1,
            "date_end": "2027-01-15",
        },
    ],
)
def test_create_booking_missing_fields(api_client, payload):
    initial_count = Booking.objects.count()

    response = api_client.post(
        "/bookings/create",
        payload,
        format="json",
    )

    assert response.status_code == 400
    assert Booking.objects.count() == initial_count


@pytest.mark.parametrize("room_id", [0, "abc"])
def test_create_booking_invalid_room_id(
    api_client,
    room_id,
):
    response = api_client.post(
        "/bookings/create",
        {
            "room_id": room_id,
            "date_start": "2027-01-10",
            "date_end": "2027-01-15",
        },
        format="json",
    )

    assert response.status_code == 400


def test_create_booking_room_not_found(api_client):
    response = api_client.post(
        "/bookings/create",
        {
            "room_id": 999999999,
            "date_start": "2027-01-10",
            "date_end": "2027-01-15",
        },
        format="json",
    )

    assert response.status_code == 404


def test_list_bookings_empty(api_client, room_factory):
    room = room_factory()

    response = api_client.get(f"/bookings/list?room_id={room.id}")

    assert response.status_code == 200
    assert response.json() == []


def test_list_bookings_sorted_by_date_start(
    api_client,
    room_factory,
    booking_factory,
):
    room = room_factory()

    first = booking_factory(
        room,
        date(2027, 2, 10),
        date(2027, 2, 15),
    )

    second = booking_factory(
        room,
        date(2027, 1, 10),
        date(2027, 1, 15),
    )

    third = booking_factory(
        room,
        date(2027, 1, 10),
        date(2027, 1, 20),
    )

    response = api_client.get(f"/bookings/list?room_id={room.id}")

    assert response.status_code == 200

    data = response.json()

    assert [item["booking_id"] for item in data] == [
        second.id,
        third.id,
        first.id,
    ]

    assert data[0]["date_start"] == "2027-01-10"
    assert data[0]["date_end"] == "2027-01-15"


def test_list_bookings_without_room_id(api_client):
    response = api_client.get("/bookings/list")

    assert response.status_code == 400


@pytest.mark.parametrize("room_id", ["0", "abc"])
def test_list_bookings_invalid_room_id(api_client, room_id):
    response = api_client.get(f"/bookings/list?room_id={room_id}")

    assert response.status_code == 400


def test_list_bookings_room_not_found(api_client):
    response = api_client.get("/bookings/list?room_id=999999999")

    assert response.status_code == 404


def test_delete_booking(api_client, room_factory, booking_factory):
    room = room_factory()

    booking = booking_factory(
        room,
        date(2027, 1, 10),
        date(2027, 1, 15),
    )

    response = api_client.delete(f"/bookings/delete?booking_id={booking.id}")

    assert response.status_code == 200
    assert response.json() == {"deleted": True}
    assert not Booking.objects.filter(pk=booking.id).exists()


def test_delete_booking_not_found(api_client):
    response = api_client.delete("/bookings/delete?booking_id=999999999")

    assert response.status_code == 404


@pytest.mark.parametrize("booking_id", ["0", "abc"])
def test_delete_booking_invalid_id(api_client, booking_id):
    response = api_client.delete(f"/bookings/delete?booking_id={booking_id}")

    assert response.status_code == 400


def test_delete_booking_without_id(api_client):
    response = api_client.delete("/bookings/delete")

    assert response.status_code == 400
