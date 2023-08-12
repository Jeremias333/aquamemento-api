from django.http import HttpResponse, JsonResponse
from api.models import Info, Person
from django.utils import timezone

def person_put_validators(data):
    if data.get('now_drink') == None:
        return JsonResponse({"message": "now_drink field is required"})

    if data.get('person_id') == None:
        return JsonResponse({"message": "person_id field is required"})

    if not isinstance(data.get('now_drink'), int):
        return JsonResponse({"message": "now_drink field must be int"})

    if not isinstance(data.get('person_id'), int):
        return JsonResponse({"message": "person_id field must be int"})
    
    if data.get('now_drink') <= 0:
        return JsonResponse({"message": "now_drink field must be positive"})

    if data.get('person_id') <= 0:
        return JsonResponse({"message": "person_id field must be positive"})

    infos = Info.objects.filter(id=data.get('now_drink'))
    if infos.count() == 0:
        return JsonResponse({"message": "Info passed into now_drink field not found"})

    person = Person.objects.filter(id=data.get('person_id'))
    if person.count() == 0:
        return JsonResponse({"message": "Person passed into person_id field not found"})

    return True

def info_create_validators(data):
    if data.get('person_id') == None:
        return JsonResponse({"message": "person_id field is required"})

    if data.get('daily_goal') == None:
        return JsonResponse({"message": "daily_goal field is required"})

    if not isinstance(data.get('person_id'), int):
        return JsonResponse({"message": "person_id field must be int"})
    
    if not isinstance(data.get('daily_goal'), float):
        return JsonResponse({"message": "daily_goal field must be float"})
    
    if data.get('person_id') <= 0:
        return JsonResponse({"message": "person_id field must be positive"})

    if data.get('daily_goal') <= 0:
        return JsonResponse({"message": "daily_goal field must be positive"})

    person = Person.objects.filter(id=data.get('person_id'))
    if person.count() == 0:
        return JsonResponse({"message": "Person passed into person_id field not found"})
    
    today = timezone.now().date()
    existing_info = Info.objects.filter(person=data.get('person_id'), created_at__date=today).first()
    if existing_info:
        return JsonResponse({"message": "An Info object already exists for today."})

    return True

def info_list_by_person_validators(data):
    if data.get('person_id') == None:
        return JsonResponse({"message": "person_id field is required"})

    if not isinstance(data.get('person_id'), int):
        return JsonResponse({"message": "person_id field must be int"})
    
    if data.get('person_id') <= 0:
        return JsonResponse({"message": "person_id field must be positive"})

    person = Person.objects.filter(id=data.get('person_id'))
    if person.count() == 0:
        return JsonResponse({"message": "Person passed into person_id field not found"})

    return True