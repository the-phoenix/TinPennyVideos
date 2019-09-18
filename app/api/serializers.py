from rest_auth.serializers import \
    LoginSerializer as BaseLoginSerializer


class LoginSerializer(BaseLoginSerializer):
    username = None
