from decimal import Decimal

from django.shortcuts import get_object_or_404

from .models import Room


def create_room(*, description: str, price_per_night: Decimal) -> Room:
    return Room.objects.create(
        description=description,
        price_per_night=price_per_night,
    )


def delete_room(*, room_id: int) -> None:
    room = get_object_or_404(Room, id=room_id)
    room.delete()
