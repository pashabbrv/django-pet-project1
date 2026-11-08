from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Booking, Room


def get_rooms(*, sort_by: str, order: str) -> QuerySet[Room]:
    fields = {
        "price": "price_per_night",
        "created_at": "created_at",
    }

    field = fields[sort_by]

    if order == "desc":
        field = f"-{field}"

    return Room.objects.order_by(field, "id")


def get_bookings(*, room_id: int) -> QuerySet[Booking]:
    get_object_or_404(Room, pk=room_id)

    return Booking.objects.filter(room_id=room_id).order_by("date_start", "id")
