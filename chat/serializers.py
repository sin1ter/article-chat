import uuid
from django.http import QueryDict
from rest_framework import serializers

from authentications.models import User
from .models import ChatLog, ChatSessions
from authentications.models import User

class ChatSessionsSerializer(serializers.ModelSerializer):
    participants = serializers.ListField(
        child=serializers.EmailField(), write_only=True
    )
    name = serializers.CharField(max_length=256)

    participant_details = serializers.SerializerMethodField()

    class Meta:
        model = ChatSessions
        fields = ('id', 'name', 'participants', 'participant_details', 'room_id', 'is_group')

    def get_participant_details(self, obj):
        # Return a list of dictionaries with user details
        return [
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            } for user in obj.participants.all()
        ]

    def create(self, validated_data):
        request_user = self.context['request'].user
        raw_data = self.context['request'].data
        print("Raw request data:", raw_data)

        # Get emails directly from raw_data using getlist for QueryDict
        if isinstance(raw_data, QueryDict):
            participant_emails = raw_data.getlist('participants')
        elif 'participants' in raw_data and isinstance(raw_data['participants'], list):
            participant_emails = raw_data['participants']
        else:
            participant_emails = []

        print("Participant emails from raw data:", participant_emails)


        # Check each email individually
        for email in participant_emails:
            user_exists = User.objects.filter(email=email).exists()
            print(f"Email {email} exists in database: {user_exists}")

        # Query the User model to get actual user objects from these emails
        participant_users = list(User.objects.filter(email__in=participant_emails))
        print("Participants found in database:", participant_users)

        # Add the request user if not already in the list
        if request_user not in participant_users:
            participant_users.append(request_user)

        is_group = len(participant_users) > 2

        print("Final participant list:", participant_users)

        # Create the chat session
        chat_session = ChatSessions.objects.create(
            name=validated_data.get('name', ''),
            is_group=is_group,
            room_id=validated_data.get('room_id', uuid.uuid4())
        )

        # Add all participant users to the chat session
        chat_session.participants.add(*participant_users)

        return chat_session