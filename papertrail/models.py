from django.db import models
from leaveapp.models import Leave
from authentication.models import Employee
# Create your models here.

class PaperTrail(models.Model):
    trail_id = models.IntegerField(primary_key=True)
    leave_id = models.ForeignKey(Leave, on_delete=models.PROTECT, db_column='leave_id')
    emp_id = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='emp_id')
    status = models.CharField(max_length=20, db_column='status')
    comment = models.TextField(max_length=300, null=True, db_column='comment')
    date = models.DateField(null=False, db_column='date')

    class Meta:
        db_table = 'paperTrail'

    # def __str__(self):
    #     return self.trail_id
