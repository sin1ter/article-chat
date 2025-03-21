from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views import ArticleCategoryViewSet, ArticleViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewset with a URL prefix
router.register(r"categories", ArticleCategoryViewSet, basename="categories")
router.register(r"article", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
]
