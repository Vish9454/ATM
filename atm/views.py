""" rest framework import """
from rest_framework import status as status_code
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

''' project level import '''
from core.response import SuccessResponse
from core.exception import get_custom_error
from core.messages import success_message, validation_message
from core.pagination import CustomPagination


from atm.serializers import UserSignUpSerializer, LoginSerializer, ATMDeatilOperationsSerializer
from atm.models import User, ATMDetails


class UserSignUp(viewsets.ViewSet):
    """
    UserSignUpViewSet
        This class combines the logic of Craete operations for users.
        Inherits: BaseUserViewSet
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer

    def create(self, request):
        """
                post method used for the signup.
            :param request:
            :return: response
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(serializer.data, status=status_code.HTTP_200_OK)


class Login(viewsets.ViewSet):
    """
    user login viewset
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialize_data = serializer.data
        serialize_data.pop('password')
        return SuccessResponse(serialize_data, status=status_code.HTTP_200_OK)


class ATMDetailOperations(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    action_serializers = {
        'create': ATMDeatilOperationsSerializer,
        'retrieve': ATMDeatilOperationsSerializer,
        'list': ATMDeatilOperationsSerializer,
        'update': ATMDeatilOperationsSerializer,
    }

    def create(self, request):
        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return Response(get_custom_error(status=400, message=validation_message.get("USER_NOT_FOUND"),
                                             error_location=validation_message.get("LOCATION")),
                            status=status_code.HTTP_400_BAD_REQUEST)
        serializer = self.action_serializers.get(self.action)(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialize_data = serializer.data
        return SuccessResponse(serialize_data, status=status_code.HTTP_200_OK)

    def retrieve(self, request, atm_id):
        obj = ATMDetails.objects.filter(id=atm_id).first()
        if obj:
            serializer = self.action_serializers.get(self.action)(obj)
            return SuccessResponse(serializer.data, status=status_code.HTTP_200_OK)
        return SuccessResponse({}, status=status_code.HTTP_200_OK)

    def list(self, request):
        obj = ATMDetails.objects.filter().all().order_by('-id')
        if obj:
            serializer = self.action_serializers.get(self.action)(obj, many=True)
            return SuccessResponse(serializer.data, status=status_code.HTTP_200_OK)
        return SuccessResponse({}, status=status_code.HTTP_200_OK)

    def update(self, request, atm_id):
        atm_id = ATMDetails.objects.filter(id=atm_id, is_deleted=False).first()
        if not atm_id:
            return Response(get_custom_error(status=400, message=validation_message.get("INVALID_ID"),
                                             error_location=validation_message.get("LOCATION")),
                            status=status_code.HTTP_400_BAD_REQUEST)
        serializer = self.action_serializers.get(self.action)(data=request.data, instance=atm_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse({"message": success_message.get("UPDATE_SUCCESSFUL")}, status=status_code.HTTP_200_OK)