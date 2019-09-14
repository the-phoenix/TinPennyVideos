from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User
from .serializers import TokenSerializer, UserSerializer

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will override the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        # this checks is_active flag
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # login saves the user's ID in the session.
            # using Django's session framework
            login(request, user)

            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            # serializer.is_valid(raise_exception=True)
            serializer.is_valid()
            # serializer.save()

            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        full_name = request.data.get("full_name", "").strip()
        birthday = request.data.get("birthday", None)

        if not email or not password:
            return Response(
                data={
                    "message": "email and password are required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # validate password
        try:
            validate_password(password)
        except ValidationError as error:
            return Response(
                data={
                    "message": ' '.join(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                data={
                    "message": "User with given email already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = User.objects.create_user(
            email=email, password=password, birthday=birthday
        )

        if full_name != "":
            names = full_name.split(' ')
            new_user.first_name = names[0]
            new_user.last_name = ' '.join(names[1:]).strip()
            new_user.save()

        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )