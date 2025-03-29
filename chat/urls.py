from django.urls import path
from .views import create_chatroom, add_user_to_chatroom, remove_user_from_chatroom

urlpatterns = [
    path("create/", create_chatroom, name="create_chatroom"),
    path("add-user/<int:room_id>/", add_user_to_chatroom, name="add_user_to_chatroom"),
    path("remove-user/<int:room_id>/", remove_user_from_chatroom, name="remove_user_from_chatroom"),
]
