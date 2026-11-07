from django.db.models import QuerySet

from .models import Room


def get_rooms(*, sort_by: str, order: str) -> QuerySet[Room]:
    fields = {
        "price": "price_per_night",
        "created_at": "created_at",
    }

    field = fields[sort_by]

    if order == "desc":
        field = f"-{field}"

    return Room.objects.order_by(field, "id")
