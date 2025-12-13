# TODO
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password



from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# TODO
from rest_framework.authtoken.models import Token

from .serilizers import RegisterSerialzer, UserSerializer,LoginSeralizer,ProfileSerializer, PasswordChangeSerializer
from .permissions import IsAdmin,IsManager,IsStaff,IsUser


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
    
    def put(self, request: Response) -> Response:
        user = request.user

        serializer = ProfileSerializer(data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            updated_user = serializer.update(user,serializer.validated_data)

        serializer = UserSerializer(updated_user)
        
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    

class PasswordChangeView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request: Request) -> Response:
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = request.user

            if not check_password(serializer.validated_data['password'], user.password):
                return Response('password is in correct',status=400)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        


class AdminPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request) -> Response:

        return Response("Xush kelibsiz Admin")

class UserPanelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]

    def get(self, request: Request) -> Response:
        return Response("Xush keldiz User")
    

class ManagerPanleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManager]

    def get(self, request: Request) -> Response:
        return Response("Xush keldiz Manager")
