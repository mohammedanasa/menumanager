from rest_framework import serializers
from django.contrib.auth import get_user_model


from restaurant.models import Category

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Category
        fields = ["cid", "name", "description", "created_at"]

class CurrentUserCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(
        many=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "email","category"]