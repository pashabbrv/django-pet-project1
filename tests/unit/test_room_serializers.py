from decimal import Decimal

import pytest

from hotels.serializers import (
    RoomCreateSerializer,
    RoomDeleteSerializer,
    RoomListQuerySerializer,
)


def test_room_create_serializer_valid():
    serializer = RoomCreateSerializer(
        data={
            "description": "Standard room",
            "price_per_night": "3500.00",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["price_per_night"] == Decimal("3500.00")


def test_room_create_serializer_zero_price():
    serializer = RoomCreateSerializer(
        data={
            "description": "Free room",
            "price_per_night": "0.00",
        }
    )

    assert serializer.is_valid()


@pytest.mark.parametrize(
    "price",
    ["-1.00", "invalid", "1.001", "100000000.00"],
)
def test_room_create_serializer_invalid_price(price):
    serializer = RoomCreateSerializer(
        data={
            "description": "Standard room",
            "price_per_night": price,
        }
    )

    assert not serializer.is_valid()
    assert "price_per_night" in serializer.errors


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"description": "Standard room"},
        {"price_per_night": "3500.00"},
        {"description": "", "price_per_night": "3500.00"},
    ],
)
def test_room_create_serializer_required_fields(payload):
    serializer = RoomCreateSerializer(data=payload)

    assert not serializer.is_valid()


def test_room_list_query_serializer_defaults():
    serializer = RoomListQuerySerializer(data={})

    assert serializer.is_valid()
    assert serializer.validated_data == {
        "sort_by": "created_at",
        "order": "asc",
    }


def test_room_list_query_serializer_valid_options():
    serializer = RoomListQuerySerializer(
        data={
            "sort_by": "price",
            "order": "desc",
        }
    )

    assert serializer.is_valid()


@pytest.mark.parametrize(
    "payload",
    [
        {"sort_by": "unknown"},
        {"order": "sideways"},
    ],
)
def test_room_list_query_serializer_invalid_options(payload):
    serializer = RoomListQuerySerializer(data=payload)

    assert not serializer.is_valid()


def test_room_delete_serializer_valid():
    serializer = RoomDeleteSerializer(data={"room_id": 1})

    assert serializer.is_valid()


@pytest.mark.parametrize("room_id", [0, -1, "abc"])
def test_room_delete_serializer_invalid_id(room_id):
    serializer = RoomDeleteSerializer(data={"room_id": room_id})

    assert not serializer.is_valid()
