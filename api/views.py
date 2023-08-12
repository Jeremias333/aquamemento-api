from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from api.models import Info, Container, Person
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, InfoSerializer, ContainerSerializer, PersonSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



def index(request):
    return JsonResponse({"message": "Hello, world!"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all().order_by('-created_at')
    serializer_class = InfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by('title')
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
