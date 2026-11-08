from datetime import date

import pytest

from hotels.serializers import (
    BookingCreateSerializer,
    BookingDeleteSerializer,
    BookingRoomQuerySerializer,
)


def test_booking_create_serializer_valid():
    serializer = BookingCreateSerializer(
        data={
            "room_id": 1,
            "date_start": "2027-01-10",
            "date_end": "2027-01-15",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["date_start"] == date(2027, 1, 10)
    assert serializer.validated_data["date_end"] == date(2027, 1, 15)


@pytest.mark.parametrize(
    ("date_start", "date_end"),
    [
        ("2027-01-15", "2027-01-10"),
        ("2027-01-10", "2027-01-10"),
        ("2027-02-30", "2027-03-02"),
        ("10-01-2027", "2027-01-15"),
    ],
)
def test_booking_create_serializer_invalid_dates(
    date_start,
    date_end,
):
    serializer = BookingCreateSerializer(
        data={
            "room_id": 1,
            "date_start": date_start,
            "date_end": date_end,
        }
    )

    assert not serializer.is_valid()


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"room_id": 1},
        {"date_start": "2027-01-10"},
        {"date_end": "2027-01-15"},
    ],
)
def test_booking_create_serializer_required_fields(payload):
    serializer = BookingCreateSerializer(data=payload)

    assert not serializer.is_valid()


@pytest.mark.parametrize("room_id", [0, -1, "abc"])
def test_booking_create_serializer_invalid_room_id(room_id):
    serializer = BookingCreateSerializer(
        data={
            "room_id": room_id,
            "date_start": "2027-01-10",
            "date_end": "2027-01-15",
        }
    )

    assert not serializer.is_valid()


def test_booking_delete_serializer_valid():
    serializer = BookingDeleteSerializer(data={"booking_id": 1})

    assert serializer.is_valid()


@pytest.mark.parametrize("booking_id", [0, -1, "abc"])
def test_booking_delete_serializer_invalid_id(booking_id):
    serializer = BookingDeleteSerializer(data={"booking_id": booking_id})

    assert not serializer.is_valid()


def test_booking_room_query_serializer_valid():
    serializer = BookingRoomQuerySerializer(data={"room_id": 1})

    assert serializer.is_valid()


def test_booking_room_query_serializer_invalid_id():
    serializer = BookingRoomQuerySerializer(data={"room_id": 0})

    assert not serializer.is_valid()
