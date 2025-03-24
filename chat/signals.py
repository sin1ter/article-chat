from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import ChatSessions
from support_notify.models import Notification

@receiver(m2m_changed, sender=ChatSessions.participants.through)
def notify_participants(sender, instance, action, **kwargs):
    if action == "post_add":
        print("Chat session updated, sending notifications...")
        for user in instance.participants.all():
            Notification.objects.create(
                title="New Chat Session Created",
                content=f"You have been added to a chat: {instance.name}",
                user=user
            )
            print(f"Notification sent to {user.email}")
