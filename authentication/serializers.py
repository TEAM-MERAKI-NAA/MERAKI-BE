
from authentication.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['user_id'] = user.pk
        token['email'] = user.email
        token['user_type'] = user.user_type
        token['displayName'] = user.username
        token['is_active'] = user.is_active

        return token

    def validate(self, attrs):
        print('validate')
        print(attrs)
        username = attrs['username']
        try:
            user = User.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
            password = attrs['password']
            pwd_valid = user.check_password(password)
            if pwd_valid:
                userdata = self.checkActiveUser(user)
                return userdata
            raise serializers.ValidationError("Invaid Username or Password")
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesnot exists")

    def checkActiveUser(self, user):
        userdata = {}
        if user.is_active:
            refresh = self.get_token(user)
            userdata = {
                'refresh':  str(refresh),
                'token': str(refresh.access_token),
                'user': {
                    'id': user.pk,
                    'displayName': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'is_active': user.is_active,
                    'name': user.username
                }
            }
        else:
            raise serializers.ValidationError(
                "User is not Active yet. Please activate your account")
        return userdata

class UserManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'is_superuser', 'first_name', 'last_name', 'password', 'user_type', 'phone_number',
                  'is_active')
        read_only_fields = ('id',)


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['displayName'] = ret['username']
        return ret

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_type', 'phone_number')
        read_only_fields = ('id',)


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['displayName'] = ret['username']
        return ret

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                 'first_name', 'last_name', 'user_type', 'phone_number')