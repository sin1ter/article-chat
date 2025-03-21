from django.test import TestCase
from article.models import Article, ArticleCategory
from authentications.models import User


class ArticleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password="pasword123")
        self.category = ArticleCategory.objects.create(name="Tech")
        self.article = Article.objects.create(
            user=self.user,
            category=self.category,
            title="Test Article",
            content="This is a test article"
        )

    def test_article_creation(self):
        article = Article.objects.get(title="Test Article")
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.content, "This is a test article")
        self.assertEqual(article.user, self.user)
        self.assertEqual(article.category, self.category)
