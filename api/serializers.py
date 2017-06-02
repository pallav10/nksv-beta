from rest_framework import serializers
from models import User, Category, Blog, ProductImage, Service


# used for registration, it hold the value of user table with all fields.


class UserSerializer(serializers.ModelSerializer):
    # token = serializers.Field(source='my_token')

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'country_code', 'contact_no',
                  'created', 'modified', 'city', 'state', 'country')


# serialize data of user for common need of user table.
class UserProfileSerializer(serializers.ModelSerializer):
    contact_no = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'first_name', 'last_name', 'created', 'country_code', 'contact_no', 'city',
            'state', 'country', 'is_password_changed')


# serialize data of categories for common need of category table.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'category_name', 'category_slug')


# serialize data of categories for common need of category table.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'product_name', 'category', 'product_price', 'product_description', 'is_available')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_category', 'service_description')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'image'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'blog_name', 'blog_description', 'blog_image')
