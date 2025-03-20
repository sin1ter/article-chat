from rest_framework import serializers
from .models import ArticleCategory, ArticleImage, Article

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['icon'] = instance.icon.url
        return data

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ('id', 'image', 'caption')

class ArticleSerializer(serializers.ModelSerializer):
    images = ArticleImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=ArticleCategory.objects.all()
    )
    user = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'category', 'title', 'images', 'uploaded_images', 'content', 'user']
        read_only_fields = ('user',)

    def get_user(self, obj):
        if obj.user:
            user_data = {
                "id": obj.user.id,
                "username": obj.user.username,
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name,
                "email": obj.user.email
            }
            return user_data
        return None


    def validate_user(self, value):
        if not value.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        return value

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        article = Article.objects.create(**validated_data)

        for image in uploaded_images:
            ArticleImage.objects.create(article=article, image=image)

        return article

