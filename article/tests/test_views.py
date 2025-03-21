from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from article.models import Article, ArticleCategory
from authentications.models import User

class ArticleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test123@gmail.com", username='testuser', first_name="first name", last_name="last name", password='testpassword')
        self.category = ArticleCategory.objects.create(name='Tech')
        self.client.login(username='testuser', password='testpassword')
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_articles(self):
        url = reverse("article-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_article(self):
        url = reverse("article-list")
        data = {
            'category': self.category.id,
            'title': 'Test Article',
            'content': 'This is a test article'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.data["title"], "New API Article")

