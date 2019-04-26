from django.contrib import admin
from authentication.models import AuthTable
from authentication.models import Department
from authentication.models import Ccfs
from authentication.models import Employee
from authentication.models import Director
from authentication.models import Hod
from authentication.models import Faculty
from authentication.models import Staff
from authentication.models import Registrar
from authentication.models import AssistRegistrar
from authentication.models import Post
from papertrail.models import PaperTrail

admin.site.register(AuthTable)
admin.site.register(Director)
admin.site.register(Department)
admin.site.register(Ccfs)
admin.site.register(Employee)
admin.site.register(Hod)
admin.site.register(Faculty)
admin.site.register(Staff)
admin.site.register(AssistRegistrar)
admin.site.register(Post)
admin.site.register(PaperTrail)
admin.site.register(Registrar)
