from django.shortcuts import render
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
from api import validators
from rest_framework.views import APIView


def index(request):
    return JsonResponse({"message": "It works!"})


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

    def create(self, request, *args, **kwargs):
        data = request.data

        result = validators.info_create_validators(data)
        if result != True:
            return result

        person = Person.objects.filter(id=data.get('person_id')).first()
        new_info = Info.objects.create(
            person=person, daily_goal=data.get('daily_goal'))

        person.now_drink = new_info.id
        person.save()
        return JsonResponse({"message": "Created new info with id: {}" .format(new_info.id)})


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by('title')
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        data = request.data

        result = validators.person_put_validators(data)
        if result != True:
            return result  # will be JsonResponse

        person = data.get('person_id')
        Person.objects.filter(id=person).update(
            now_drink=data.get('now_drink'))

        return JsonResponse({"message": "Updated completed to person id: {}" .format(person)})


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


class ListHistoryByPersonByDateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = request.data

        result = validators.info_list_by_date_validators(data)
        if type(result) == type(JsonResponse):
            return result
        else:
            date = result

        person_id = data.get('person_id')

        infos = Info.objects.filter(
            person=person_id, created_at__date=date).order_by('-created_at')
        serializer = InfoSerializer(
            infos, many=True, context={"request": request})
        return JsonResponse({"infos": serializer.data})


class ListHistoryByPersonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = request.data

        result = validators.info_list_by_person_validators(data)
        if result != True:
            return result

        person_id = data.get('person_id')
        infos = Info.objects.filter(person=person_id).order_by('-created_at')
        serializer = InfoSerializer(
            infos, many=True, context={"request": request})
        return JsonResponse({"infos": serializer.data})


class CalcDailyGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        result = validators.calc_daily_goal_validators(data)
        if result != True:
            return result

        kg = data.get('kg')

        daily_goal = kg*35

        return JsonResponse({"daily_goal": float(daily_goal)})


class CalcRemainingGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        result = validators.calc_remaining_daily_goal_validators(data)
        if result != True:
            return result

        remaining_goal = float(data.get('daily_goal') - data.get('drank'))

        return JsonResponse({"remaining_goal": remaining_goal})


class CalcRemainingPercentGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        result = validators.calc_remaining_percent_goal_validators(data)
        if result != True:
            return result

        remaining_percent = float(
            (data.get('drank') / data.get('daily_goal')) * 100)

        return JsonResponse({"remaining_percent": remaining_percent})


class ConsumeDrinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        data = request.data

        result = validators.consume_drink_validators(data)
        if result != True:
            return result

        person_id = data.get('person_id')
        person = Person.objects.filter(id=person_id).first()
        info = Info.objects.filter(id=person.now_drink).first()

        info.drank = info.drank + data.get('drink')
        info.save()

        return JsonResponse({"message": "Person {} consumed {}ml" .format(person_id, data.get('drink'))})
