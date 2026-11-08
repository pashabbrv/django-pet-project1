from datetime import date
from decimal import Decimal
from pathlib import Path

from django.db import connection
import pytest
from rest_framework.test import APIClient

from hotels.models import Booking, Room


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"
    sql = schema_path.read_text(encoding="utf-8")

    with django_db_blocker.unblock(), connection.cursor() as cursor:
        for statement in sql.split(";"):
            if statement.strip():
                cursor.execute(statement)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def room_factory(db):
    def create_room(
        description: str = "Standard double room",
        price_per_night: str = "3500.00",
    ) -> Room:
        return Room.objects.create(
            description=description,
            price_per_night=Decimal(price_per_night),
        )

    return create_room


@pytest.fixture
def booking_factory(db):
    def create_booking(
        room: Room,
        date_start: date,
        date_end: date,
    ) -> Booking:
        return Booking.objects.create(
            room=room,
            date_start=date_start,
            date_end=date_end,
        )

    return create_booking
