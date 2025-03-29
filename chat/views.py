from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chatroom(request):
    """Create a new chatroom"""
    name = request.data.get("name")
    if not name:
        return Response({"error": "Chatroom name is required."}, status=status.HTTP_400_BAD_REQUEST)

    chatroom, created = ChatRoom.objects.get_or_create(name=name)
    chatroom.users.add(request.user)  # Add creator to the chatroom
    return Response({"message": "Chatroom created successfully", "room_id": chatroom.id}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_user_to_chatroom(request, room_id):
    """Add a user to a chatroom"""
    chatroom = get_object_or_404(ChatRoom, id=room_id)
    user_email = request.data.get("email")

    if not user_email:
        return Response({"error": "User email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    chatroom.add_user(user)
    return Response({"message": f"{user.email} added to chatroom."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_user_from_chatroom(request, room_id):
    """Remove a user from a chatroom"""
    chatroom = get_object_or_404(ChatRoom, id=room_id)
    user_email = request.data.get("email")

    if not user_email:
        return Response({"error": "User email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    chatroom.remove_user(user)
    return Response({"message": f"{user.email} removed from chatroom."}, status=status.HTTP_200_OK)
