from rest_framework import serializers
from .models import ChatRoom, Message
from authentications.models import User

class ChatRoomSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'users', 'user_info']

    def get_user_info(self, obj):
        return [
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in obj.users.all()
        ]

    def create(self, validated_data):
        # Get the current request to automatically add the logged-in user
        request = self.context.get('request')
        chatroom = ChatRoom.objects.create(name=validated_data['name'])
        chatroom.users.add(request.user)  # Add logged-in user automatically
        return chatroom



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'timestamp']
        read_only_fields = ['user', 'timestamp', 'room']  

    def create(self, validated_data):
        request = self.context.get('request')
        chat_room_id = request.query_params.get("chat_room_id") 

        if not chat_room_id:
            raise serializers.ValidationError({"chat_room_id": "This field is required in query params."})

        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError({"chat_room_id": "Chat room does not exist."})

        validated_data['room'] = chat_room  
        validated_data['user'] = request.user  

        return super().create(validated_data)
