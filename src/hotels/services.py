from datetime import date
from decimal import Decimal

from django.shortcuts import get_object_or_404

from .models import Booking, Room


def create_room(*, description: str, price_per_night: Decimal) -> Room:
    return Room.objects.create(
        description=description,
        price_per_night=price_per_night,
    )


def delete_room(*, room_id: int) -> None:
    room = get_object_or_404(Room, id=room_id)
    room.delete()


def create_booking(*, room_id: int, date_start: date, date_end: date) -> Booking:
    room = get_object_or_404(Room, pk=room_id)

    return Booking.objects.create(
        room=room,
        date_start=date_start,
        date_end=date_end,
    )


def delete_booking(*, booking_id: int) -> None:
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
