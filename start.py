import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aquamemento.settings')
django.setup()

from api.models import Container

containers_list = [
    {'capacity': 250.0, 'title': 'Copo pequeno'},
    {'capacity': 350.0, 'title': 'Copo médio'},
    {'capacity': 500.0, 'title': 'Garrafa média'},
]

def create_default_containers():
    for item in containers_list:
        container = Container(**item)
        container.save()
        print("Container created: ", container.title)

if __name__ == '__main__':
    print("Creating default containers...")
    create_default_containers()
    print("Done!")