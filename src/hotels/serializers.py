from decimal import Decimal
from typing import Any

from rest_framework import serializers

from .models import Booking, Room


class RoomCreateSerializer(serializers.Serializer):
    description = serializers.CharField()
    price_per_night = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0"),
    )


class RoomDeleteSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)


class RoomListQuerySerializer(serializers.Serializer):
    sort_by = serializers.ChoiceField(
        choices=["price", "created_at"],
        default="created_at",
    )
    order = serializers.ChoiceField(
        choices=["asc", "desc"],
        default="asc",
    )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)
    date_start = serializers.DateField(input_formats=["%Y-%m-%d"])
    date_end = serializers.DateField(input_formats=["%Y-%m-%d"])

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["date_end"] <= attrs["date_start"]:
            raise serializers.ValidationError(
                {"date_end": "Дата окончания должна быть позже даты начала."}
            )
        return attrs


class BookingDeleteSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField(min_value=1)


class BookingRoomQuerySerializer(serializers.Serializer):
    room_id = serializers.IntegerField(min_value=1)


class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end"]
