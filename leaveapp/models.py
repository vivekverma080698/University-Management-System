from django.db import models
from authentication.models import Employee
# Create your models here.


class Leave(models.Model):
    emp_ID = models.EmailField(max_length=100, db_column='email_id')
    leave_ID = models.CharField(max_length=50, primary_key=True, db_column='leave_id')
    status = models.CharField(max_length=50, db_column='status')
    date = models.DateField(null=False)
    concern_auth = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='concern_auth',null=True)
    text = models.TextField(max_length=300)

    class Meta:
        db_table = 'leave'

    # def __str__(self):
    #     return self.leave_ID


class LeaveRoute(models.Model):
    Role = models.CharField(max_length=50, null=False, db_column='role')
    From = models.CharField(max_length=50, null=False, db_column='from')
    to = models.CharField(max_length=50, null=False, db_column='to')

    class Meta:
        db_table = 'leaveroute'

    # def __str__(self):
    #     return self.From + ' ' + self.to