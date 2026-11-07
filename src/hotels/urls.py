from django.urls import path

from .views import RoomCreateView, RoomDeleteView, RoomListView

urlpatterns = [
    path("rooms/create", RoomCreateView.as_view(), name="room-create"),
    path("rooms/delete", RoomDeleteView.as_view(), name="room-delete"),
    path("rooms/list", RoomListView.as_view(), name="room-list"),
]
