import base64
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from django.http.request import QueryDict
import json


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains'],
            'name': ['icontains'],
            'email': ['icontains'],
            'mobile': ['icontains'],
            'role': ['exact'],
            'role__id': ['exact'],
            'role__role': ['exact', 'icontains'],
            'status': ['exact'],
        }

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser)
    filterset_class = UserFilter
    filter_backends = [rest_framework_filters.SearchFilter,
                       filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def update(self, request, pk=None):
        instance = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            if 'picture' in request.data:
                instance.picture = request.FILES['picture'] 
            elif request.data['profile_picture_removed'] == 'true':
                instance.picture.delete(save=True)
            else:
                pass
            instance = serializer.save()
            instance.save()
            return Response(serializer.data)
        else:
            print("Not Valid", serializer.errors)
        return Response({'errors': serializer.errors}, status=401)
    

    @action(detail=False, methods=['PUT'])
    def updateuserstatus(self, request):
        user_id = request.query_params.get('user', None)
        status = request.query_params.get('status', None)
        modified_by = request.query_params.get('modified_by', None)

        instance = User.objects.get(pk=user_id)
        modified_by_instance = User.objects.get(pk=modified_by)

        data = {
            "status": status,
            "modified_by": modified_by_instance
        }

        serializer = UserSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            instance.status = data['status']
            instance.modified_by = data['modified_by']
            instance.save()
            return Response(serializer.data)
        else:
            print("Not Valid", serializer.errors)
        return Response({'errors': serializer.errors}, status=401)


    @action(detail=False, methods=['PUT'])
    def updateuserrole(self, request):
        user_id = request.query_params.get('user', None)
        role_id = request.query_params.get('role', None)
        modified_by = request.query_params.get('modified_by', None)

        instance = User.objects.get(pk=user_id)
        modified_by_instance = User.objects.get(pk=modified_by)
        role_instance = Role.objects.get(pk=role_id)

        data = {
            "modified_by": modified_by_instance
        }

        serializer = UserSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            instance.role = role_instance
            instance.modified_by = data['modified_by']
            instance.save()
            return Response(serializer.data)
        else:
            print("Not Valid", serializer.errors)
        return Response({'errors': serializer.errors}, status=401)
    

    @action(detail=False, methods=['POST'])
    def register(self, request):
        username = request.data['username'] if 'username' in request.data else None
        firstname = request.data['firstname'] if 'firstname' in request.data else None
        middlename = request.data['middlename'] if 'middlename' in request.data else None
        lastname = request.data['lastname'] if 'lastname' in request.data else None
        mobile = request.data['mobile'] if 'mobile' in request.data else None
        email = request.data['email'] if 'email' in request.data else None
        password = request.data['password'] if 'password' in request.data else None
        role = request.data['role'] if 'role' in request.data else None
        role_instance = Role.objects.filter(role=role).first()

        probable_user = User.objects.filter(Q(username=username)|Q(mobile=mobile)|Q(email=email)).exists()
        if not probable_user:
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.first_name = firstname
            user.middle_name = middlename
            user.last_name = lastname
            user.email = email
            user.mobile = mobile
            user.role = role_instance
            user.status = 'INACTIVE'
            user.save()
            return Response({'message': "User registered successfully"}, status=201)
        else:
            return Response({'error message': "Username, mobile number or email is already registered"}, status=401)


class RoleFilter(filters.FilterSet):

    class Meta:
        model = Role
        fields = {
            'role': ['icontains'],
            'user_type': ['icontains'],
            'status': ['exact'],
        }


class RoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Role.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [TokenAuthentication]
    filterset_class = RoleFilter
    filter_backends = [rest_framework_filters.SearchFilter,
                       filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def update(self, request, pk=None):
        instance = self.get_object()
        
        serializer = RoleSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            return Response(serializer.data)
        return Response({'errors': serializer.errors}, status=401)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        print(request.data)
        username = request.data['username']
        password = request.data['password']

        probable_user = User.objects.filter(Q(username=username)|Q(email=username)|Q(mobile=username)).exists()
        probable_user_details = User.objects.filter(Q(username=username)|Q(email=username)|Q(mobile=username)).first()
        
        if probable_user:
            user = authenticate(request, username=probable_user_details.username, password=password) 
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                serializer = UserSerializer(instance=user, context={"request": request})

                return Response(
                    {
                        "token": token.key,
                        "user": serializer.data,
                    },
                    status=200,
                )
            else:
                return Response({"msg": "Credentials are wrong"}, status=402)
        error_code = 404
        if error_code == 404:
            return Response({"msg": "User does not exist with this username"}, status=402)
        elif error_code == 400:
            return Response({"msg": "User must provide email and password"}, status=402)
        return Response({"msg": "Credentials are wrong"}, status=402)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        logout(request)
        return Response(status=204)
