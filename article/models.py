from django.db import models
from support.models import BaseModel, CompressedImageField
from authentications.models import User



class ArticleCategory(BaseModel):
    name = models.CharField(max_length=255)
    icon = CompressedImageField(quality=75, width=1920)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Article(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = CompressedImageField(quality=75, width=1920)
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption

    def __str__(self):
        return f"Image for {self.article.title}"