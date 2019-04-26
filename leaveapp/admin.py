from django.contrib import admin
from leaveapp.models import Leave
from leaveapp.models import LeaveRoute

# Register your models here.

admin.site.register(Leave)
admin.site.register(LeaveRoute)