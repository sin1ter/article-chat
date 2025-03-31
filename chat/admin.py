from django.contrib import admin
from .models import *

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message)
