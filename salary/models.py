from django.db import models
from authentication.models import Staff, Employee, AssistRegistrar, Ccfs


# Create your models here.

class Cfti(models.Model):
    cftiID = models.AutoField(primary_key=True,db_column='cfti_id')
    experience = models.IntegerField(db_column='experience')
    grade = models.CharField(max_length=20, db_column='grade')
    baseSalary = models.DecimalField(max_digits=30, decimal_places=2, db_column='salary')
    lastUpdated = models.DateTimeField(db_column='last_updated')

    class Meta:
        db_table = 'cfti'
        # unique_together = ['experience','grade']


    # def __str__(self):
    #     return str(self.experience) + ' ' + str(self.grade)


class Calender(models.Model):
    month = models.IntegerField(db_column='date')
    year = models.IntegerField(db_column='year')
    bonus = models.DecimalField(max_digits=20, decimal_places=2, db_column='bonus')

    class Meta:
        db_table = 'calender'

    # def __str__(self):
    #     return str(self.month) + ' ' + str(self.year)

# doubt regarding id


class Payslip(models.Model):
    ID = models.AutoField(primary_key=True,db_column='ID')
    # Email + Month + Year
    payslip_id = models.CharField(max_length=50, db_column='payslip_id')
    # Slip generated staff name
    slip_gen = models.ForeignKey(Ccfs, on_delete=models.PROTECT, db_column='slip_gen', null=True)
    slip_gen_ar=models.ForeignKey(AssistRegistrar, on_delete=models.PROTECT, db_column='slip_gen_ar', null=True)
    payslip_ownerName = models.CharField(max_length=50,null=True)
    slip_emp = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='slip_emp', null=True)
    month = models.IntegerField(null=True, db_column='month')
    year = models.IntegerField(null=True, db_column='year')
    experience = models.IntegerField(null=True, db_column='experience')
    grade_of_employment = models.CharField(max_length=20, default='A', null=False, db_column='grade_of_employment')
    base_salary = models.DecimalField(max_digits=30, decimal_places=2, db_column='salary', null=True)
    bonus_received = models.DecimalField(max_digits=30, decimal_places=2, null=True, db_column='bonus')
    total_salary = models.DecimalField(max_digits=30, decimal_places=2, null=True, db_column='total_salary')
    date_of_generation = models.DateField(null=True, db_column='date_of_generation')
    approvedByAccountSection = models.BooleanField(default=None, null=True, db_column='approvedByAccountSection')
    approvedByAssistRegistrar = models.BooleanField(default=None, null=True, db_column='approvedByAssistRegistrar')
    class Meta:
        db_table = 'payslip'
        # unique_together = (("slip_gen", "slip_staff"),)

    # def __str__(self):
    #     return self.payslip_id



# Papertrail for paySlip
class paperTrailPayslip(models.Model):
    paperTrailID = models.AutoField(primary_key=True,db_column='paperTrailID')
    payslip_id = models.IntegerField(db_column='payslip_id')
    date = models.DateField(null=False, db_column='date')
    comment = models.TextField(null=True, db_column='comment')
    role = models.CharField(max_length=20, null=False, db_column='role')
    # employee id of generator
    empIDGen = models.IntegerField(db_column='empIDGen', null=False)
    status = models.CharField(max_length=20, db_column='status', null=False)

    class Meta:
        db_table='paperTrailPayslip'



