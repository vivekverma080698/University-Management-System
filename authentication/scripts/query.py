import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EMSystem.settings')
django.setup()

from authentication.models import AuthTable, Department, Employee, Faculty, Director, Hod, Registrar, Ccfs, Staff, Post, AssistRegistrar

def receive(request):
    print(request.POST['a'])

receive()