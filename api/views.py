import re
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from rest_framework import schemas
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import messages
import utils
import validations_utils
from exceptions_utils import ValidationException
from forms import ResetPasswordForm
from models import UserResetPassword, Article, ImageGallery, \
    VideoGallery, Category, ItemType, Item, Cart, Horoscope
from permission import UserPermissions
from serializers import UserProfileSerializer, ArticleSerializer, ImageSerializer, VideoSerializer, CategorySerializer, \
    ItemCategorySerializer, ItemSerializer, CartSerializer, HoroscopeSerializer


# Create your views here.


@api_view()
@permission_classes((AllowAny,))
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Rest Swagger')
    return Response(generator.get_schema(request=request))


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_registration(request):
    """
    **Registers a new user- Ignore**

    * Accepts only POST requests
dd
    > POST

    * Requires following fields of users in JSON format:

        - Sign Up with Email

            1. `email` - Valid email address
            2. `password` - String


    * Possible HTTP status codes and JSON response:

        * `HTTP_201_CREATED` - When new user registration is done successfully:

                {
                      "first_name": null or string,
                      "last_name": null or string,
                      "created": date_timestamp,
                      "contact_no": integer,
                      "token": "token string",
                      "user_role": integer,
                      "email": string
                }

        * `HTTP_400_BAD_REQUEST` :

            - Email already used to register one user.
            Use a different email address

                {
                 "message": "User with this email already exists."
                }

        * `HTTP_400_BAD_REQUEST` - Invalid email address

                {
                    "message": "Enter a valid email address."
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

    * Status code can be used from HTTP header. A separate status field in json
    data is not provided.
    :param request:

    """
    if request.method == 'POST':
        try:
            with transaction.atomic():
                try:
                    data = validations_utils.email_validation(
                        request.data)  # Validates email id, it returns lower-cased email in data.
                    data = validations_utils.password_validation(data)  # Validates password criteria.
                    data['password'] = utils.hash_password(data['password'])  # password encryption
                    data = utils.create_user(data)  # Creates user with request data.
                    user = validations_utils.user_validation_with_email(data['email'])  # Validates if user exists or
                    #  not.

                    # if 'HTTP_HOST' not in request.META:
                    #     request.META['HTTP_HOST'] = '127.0.0.1:8000'
                    # hostname = request.META['HTTP_HOST']
                    # current_site = get_current_site(request)
                    # utils.send_welcome_mail(current_site, user.id, user.email)  # send welcome email.
                    return Response(data, status=status.HTTP_201_CREATED)
                except ValidationException as e:  # Generic exception
                    return Response(e.errors, status=e.status)

        except IntegrityError:
            return Response(messages.USER_REGISTRATION_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes((UserPermissions, IsAuthenticated))
def user_detail(request, pk):
    """
    **Get or change the user profile data- Ignore**

    > GET

    Returns the User Profile data.

    * Requires `user id` which is an integer and taken as primary key
    to identify user.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - Returns the User Profile data:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error



    > PUT

    ### Update User Profile Data

    * Requires data that needs to be changed. Any and all of the below fields
    could be modified in a single PUT request.

        1. `first_name`: String
        2. `last_name`: String
        3. `contact_no`: Integer
        4. `email` : String


    * Requires only the changed data of the user and `email` along the changed
    parameters.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - User profile data in JSON format:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR`

        :param pk:
        :param request:
    """
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        token_user_id = validations_utils.user_token_validation(
            request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'GET':
        user_profile_serializer = UserProfileSerializer(user)
        return Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            data = validations_utils.email_validation(data)  # Validates email id, it returns lower-cased email in data.
            updated_data = utils.update_user(data, user)  # Updates user data.
            return Response(updated_data, status=status.HTTP_200_OK)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_login(request):
    """
    **User Login**

    Login an existing user.

    Used for authenticating the user.

    > POST

    * Requires following fields of users in JSON format:

        1. `email` - String
        2. `password` - String

    * Returns user profile data on successful login.
    * Also returns Authentication token to be used by frontend for further
     communication with backend.
    * On failure it returns appropriate HTTP status and message in JSON
    response.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` on successful login.

        * `HTTP_401_UNAUTHORIZED` for failed login attempt.

                {
                 "message": "Invalid username or password"
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error.

        * `HTTP_404_NOT_FOUND` - When user is not found.

                {
                 "message": "User with specified email does not exist."
                }
    :param request:
    """
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response(
            messages.REQUIRED_EMAIL_AND_PASSWORD,
            status=status.HTTP_400_BAD_REQUEST)
    try:
        # response = validations_utils.login_user_existence_validation(email)
        user = authenticate(email=email, password=password)  # Validates credentials of user.
    except ValidationException:
        return Response(messages.INVALID_EMAIL_OR_PASSWORD, status=status.HTTP_401_UNAUTHORIZED)
    try:
        login_user = utils.authenticate_user(user, request.data)  # Authorizes the user and returns appropriate data.
        # token = utils.fetch_token(user)  # fetches the token for authorized user.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    return Response(login_user, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((UserPermissions, IsAuthenticated))
def user_change_password(request, pk):
    """
    ### Change Password

    * While changing password for user registered with email, PUT request
    requires two fields and their values:

        * current_password - String
        * new_password - String

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - If password change was successful:

                {
                 "user_id": integer,
                 "message": "Password updated successfully"
                }

        * `HTTP_401_UNAUTHORIZED` - If user provided incorrect value for
        current_password:

                {
                 "message": "Current password is incorrect."
                }

        * `HTTP_400_BAD_REQUEST` - If new_password is same as current_password:

                {
                 "message": "New password cannot be same as current password"
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
        :param pk:
        :param request:
    """
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'PUT':
        try:
            request.data['current_password']
        except KeyError:
            return Response(messages.REQUIRED_CURRENT_PASSWORD,
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            new_password = request.data['new_password']
            if new_password is None or not re.match(r'[A-Za-z0-9@#$%^&+=]+', new_password):
                return Response(messages.PASSWORD_NECESSITY, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                pass
        except KeyError:
            return Response(messages.REQUIRED_NEW_PASSWORD, status=status.HTTP_400_BAD_REQUEST)
        data_keys = request.data.keys()
        # Change Password will only require current_password and new_password.
        if 'current_password' in data_keys and 'new_password' in data_keys:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
            try:
                password = utils.change_password(current_password, new_password, user)  # Changes password.
                return Response(password, status=status.HTTP_200_OK)
            except ValidationException as e:
                return Response(e.errors, status=e.status)


@api_view(['POST'])
@permission_classes((AllowAny,))
def password_reset(request):
    """
    **Password Reset**

    * To reset user password.

    ### POST

    Send mail to the user on specified email address with the link to
    reset password.

    * Requires only the `email` address.

    * Possible HTTP status codes and JSON response:

        * `HTTP_404_NOT_FOUND` - If user with specified email is not found.

                {
                    'message': "User with specified email does not exist."
                }

        * `HTTP_200_OK` - When Password Reset Link is successfully sent.

                {
                    'message': "Password Reset Link sent."
                }
    :param request:
    """
    try:
        with transaction.atomic():
            try:
                data = request.data
                data = validations_utils.email_validation(data)  # Validates email id, it returns lower-cased email in data.
                user = validations_utils.user_validation_with_email(data['email'])
            except ValidationException as e:  # Generic exception
                return Response(e.errors, status=e.status)
            current_site = get_current_site(request)
            domain = current_site.domain
            key = utils.create_reset_password_key(user.email)
            utils.send_reset_password_mail(user, key, domain)  # Sends an email for resetting the password.
            return Response(messages.PASSWORD_RESET_LINK_SENT, status=status.HTTP_200_OK)
    except IntegrityError:
        return Response(messages.CAN_NOT_RESET_PASSWORD, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def password_reset_confirm(request, pk, key):
    try:
        user_reset_password = UserResetPassword.objects.get(user_id=pk)
        error_message = ''
    except UserResetPassword.DoesNotExist:
        return HttpResponse(messages.USER_DOES_NOT_EXISTS)

    if request.method == 'GET':
        if user_reset_password.key_expires < timezone.now():
            # return HttpResponse('Sorry! Link is expired :(')
            error_message = "Sorry! Link is expired :("
        else:
            if user_reset_password.key == key:
                user_reset_password.is_valid_key = True
                user_reset_password.save()
                url = '/api/users/%s/password_reset/done/' % pk
                return HttpResponseRedirect(url)
            else:
                # return HttpResponse('Link is not valid. :(')
                error_message = "Link is not valid. :("
    return render(request, 'reset_password.html', {'error_message': error_message})


def password_reset_done(request, pk):
    try:
        user_reset_password = UserResetPassword.objects.get(user_id=pk)
        response = ''
        success_message = ''
    except UserResetPassword.DoesNotExist:
        return HttpResponse("User does not exist.")

    if request.method == 'POST':
        reset_password_form = ResetPasswordForm(data=request.POST)
        if reset_password_form.is_valid():
            password = request.POST['new_password']
            success_message = utils.reset_password(user_reset_password, password)
        else:
            # ResetPasswordForm.errors
            response = messages.PASSWORD_MISMATCH
    else:
        reset_password_form = ResetPasswordForm()

    return render(
        request, 'reset_password.html',
        {'form': reset_password_form,
         'response': response,
         'success_message': success_message}
    )

#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def product_categories(request):
#     """
#         **Get all the product_categories data- Ignore**
#
#         > GET
#
#         Returns the product_categories data.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the products data:
#
#                     {
#                       "id": Integer,
#                       "name": String,
#                       "description": String,
#                       "image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param request:
#         """
#     all_product_categories = ProductCategory.objects.all()  # Get all product_categories
#     if request.method == 'GET':
#         if all_product_categories:
#             product_category_serializer = ProductCategorySerializer(all_product_categories, many=True)
#             return Response(product_category_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(messages.EMPTY_PRODUCT_CATEGORIES, status=status.HTTP_204_NO_CONTENT)

#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def products(request, pk):
#     """
#
#         **Get the product data- Ignore**
#
#         > GET
#
#         Returns the Product data.
#
#         * Requires `product id` which is an integer and taken as primary key
#         to identify product.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the product data:
#
#                     {
#                       "id": Integer,
#                       "product_name": String,
#                       "product_category": String,
#                       "product_price": String,
#                       "product_description": String,
#                       "product_image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param pk:
#             :param request:
#         """
#     if Product.objects.filter(product_category_id=pk).exists():  # Checks if product_category exists with given id.
#         all_products = Product.objects.filter(product_category_id=pk)
#     else:
#         return Response(messages.CATEGORY_PRODUCTS_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         product_serializer = ProductSerializer(all_products, many=True)
#         return Response(product_serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def product_detail(request, pk):
#     """
#
#         **Get the product data- Ignore**
#
#         > GET
#
#         Returns the Product data.
#
#         * Requires `product id` which is an integer and taken as primary key
#         to identify product.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the product data:
#
#                     {
#                       "id": Integer,
#                       "product_name": String,
#                       "product_category": String,
#                       "product_price": String,
#                       "product_description": String,
#                       "product_image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param pk:
#             :param request:
#         """
#     try:
#         product = validations_utils.product_validation(pk)  # Validates if product exists or not.
#     except ValidationException as e:  # Generic exception
#         return Response(e.errors, status=e.status)
#     if request.method == 'GET':
#         product_serializer = ProductSerializer(product)
#         return Response(product_serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def service_categories(request):
#     """
#         **Get all the product_categories data- Ignore**
#
#         > GET
#
#         Returns the product_categories data.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the products data:
#
#                     {
#                       "id": Integer,
#                       "name": String,
#                       "description": String,
#                       "image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param request:
#         """
#     all_service_categories = ServiceCategory.objects.all()  # Get all service_categories
#     if request.method == 'GET':
#         if all_service_categories:
#             service_category_serializer = ServiceCategorySerializer(all_service_categories, many=True)
#             return Response(service_category_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(messages.EMPTY_PRODUCT_CATEGORIES, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def services(request, pk):
#     """
#
#         **Get the product data- Ignore**
#
#         > GET
#
#         Returns the Product data.
#
#         * Requires `product id` which is an integer and taken as primary key
#         to identify product.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the product data:
#
#                     {
#                       "id": Integer,
#                       "product_name": String,
#                       "product_category": String,
#                       "product_price": String,
#                       "product_description": String,
#                       "product_image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param pk:
#             :param request:
#         """
#     if Service.objects.filter(service_category_id=pk).exists():  # Checks if service_category exists with given id.
#         all_services = Service.objects.filter(service_category_id=pk)
#     else:
#         return Response(messages.CATEGORY_SERVICES_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         service_serializer = ServiceSerializer(all_services, many=True)
#         return Response(service_serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def service_detail(request, pk):
#     """
#
#         **Get the product data- Ignore**
#
#         > GET
#
#         Returns the Product data.
#
#         * Requires `product id` which is an integer and taken as primary key
#         to identify product.
#
#         * Possible HTTP status codes and JSON response:
#
#             * `HTTP_200_OK` - Returns the product data:
#
#                     {
#                       "id": Integer,
#                       "product_name": String,
#                       "product_category": String,
#                       "product_price": String,
#                       "product_description": String,
#                       "product_image": Url,
#                       "is_available": Boolean
#                     }
#
#             * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error
#
#             :param pk:
#             :param request:
#         """
#     try:
#         service = validations_utils.service_validation(pk)  # Validates if user exists or not.
#     except ValidationException as e:  # Generic exception
#         return Response(e.errors, status=e.status)
#     if request.method == 'GET':
#         service_serializer = ServiceSerializer(service)
#         return Response(service_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def item_categories(request):
    """
            **Get all the product_categories data- Ignore**

            > GET

            Returns the product_categories data.

            * Possible HTTP status codes and JSON response:

                * `HTTP_200_OK` - Returns the products data:

                        {
                          "id": Integer,
                          "name": String,
                          "description": String,
                          "image": Url,
                          "is_available": Boolean
                        }

                * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

                :param request:
            """
    all_item_categories = ItemType.objects.all()  # Get all product_categories
    if request.method == 'GET':
        if all_item_categories:
            item_category_serializer = ItemCategorySerializer(all_item_categories, many=True)
            return Response(item_category_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_PRODUCT_CATEGORIES, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def categories(request, pk):
    """
        **Get all the product_categories data- Ignore**

        > GET

        Returns the product_categories data.

        * Possible HTTP status codes and JSON response:

            * `HTTP_200_OK` - Returns the products data:

                    {
                      "id": Integer,
                      "name": String,
                      "description": String,
                      "image": Url,
                      "is_available": Boolean
                    }

            * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

            :param pk:
            :param request:
        """
    if Category.objects.filter(item_type_id=pk).exists():  # Checks if product_category exists with given id.
        all_categories = Category.objects.filter(item_type_id=pk)
    else:
        return Response(messages.CATEGORY_ITEM_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        category_serializer = CategorySerializer(all_categories, many=True)

        return Response(category_serializer.data[::-1], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def items(request, pk):
    """
        **Get all the product_categories data- Ignore**

        > GET

        Returns the product_categories data.

        * Possible HTTP status codes and JSON response:

            * `HTTP_200_OK` - Returns the products data:

                    {
                      "id": Integer,
                      "name": String,
                      "description": String,
                      "image": Url,
                      "is_available": Boolean
                    }

            * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

            :param pk:
            :param request:
        """

    if Item.objects.filter(category_id=pk).exists():  # Checks if product_category exists with given id.
        all_items = Item.objects.filter(category_id=pk)
    else:
        return Response(messages.ITEMS_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        item_serializer = ItemSerializer(all_items, many=True)
        return Response(item_serializer.data[::-1], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def item_detail(request, pk):
    """
    **Get or change the user profile data- Ignore**

    > GET

    Returns the User Profile data.

    * Requires `user id` which is an integer and taken as primary key
    to identify user.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - Returns the User Profile data:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error



    > PUT

    ### Update User Profile Data

    * Requires data that needs to be changed. Any and all of the below fields
    could be modified in a single PUT request.

        1. `first_name`: String
        2. `last_name`: String
        3. `contact_no`: Integer
        4. `email` : String


    * Requires only the changed data of the user and `email` along the changed
    parameters.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - User profile data in JSON format:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR`

        :param pk:
        :param request:
    """

    data = request.data
    try:
        item = validations_utils.item_validation(pk)  # Validates if user exists or not.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'GET':
        item_serializer = ItemSerializer(item)
        return Response(item_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes((UserPermissions, IsAuthenticated))
def cart(request, pk, key):
    """
    **add a new item to cart- Ignore**

    * Accepts only POST requests
dd
    > POST

    * Requires following fields of users in JSON format:

        - Sign Up with Email

            1. `email` - Valid email address
            2. `password` - String


    * Possible HTTP status codes and JSON response:

        * `HTTP_201_CREATED` - When new user registration is done successfully:

                {
                      "first_name": null or string,
                      "last_name": null or string,
                      "created": date_timestamp,
                      "contact_no": integer,
                      "token": "token string",
                      "user_role": integer,
                      "email": string
                }

        * `HTTP_400_BAD_REQUEST` :

            - Email already used to register one user.
            Use a different email address

                {
                 "message": "User with this email already exists."
                }

        * `HTTP_400_BAD_REQUEST` - Invalid email address

                {
                    "message": "Enter a valid email address."
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

    * Status code can be used from HTTP header. A separate status field in json
    data is not provided.
    :param key:
    :param pk:
    :param request:

    """
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        token_user_id = validations_utils.user_token_validation(
            request.auth.user_id, pk)  # Validates user's Token authentication.
        item = validations_utils.item_validation(key)

    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                try:
                    data['user'] = user.id
                    data['item'] = item.id
                    data = utils.add_item_to_cart(data)  # Creates user with request data.
                    return Response(data, status=status.HTTP_201_CREATED)
                except ValidationException as e:  # Generic exception
                    return Response(e.errors, status=e.status)
        except IntegrityError:
            return Response(messages.ADD_ITEM_TO_CART_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        try:
            with transaction.atomic():
                try:
                    if Cart.objects.filter(
                            user_id=user.id,
                            item_id=item.id).exists():  # Checks if product_category exists with given id.

                        cart_item_obj = Cart.objects.filter(user_id=user.id, item_id=item.id)
                    else:
                        return Response(messages.EMPTY_CART, status=status.HTTP_404_NOT_FOUND)
                    if cart_item_obj:
                        cart_item = Cart.objects.get(pk=cart_item_obj.id)
                        cart_item.delete()
                        return Response(messages.CART_ITEM_SUCCESSFULLY_DELETED, status=status.HTTP_200_OK)
                except ValidationException as e:  # Generic exception
                    return Response(e.errors, status=e.status)
        except IntegrityError:
            return Response(messages.DELETE_ITEM_TO_CART_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            with transaction.atomic():
                try:
                    if Cart.objects.filter(
                            user_id=user.id,
                            item_id=item.id).exists():  # Checks if product_category exists with given id.

                        cart_item_obj = Cart.objects.filter(user_id=user.id, item_id=item.id)
                    else:
                        return Response(messages.EMPTY_CART, status=status.HTTP_404_NOT_FOUND)
                    try:
                        cart_item = validations_utils.cart_item_validation(cart_item_obj.id)
                    except ValidationException as e:  # Generic exception
                        return Response(e.errors, status=e.status)
                    updated_data = utils.update_cart_item(data, cart_item)  # Updates cart data.
                    return Response(updated_data, status=status.HTTP_200_OK)
                except ValidationException as e:  # Generic exception
                    return Response(e.errors, status=e.status)
        except IntegrityError:
            return Response(messages.UPDATE_ITEM_TO_CART_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((UserPermissions, IsAuthenticated))
def cart_detail(request, pk):
    """
            **Get all the product_categories data- Ignore**

            > GET

            Returns the product_categories data.

            * Possible HTTP status codes and JSON response:

                * `HTTP_200_OK` - Returns the products data:

                        {
                          "id": Integer,
                          "name": String,
                          "description": String,
                          "image": Url,
                          "is_available": Boolean
                        }

                * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

                :param pk:
                :param request:
            """
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        token_user_id = validations_utils.user_token_validation(
            request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)

    if request.method == 'GET':
        if Cart.objects.filter(user_id=user.id).exists():  # Checks if product_category exists with given id.
            cart_items = Cart.objects.filter(user_id=user.id)
        else:
            return Response(messages.EMPTY_CART, status=status.HTTP_404_NOT_FOUND)
        if cart_items:
            cart_serializer = CartSerializer(cart_items, many=True)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_CART, status=status.HTTP_204_NO_CONTENT)


# @api_view(['PUT'])
# @permission_classes((UserPermissions, IsAuthenticated))
# def update_cart_detail(request, pk):
#     data = request.data
#     try:
#         cart_item = validations_utils.cart_item_validation(pk)
#     except ValidationException as e:  # Generic exception
#         return Response(e.errors, status=e.status)
#     if request.method == 'PUT':
#         try:
#             with transaction.atomic():
#                 try:
#                     updated_data = utils.update_cart_item(data, cart_item)  # Updates cart data.
#                     return Response(updated_data, status=status.HTTP_200_OK)
#                 except ValidationException as e:  # Generic exception
#                     return Response(e.errors, status=e.status)
#         except IntegrityError:
#             return Response(messages.UPDATE_ITEM_TO_CART_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # elif request.method == 'DELETE':
    #     try:
    #         with transaction.atomic():
    #             try:
    #                 if cart_item:
    #                     cart_item = Cart.objects.get(pk=pk)
    #                     cart_item.delete()
    #                     return Response(messages.CART_ITEM_SUCCESSFULLY_DELETED, status=status.HTTP_200_OK)
    #             except ValidationException as e:  # Generic exception
    #                 return Response(e.errors, status=e.status)
    #     except IntegrityError:
    #         return Response(messages.DELETE_ITEM_TO_CART_FAILED, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((AllowAny,))
def articles(request):
    all_articles = Article.objects.all()  # Get all articles
    if request.method == 'GET':
        if all_articles:
            article_serializer = ArticleSerializer(all_articles, many=True)
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_ARTICLE, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def images(request):
    all_images = ImageGallery.objects.all()  # Get all images
    if request.method == 'GET':
        if all_images:
            image_serializer = ImageSerializer(all_images, many=True)
            return Response(image_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_IMAGES, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def videos(request):
    all_videos = VideoGallery.objects.all()  # Get all videos
    if request.method == 'GET':
        if all_videos:
            video_serializer = VideoSerializer(all_videos, many=True)
            return Response(video_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_VIDEOS, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def horoscope(request):
    all_horoscopes = Horoscope.objects.all()  # Get all videos
    if request.method == 'GET':
        if all_horoscopes:
            horoscope_serializer = HoroscopeSerializer(all_horoscopes, many=True)
            return Response(horoscope_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(messages.EMPTY_HOROSCOPE, status=status.HTTP_204_NO_CONTENT)
