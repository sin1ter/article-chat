from django.contrib import admin

from .models import ChatSessions, ChatLog

admin.site.register(ChatSessions)
admin.site.register(ChatLog)