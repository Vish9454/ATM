from rest_framework import serializers
from core.messages import validation_message
from rest_framework.authtoken.models import Token
from core import utils as core_utils
from django.contrib.auth import authenticate
from django.contrib.gis.geos import Point

from atm.models import User, ATMDetails

class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Users signup serializer
    """
    email = serializers.EmailField(min_length=5, max_length=50, required=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    @staticmethod
    def validate_email(email):
        """
            method used to check email already exits in users table or not.
        :param email:
        :return:
        """
        if User.all_objects.filter(email=email.lower()).exists():
            raise serializers.ValidationError(validation_message.get("EMAIL_ALREADY_EXIST"))
        return email.lower()

    def create(self, validated_data):
        """
                    method used to create the data.
                :param validated_data:
                :return:
                """
        # create user object
        user_password = validated_data.pop('password')
        user_obj = User.objects.create(**validated_data)
        user_obj.set_password(user_password)
        user_obj.save()
        token, created = Token.objects.get_or_create(user=user_obj)
        self.validated_data['token'] = token.key
        return validated_data

    class Meta:
        model = User
        fields = ('id', 'full_name', 'first_name', 'last_name', 'email', 'password')


class LoginSerializer(serializers.ModelSerializer):
    """
    login of user serializer
    """
    email = serializers.EmailField(min_length=5, max_length=50, required=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"].lower(), password=attrs["password"])
        if user is not None:
            attrs["user"] = user
        else:
            raise serializers.ValidationError(validation_message.get('INVALID_CREDENTIAL'))
        return attrs

    def create(self, validated_data):
        user_obj = User.objects.filter(email=validated_data.get('email')).first()
        return user_obj

    def to_representation(self, instance):
        data = super(LoginSerializer, self).to_representation(instance)
        data['token'] = core_utils.get_or_create_user_token(instance)
        return data

    class Meta:
        model = User
        fields = ('id', "email", "password", 'full_name', 'first_name', 'last_name')


class ATMDeatilOperationsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        lat = float(request.data.get('lat'))
        lng = float(request.data.get('lng'))
        point = Point(x=lng, y=lat, srid=4326)
        validated_data.update({"geolocation": point})
        slot_obj = ATMDetails.objects.create(**validated_data)
        return slot_obj

    def update(self, instance, valiadated_data):
        ATMDetails.objects.filter(id=instance.id).update(**valiadated_data)
        return valiadated_data

    class Meta:
        model = ATMDetails
        fields = ('__all__')
