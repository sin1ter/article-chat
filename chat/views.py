from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from authentications.models import User

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically add the logged-in user to the chatroom
        serializer.save(users=[self.request.user])

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        """Add a user to the chatroom."""
        chatroom = self.get_object()
        user_email = request.data.get("email")

        if not user_email:
            return Response({"error": "User email is required."}, status=400)

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        # Add the user to the chatroom
        chatroom.users.add(user)
        return Response({"message": f"{user.email} added to chatroom."}, status=200)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return messages only from a specific chat room."""
        chat_room_id = self.request.query_params.get("chat_room_id")
        if chat_room_id:
            return Message.objects.filter(room_id=chat_room_id).order_by("timestamp")
        return Message.objects.none()
    