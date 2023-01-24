from rest_framework import serializers

from restaurant.models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]