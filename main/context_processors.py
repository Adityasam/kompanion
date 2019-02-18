from main.models import Center
from django.contrib.auth.models import User

def center_name_processor(request):
    c_name = Center.objects.all()            
    return {'centers_name': c_name}