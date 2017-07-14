from rest_framework import serializers
from models import *

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


class UserResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResetPassword
        fields = ('id', 'user', 'key', 'key_expires')


# # serialize data of product_categories for common need of product_categories table.
# class ProductCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ('id', 'name', 'description', 'image', 'is_available')
#
#
# # serialize data of categories for common need of category table.
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'product_category', 'name', 'price', 'description', 'image', 'is_available')
#
#
# # serialize data of product_categories for common need of product_categories table.
# class ServiceCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceCategory
#         fields = ('id', 'name', 'description', 'image', 'is_available')
#
#
# # serialize data of categories for common need of category table.
# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = ('id', 'service_category', 'name', 'price', 'description', 'image', 'is_available')


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'item_type_id', 'name', 'description', 'image', 'is_available')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'category', 'name', 'description', 'image', 'price', 'is_available')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'item', 'quantity', 'price')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'name', 'description', 'image')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ('id', 'name', 'description', 'image')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGallery
        fields = ('id', 'name', 'description', 'video')


class HoroscopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horoscope
        fields = ('id', 'category', 'name', 'description', 'created')
