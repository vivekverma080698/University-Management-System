from django.contrib import admin
from salary.models import Calender, paperTrailPayslip
from salary.models import Payslip
from salary.models import Cfti


admin.site.register(Calender)
admin.site.register(Payslip)
admin.site.register(Cfti)
admin.site.register(paperTrailPayslip)
