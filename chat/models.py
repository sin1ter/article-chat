import uuid
from django.db import models
from authentications.models import User
from support.models import BaseModel

class ChatSessions(BaseModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name="chat_sessions")
    room_id = models.CharField(max_length=256, unique=True, default=uuid.uuid4)
    is_group = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room_id'],
                name="unique_one_to_one_chat",
                condition=models.Q(is_group=False),
                violation_error_message="A one-on-one chat already exists."
            )
        ]

    def __str__(self):
        return self.name

class ChatLog(BaseModel):
    room = models.ForeignKey(
        ChatSessions,
        on_delete=models.CASCADE,
        related_name="chat_logs"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    content = models.CharField(max_length=1024, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]} ({self.timestamp})"

