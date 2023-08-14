from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Info, Container, Person

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class InfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Info
        fields = ['id', 'created_at', 'person', 'daily_goal', 'drank', 'reached_goal']
    
class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ['title', 'capacity']

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'kg', 'now_drink']

    def create(self, validated_data):
        name = validated_data.get('name')
        existing_person = Person.objects.filter(name=name).first()
        
        if existing_person:
            return existing_person
        
        return super().create(validated_data)
