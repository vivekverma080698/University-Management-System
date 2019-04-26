from django.db import models


class AuthTable(models.Model):
    emailID = models.EmailField(max_length=100, primary_key=True, db_column='email_id')
    password = models.CharField(max_length=256, null=False, db_column='password')
    role = models.CharField(max_length=50, null=False, db_column='role')

    class Meta:
        db_table = 'authtable'

    def __str__(self):
        return self.emailID


class Employee(models.Model):
    ID = models.AutoField(primary_key=True,db_column="ID")
    emp_ID = models.OneToOneField(AuthTable, on_delete=models.CASCADE, null=False, db_column='emp_id')
    first_name = models.CharField(max_length=30, null=False, db_column='first_name')
    last_name = models.CharField(max_length=30, null=False, db_column='last_name')
    date_of_birth = models.DateField(null=False, db_column='date_of_birth')
    gender = models.CharField(max_length=10, null=False, db_column='gender')
    address = models.TextField(null=False, db_column='address')
    PAN = models.CharField(max_length=50, null=True, db_column='pan')
    date_of_join = models.DateField(null=False, db_column='date_of_join')
    STAFF='STAFF'
    FACULTY='FACULTY'
    CCFS='CCFS'
    DIRECTOR='DIRECTOR'
    REGISTRAR='REGISTRAR'
    ASSIST_REGISTRAR='ASSIST_REGISTRAR'
    HOD='HOD'
    DFA='DFA'
    ADFA='ADFA'
    DEPTSEC='DEPSEC'

    CHOICES = (
        (STAFF , 'STAFF'),
        (FACULTY, 'FACULTY'),
        (CCFS, 'CCFS'),
        (DIRECTOR, 'DIRECTOR'),
        (REGISTRAR, 'REGISTRAR'),
        (ASSIST_REGISTRAR,'ASSIST_REGISTRAR'),
        (HOD , 'HOD'),
        (DFA, 'DEAN FACULTY AFFAIR'),
        (ADFA, 'ASSOCIATE DEAN FACULTY AFFAIR'),
        (DEPTSEC, 'DEPARTMENT SECRETARY'),
    )

    current_role = models.CharField(max_length=20, null=False,choices=CHOICES, db_column='current_role')
    leave_available = models.IntegerField(null=False, db_column='leave_available')
    borrow_available = models.IntegerField(null=False, db_column='borrow_available')
    grade_of_employment = models.CharField(max_length=20, default='A', null=False, db_column='grade_of_employment')
    past_experience = models.IntegerField(default=0, db_column='past_experience')
    contact = models.CharField(max_length=12,null=True,db_column='contact')

    class Meta:
        db_table = 'employee'

    # def __str__(self):
    #     return str(self.emp_ID) + ' ' + str(self.first_name) + ' ' + self.last_name


class Department(models.Model):
    dept_ID = models.IntegerField(primary_key=True, db_column='dept_id')
    dept_name = models.CharField(max_length=40, null=False, db_column='dept_name')

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.dept_name


class Faculty(models.Model):
    faculty_id = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, primary_key=True,
                                   db_column='faculty_id')
    dept_ID = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')

    class Meta:
        db_table = 'faculty'

    # def __str__(self):
    #     return self.faculty_id


class Director(models.Model):
    dirID = models.AutoField(primary_key=True, db_column='dir_id')
    dirEmail = models.EmailField(max_length=100, db_column='dir_email')
    faculty_ID = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column='faculty_id')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    class Meta:
        db_table = 'director'

    # def __str__(self):
    #     return self.dir_ID

# Function for on delete set
# def ondelteHOD():

class Hod(models.Model):
    hodID = models.AutoField(primary_key=True, db_column='hod_id')
    hodEmail = models.EmailField(max_length=100, db_column='hod_email')
    faculty_ID = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column='faculty_id')
    start_date = models.DateField(null=False, db_column='start_date')
    end_date = models.DateField(null=True, db_column='end_date')

    class Meta:
        db_table = 'hod'

    # def __str__(self):
    #     return self.hod_ID


class Staff(models.Model):
    staff_id = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, primary_key=True, db_column='staff_id')
    dept_ID = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')

    class Meta:
        db_table = 'staff'

    # def __str__(self):
    #     return self.staff_id


class Registrar(models.Model):
    regID = models.AutoField(primary_key=True, db_column='reg_id')
    regEmail = models.EmailField(max_length=100, db_column='reg_email')
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='faculty_id')
    start_date = models.DateField(null=False, db_column='start_date')
    end_date = models.DateField(null=True, db_column='end_date')

    class Meta:
        db_table = 'registrar'

    # def __str__(self):
    #     return self.reg_ID


class AssistRegistrar(models.Model):
    assRegID = models.AutoField(primary_key=True, db_column='ass_reg_id')
    assRegEmail = models.EmailField(max_length=100, db_column='ass_reg_email')
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='faculty_id')
    start_date = models.DateField(null=False, db_column='start_date')
    end_date = models.DateField(null=True, db_column='end_date')

    class Meta:
        db_table = 'assist_registrar'

    # def __str__(self):
    #     return str(self.areg_ID)


class Ccfs(models.Model):
    ccfs_id = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, db_column='ccfs_id')
    dept_ID = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_id')

    class Meta:
        db_table = 'ccfs'

    # def __str__(self):
    #     return self.ccfs_id


class Post(models.Model):
    postID = models.AutoField(primary_key=True, db_column='post_id')
    postEmail = models.EmailField(max_length=100, db_column='post_email')
    ccfs = models.ForeignKey(Ccfs, on_delete=models.CASCADE, db_column='ccfs_id')
    start_date = models.DateField(null=False, db_column='start_date')
    end_date = models.DateField(null=True, db_column='end_date')
    DFA = 'DFA'
    ADFA = 'ADFA'
    DEPTSEC = 'DEPTSEC'
    CHOICE = (
        (DFA, 'DEAN FACULTY AFFAIR'),
        (ADFA, 'ASSOCIATE DEAN FACULTY AFFAIR'),
        (DEPTSEC, 'DEPARTMENT SECRETARY'),
    )

    name = models.CharField(max_length=20, null=False, choices=CHOICE, db_column='post_name')

    class Meta:
        db_table = 'post'

    # def __str__(self):
    #     return str(self.post_ID)


