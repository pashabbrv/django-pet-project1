from decimal import Decimal

from rest_framework import serializers

from .models import Room


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
