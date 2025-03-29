from rest_framework import permissions, views, status
from .serializers import RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

# view for registering users
class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterUserSerializer,
        responses={200: dict},
    )

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response({
            "user": {
                "email": user_data["user"].email,
                "username": user_data["user"].username,
                "first_name": user_data["user"].first_name,
                "last_name": user_data["user"].last_name,
            },
            "refresh": user_data["refresh"],
            "access": user_data["access"],
        }, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginUserSerializer,
        responses={200: dict},
    )
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )