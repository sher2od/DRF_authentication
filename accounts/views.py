# TODO
from django.contrib.auth import authenticate



from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# TODO
from rest_framework.authtoken.models import Token

from .serilizers import RegisterSerialzer, UserSerializer,LoginSeralizer

from rest_framework.authentication import TokenAuthentication

class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = RegisterSerialzer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            user_json = UserSerializer(user).data

            return Response(user_json,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self,request:Request) -> Response:
        serializer = LoginSeralizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = authenticate(username=data['username'], password = data['password'])

        if user is not None:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self,request: Request) -> Response:
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request: Request) -> Response:
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)