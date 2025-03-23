from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import ChatLog, ChatSessions
from .serializers import ChatSessionsSerializer


class ChatSessionsViewSet(viewsets.ModelViewSet):
    queryset = ChatSessions.objects.all()
    serializer_class = ChatSessionsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['participants', 'room_id', 'is_group']
    ordering_fields = ['id']
    ordering = ['-id']
    search_fields = ['participants__username', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(participants__in=[self.request.user])
        return queryset

    def perform_create(self, serializer):

        serializer.save(participants=[self.request.user])


