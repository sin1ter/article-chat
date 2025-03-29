from django.db import models
from django.conf import settings

from authentications.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name="chatrooms")  # Users in chatroom

    def add_user(self, user):
        """Add a user to the chatroom."""
        self.users.add(user)

    def remove_user(self, user):
        """Remove a user from the chatroom."""
        self.users.remove(user)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return f"{self.user.email}: {self.content[:20]}"
