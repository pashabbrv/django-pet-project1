from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_rooms
from .serializers import (
    RoomCreateSerializer,
    RoomDeleteSerializer,
    RoomListQuerySerializer,
    RoomSerializer,
)
from .services import create_room, delete_room


class RoomCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = create_room(**serializer.validated_data)

        return Response(
            {"room_id": room.id},
            status=status.HTTP_201_CREATED,
        )


class RoomDeleteView(APIView):
    def delete(self, request: Request) -> Response:
        serializer = RoomDeleteSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        delete_room(**serializer.validated_data)

        return Response({"deleted": True})


class RoomListView(APIView):
    def get(self, request: Request) -> Response:
        serializer = RoomListQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        rooms = get_rooms(**serializer.validated_data)

        return Response(RoomSerializer(rooms, many=True).data)
