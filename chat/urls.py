from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import ChatSessionsViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewset with a URL prefix
router.register(r"chat", ChatSessionsViewSet, basename="chats")

urlpatterns = [
    path("", include(router.urls)),
]
