from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer


from restaurant.models import *

User = get_user_model()

"""class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Category
        fields = ["cid", "name", "description", "created_at"]"""

class CurrentUserCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(
        many=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "email","category"]


#New 



class ModifierSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Modifier
        fields = ('mid','owner', 'name', 'price', 'is_active')
        read_only_fields = ('mid', 'created_at', 'updated_at')

class ModifierGroupSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modifiers = ModifierSerializer(many=True)
    class Meta:
        model = ModifierGroup
        fields = ('mgid','owner', 'name', 'description', 'is_active', 'modifiers')
        read_only_fields = ('mgid', 'created_at', 'updated_at')

class ProductSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modifier_groups = ModifierGroupSerializer(many=True)

    class Meta:
        model = Product
        fields = ('pid', 'owner', 'name', 'price', 'description', 'is_active' ,'modifier_groups')
        read_only_fields = ('created_at', 'updated_at')
        depth= 1

class CategorySerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ('owner','cid','name','description','is_active','product')
        read_only_fields = ('cid', 'created_at', 'updated_at')
        depth = 3

class MenuSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(many=True)

    class Meta:
        model = Menu
        fields = ('menuid', 'owner', 'name', 'description', 'category')
        read_only_fields = ('created_at', 'updated_at')
        depth = 2

    

class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menu = MenuSerializer(many=True)
    
    class Meta:
        model = Restaurant
        fields = ('owner','lid','name','menu')
        read_only_fields = ('lid', 'created_at', 'updated_at')
