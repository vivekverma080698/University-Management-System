import os
import django
import datetime
from django.utils import timezone
from passlib.handlers.pbkdf2 import pbkdf2_sha256


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EMSystem.settings')
django.setup()
from salary.models import Cfti


from authentication.models import AuthTable, Department, Employee, Faculty, Director, Hod, Registrar, Ccfs, Staff, Post, AssistRegistrar

# Creating department

def create_department(dept_ID,dept_name):
    deptObj = Department()
    deptObj.dept_ID = dept_ID
    deptObj.dept_name = dept_name
    deptObj.save()


def createFaculty(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN,
            date_of_join, leave_available, borrow_available, grade, past_exp,contact):
    Authobj = AuthTable()
    Authobj.emailID = emp_ID
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'FACULTY'
    Authobj.save()

    newOBJ = AuthTable.objects.get(emailID=emp_ID)
    empObj = Employee()
    empObj.emp_ID = newOBJ
    empObj.first_name = first_name
    empObj.last_name = last_name
    empObj.date_of_birth = date_of_birth
    empObj.gender = gender
    empObj.address = address
    empObj.PAN = PAN
    empObj.date_of_join = date_of_join
    empObj.current_role = 'Faculty'
    empObj.leave_available = leave_available
    empObj.borrow_available = borrow_available
    empObj.grade_of_employment = grade
    empObj.past_experience = past_exp
    empObj.contact = contact
    empObj.save()

    FacultyObj = Faculty()
    FacultyObj.faculty_id = empObj
    FacultyObj.dept_ID = Department.objects.get(dept_ID=dept_ID)

    FacultyObj.save()


def createStaff(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN,
            date_of_join, leave_available, borrow_available, grade, past_exp,contact):
    Authobj = AuthTable()
    Authobj.emailID = emp_ID
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'STAFF'
    Authobj.save()

    newOBJ = AuthTable.objects.get(emailID=emp_ID)
    empObj = Employee()
    empObj.emp_ID = newOBJ
    empObj.first_name = first_name
    empObj.last_name = last_name
    empObj.date_of_birth = date_of_birth
    empObj.gender = gender
    empObj.address = address
    empObj.PAN = PAN
    empObj.date_of_join = date_of_join
    empObj.current_role = 'STAFF'
    empObj.leave_available = leave_available
    empObj.borrow_available = borrow_available
    empObj.grade_of_employment = grade
    empObj.past_experience = past_exp
    empObj.contact = contact
    empObj.save()

    StaffObj = Staff()
    StaffObj.staff_id = empObj
    StaffObj.dept_ID = Department.objects.get(dept_ID=dept_ID)
    StaffObj.save()


def createCCFS(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN,
            date_of_join, leave_available, borrow_available, grade, past_exp,contact):
    Authobj = AuthTable()
    Authobj.emailID = emp_ID
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'CCFS'
    Authobj.save()

    newOBJ = AuthTable.objects.get(emailID=emp_ID)
    empObj = Employee()
    empObj.emp_ID = newOBJ
    empObj.first_name = first_name
    empObj.last_name = last_name
    empObj.date_of_birth = date_of_birth
    empObj.gender = gender
    empObj.address = address
    empObj.PAN = PAN
    empObj.date_of_join = date_of_join
    empObj.current_role = 'CCFS'
    empObj.leave_available = leave_available
    empObj.borrow_available = borrow_available
    empObj.grade_of_employment = grade
    empObj.past_experience = past_exp
    empObj.contact = contact
    empObj.save()

    CCFSObj = Ccfs()
    CCFSObj.ccfs_id = empObj
    CCFSObj.dept_ID = Department.objects.get(dept_ID=dept_ID)
    CCFSObj.save()

# Have to correct it
def create_director(dirEmail, password, facultyEmail, start_date):

    try:
        # Faculty.objects.filter()faculty_id=faculty_ID)
        AuthObj = AuthTable.objects.get(emailID=facultyEmail)
        Faculty.objects.get(faculty_id=Employee.objects.get(emp_ID = AuthObj))
    except:
        print('Director should be Faculty')
        return

    try:
        aa = Director.objects.get(end_date=None)
        aa.end_date = datetime.date.today()
        aa.save()
        AuthTable.objects.get(aa.dir_ID).delete()
    except:
        pass

    Authobj = AuthTable()
    Authobj.emailID = dirEmail
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'DIRECTOR'
    Authobj.save()


    EmpObj = Employee.objects.get(emp_ID=AuthObj)
    EmpObj.current_role = 'DIRECTOR'
    EmpObj.save()

    DirObj = Director()
    DirObj.dirEmail = dirEmail
    DirObj.faculty_ID = Faculty.objects.get(faculty_id=EmpObj)
    DirObj.start_date = start_date
    DirObj.save()


def create_hod(hodEmail,password, facultyEmail, start_date):
    try:
        AuthObj = AuthTable.objects.get(emailID=facultyEmail)
        FacultyObj = Faculty.objects.get(faculty_id=Employee.objects.get(emp_ID=AuthObj))
        department = FacultyObj.dept_ID
    except:
        print('This employee is not faculty')
        return

    try:
        aa = Hod.objects.filter(end_date=None)
        for hod in aa.iterator():
            if department == hod.faculty_ID.dept_ID:
                hod.end_date = datetime.date.today()
                hod.save()
                EmpObj = Employee.objects.get(emp_ID=hod.faculty_ID.faculty_id)
                EmpObj.current_role = 'FACULTY'
                EmpObj.save()
                AuthTable.objects.get(emailID=hod.hodEmail).delete()
    except:
        pass

    Authobj = AuthTable()
    Authobj.emailID = hodEmail
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'HOD'
    Authobj.save()

    EmpObj = Employee.objects.get(emp_ID=AuthObj)
    EmpObj.current_role = 'HOD'
    EmpObj.save()

    HodObj = Hod()
    HodObj.hodEmail = hodEmail
    HodObj.faculty_ID = FacultyObj
    HodObj.start_date = start_date
    HodObj.save()

# Have to check its role
def create_registrar(regEmail, password, staffEmail, start_date):

    try:
        AuthObj = AuthTable.objects.get(emailID=staffEmail)
        StaffObj = Staff.objects.get(staff_id=Employee.objects.get(emp_ID=AuthObj))
    except:
        print('This employee is not staff')
        return

    try:
        aa = Registrar.objects.get(end_date=None)
        aa.end_date = datetime.date.today()
        aa.save()
        AuthTable.objects.get(emailID=aa.regEmail).delete()
    except:
        pass


    Authobj = AuthTable()
    Authobj.emailID = regEmail
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'REGISTRAR'
    Authobj.save()

    EmpObj = Employee.objects.get(emp_ID=AuthObj)
    EmpObj.current_role = 'REGISTRAR'
    EmpObj.save()


    RegObj = Registrar()
    RegObj.regEmail = regEmail
    RegObj.staff_id = StaffObj
    RegObj.start_date = start_date
    RegObj.save()

# here there is a doubt abour=t updating its department


def create_assist_registrar(aregEmail, password, staffEmail, start_date):

    try:
        AuthObj = AuthTable.objects.get(emailID=staffEmail)
        StaffObj = Staff.objects.get(staff_id=Employee.objects.get(emp_ID=AuthObj))
        department = StaffObj.dept_ID
    except:
        print('This employee is not staff')
        return

    Authobj = AuthTable()
    Authobj.emailID = aregEmail
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = 'ASSIST_REGISTRAR'
    Authobj.save()

    try:
        aa = AssistRegistrar.objects.filter(end_date=None)
        for asreg in aa.iterator():
            if asreg.staff_id.dept_ID == department:
                asreg.end_date = datetime.date.today()
                asreg.save()
                # EmpObj = Employee.objects.get(emp_ID=asreg.staff_id)
                # EmpObj.current_role = 'STAFF'
                # EmpObj.save()
                # AuthTable.objects.get(emailID = asreg.areg_ID).delete()

                EmpObj = Employee.objects.get(emp_ID=asreg.staff_id.staff_id)
                EmpObj.current_role = 'STAFF'
                EmpObj.save()
                AuthTable.objects.get(emailID=asreg.assRegEmail).delete()

    except:
        pass

    EmpObj = Employee.objects.get(emp_ID=AuthObj)
    EmpObj.current_role = 'ASSIST_REGISTRAR'
    EmpObj.save()

    AregObj = AssistRegistrar()
    AregObj.assRegEmail = aregEmail
    AregObj.staff_id = StaffObj
    AregObj.start_date = start_date
    AregObj.save()

# Giving Special post


def givePost(postEmail, password, ccfsEmail,start_date,name):

    try:
        AuthObj = AuthTable.objects.get(emailID=ccfsEmail)
        CCFSObj = Ccfs.objects.get(ccfs_id=Employee.objects.get(emp_ID=AuthObj))

        # CCFSObj = Ccfs.objects.get(ccfs_id=ccfs_id)
    except:
        print('This employee is not CCFS')
        return

    try:
        aa = Post.objects.filter(end_date=None)
        for postobj in aa.iterator():
            if postobj.name == name:
                postobj.end_date = datetime.date.today()
                postobj.save()

                EmpObj = Employee.objects.get(emp_ID=postobj.ccfs.ccfs_id)
                EmpObj.current_role = 'CCFS'
                EmpObj.save()
                AuthTable.objects.get(emailID = postobj.post_ID).delete()

                # EmpObj = Employee.objects.get(emp_ID=asreg.staff_id.staff_id)
                # EmpObj.current_role = 'STAFF'
                # EmpObj.save()
                # AuthTable.objects.get(emailID=asreg.assRegEmail).delete()

    except:
        print('Something wrong')
        pass

    Authobj = AuthTable()
    Authobj.emailID = postEmail
    Authobj.password = pbkdf2_sha256.hash(password)
    Authobj.role = name
    Authobj.save()

    EmpObj = Employee.objects.get(emp_ID=AuthObj)
    EmpObj.current_role = name
    EmpObj.save()

    postObj = Post()
    postObj.postEmail = postEmail
    postObj.ccfs = CCFSObj
    postObj.start_date = start_date
    postObj.name = name
    postObj.save()


def delete_employee(emailID):
    AuthOBJ = AuthTable.objects.get(emailID=emailID)
    AuthOBJ.delete()


def clear_database():
    AuthTable.objects.all().delete()


def clear_aReg():
    AssistRegistrar.objects.all().delete()

def clear_post():
    Post.objects.all().delete()


def clear_hod():
    Hod.objects.all().delete()


def clear_dir():
    Director.objects.all().delete()


def clear_reg():
    Registrar.objects.all().delete()

def insert_cfti(experience, grade, base_salary):
    cfti = Cfti()
    cfti.experience = experience
    cfti.grade = grade
    cfti.baseSalary = base_salary
    cfti.lastUpdated = timezone.now()
    cfti.save()


if __name__ == '__main__':
    print('Hello')
    # insert_cfti(5,'A',800)
    # insert_cfti(5,'A',700)
    # insert_cfti(5,'A',400)

    # create_department(10001,'CSE')
    # create_department(10002,'ME')
    # create_department(10003,'EE')
    # create_department(10004,'ACCOUNT')
    # create_department(10005,'PURCHASE')
    # create_department(10006,'ESTABLISHMENT')
    #
    # createFaculty(emp_ID='vivek@gmail.com', password='vivek', dept_ID=10001, first_name='Vivek', last_name='Verma', date_of_birth='1999-08-08', gender='MALE', address='IIT', PAN='XXXXXX', date_of_join='1999-09-09', leave_available=10, borrow_available=10, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='ram@gmail.com', password='ram', dept_ID=10002 , first_name='Ram',last_name= 'Krishna',date_of_birth= '1999-05-04',gender= 'Male', address='SE-137 IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2018-04-03', leave_available=20,borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='shailza@gmail.com',password='shailza', dept_ID=10003, first_name='Shailza', last_name= 'Virmani',date_of_birth= '2001-04-27', gender= 'Female', address= 'Kanpur',PAN= 'XXXX-XXXX-XXXX',date_of_join= '2018-11-04',leave_available= 20, borrow_available=20,grade='A',past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='sarit@gmail.com', password='sarit', dept_ID=10004, first_name= 'Sarit', last_name='Das', date_of_birth='1965-12-08', gender='Male', address='SW-110 IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2011-01-01', leave_available=12, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='anil@gmail.com', password='anil', dept_ID=10005, first_name= 'Anil', last_name='Shukla', date_of_birth='1985-04-04', gender='Male', address='SE-137 IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2012-02-03', leave_available=0, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='sodhi@gmail.com', password='sodhi', dept_ID=10006, first_name='Balwinder', last_name='Sodhi', date_of_birth='1975-01-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2013-03-04', leave_available=18, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='vineet@gmail.com', password='vineet', dept_ID=10001, first_name='Vineet', last_name='Mehta', date_of_birth='1998-11-06', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2014-04-01', leave_available=7, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='shyam@gmail.com', password='shyam', dept_ID=10002, first_name='Shyam', last_name='Shunder', date_of_birth='1965-05-04', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2015-05-03', leave_available=5, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='sonu@gmail.com', password='sonu', dept_ID=10003, first_name='Sonu', last_name='Singh', date_of_birth='1999-09-17', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2016-06-04', leave_available=14, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createFaculty(emp_ID='prinshu@gmail.com', password='prinshu', dept_ID=10004, first_name='Prinshu', last_name='Kumar', date_of_birth='1998-04-08', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2017-07-01', leave_available=13, borrow_available=20, grade='A', past_exp=5, contact='9812939021')

    # createStaff(emp_ID='abhisheik@gmail.com', password='abhisheik', dept_ID=10005, first_name='Abhisheik', last_name='Singh', date_of_birth='1999-05-10', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2018-08-03', leave_available=8, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='gunturi@gmail.com', password='gunturi', dept_ID=10006, first_name='Gunturi', last_name='Sir', date_of_birth='1975-04-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2014-09-04', leave_available=0, borrow_available=14, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='hcverma@gmail.com', password='hcverma', dept_ID=10001, first_name='Harish', last_name='Verma', date_of_birth='1960-09-08', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2008-10-01', leave_available=7, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='ckn@gmail.com', password='ckn', dept_ID=10002, first_name='CKN', last_name='Narayan', date_of_birth='1970-02-04', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2009-11-03', leave_available=19, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='krishna@gmail.com', password='krishna', dept_ID=10003, first_name='Krishna', last_name='Das', date_of_birth='1993-07-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2010-12-04', leave_available=8, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='ganesh@gmail.com', password='ganesh', dept_ID=10004, first_name='Ganesh', last_name='Sharma', date_of_birth='1998-11-08', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2019-01-01', leave_available=20, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='praveen@gmail.com', password='praveen', dept_ID=10005, first_name='Praveen', last_name='Kumar', date_of_birth='1999-05-04', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2018-04-03', leave_available=20, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='hamid@gmail.com', password='hamid', dept_ID=10006, first_name='Hamid', last_name='Ansari', date_of_birth='2001-04-27', gender='Male', address='Kanpur', PAN='XXXX-XXXX-XXXX', date_of_join='2018-11-04', leave_available=20, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='prerna@gmail.com', password='prerna', dept_ID=10001, first_name='Prerna', last_name='Singh', date_of_birth='1965-12-08', gender='Female', address='SW-110 IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2011-01-01', leave_available=12, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createStaff(emp_ID='komal@gmail.com', password='komal', dept_ID=10002, first_name='Komal', last_name='Chugh', date_of_birth='1985-04-04', gender='Female', address='SE-137 IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2012-02-03', leave_available=0, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    #
    # createCCFS(emp_ID='chomu@gmail.com', password='chomu', dept_ID=10003, first_name='Chomu', last_name='Chomu', date_of_birth='1975-01-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2013-03-04', leave_available=18, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='vikas@gmail.com', password='vikas', dept_ID=10004, first_name='Vikas', last_name='Singh', date_of_birth='1998-11-06', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2014-04-01', leave_available=7, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='satyendra@gmail.com', password='satyendra', dept_ID=10005, first_name='Satyendra', last_name='Nath', date_of_birth='1965-05-04', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2015-05-03', leave_available=5, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='asif@gmail.com', password='asif', dept_ID=10006, first_name='Asif', last_name='Ansari', date_of_birth='1999-09-17', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2016-06-04', leave_available=14, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='atif@gmail.com', password='atif', dept_ID=10001, first_name='Atif', last_name='Aslam', date_of_birth='1998-04-08', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2017-07-01', leave_available=13, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='kartik@gmail.com', password='kartik', dept_ID=10002, first_name='Kartik', last_name='Vishkarma', date_of_birth='1999-05-10', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2018-08-03', leave_available=8, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='yash@gmail.com', password='yash', dept_ID=10003, first_name='Yash', last_name='Agrawal', date_of_birth='1975-04-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2014-09-04', leave_available=0, borrow_available=14, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='mohit@gmail.com', password='mohit', dept_ID=10004, first_name='Mohit', last_name='Suri', date_of_birth='1960-09-08', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2008-10-01', leave_available=7, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='prakash@gmail.com', password='praksh', dept_ID=10005, first_name='Prakash', last_name='Naglot', date_of_birth='1970-02-04', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2009-11-03', leave_available=19, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    # createCCFS(emp_ID='rohit@gmail.com', password='rohit', dept_ID=10006, first_name='Rohit', last_name='Kumar', date_of_birth='1993-07-27', gender='Male', address='IIT Ropar', PAN='XXXX-XXXX-XXXX', date_of_join='2010-12-04', leave_available=8, borrow_available=20, grade='A', past_exp=5, contact='9812939021')
    #
    # createCCFS(emp_ID='mushkan@gmail.com', password='mushkan', dept_ID=10004, first_name='Mushkan', last_name='Zoya',
    #            date_of_birth='1993-07-27', gender='Female', address='IIT Ropar', PAN='XXXX-XXXX-XXXX',
    #            date_of_join='2010-12-04', leave_available=8, borrow_available=20, grade='A', past_exp=5,
    #            contact='9822539423')
    # create_director(dirEmail='dir_sarit@gmail.com', password='dir_sarit', facultyEmail='sarit@gmail.com', start_date='2015-01-01')

    # create_registrar(regEmail='reg_abhisheik@gmail.com', password='reg_abhisheik', staffEmail='abhisheik@gmail.com', start_date='2015-01-01')
    #
    # create_assist_registrar(aregEmail='areg_ganesh@gmail.com', password='areg_ganesh', staffEmail='ganesh@gmail.com', start_date='2015-02-11')
    # create_assist_registrar(aregEmail='areg_praveen@gmail.com', password='areg_praveen', staffEmail='praveen@gmail.com', start_date='2015-02-07')
    # create_assist_registrar(aregEmail='areg_hamid@gmail.com', password='areg_hamid', staffEmail='hamid@gmail.com', start_date='2015-02-03')

    # create_hod(hodEmail='hod_vivek@gmail.com', password='hod_vivek', facultyEmail='vivek@gmail.com', start_date='2015-06-05')
    # create_hod(hodEmail='hod_ram@gmail.com', password='hod_ram', facultyEmail='ram@gmail.com', start_date='2015-06-05')
    # create_hod(hodEmail='hod_shailza@gmail.com', password='hod_shailza', facultyEmail='shailza@gmail.com', start_date='2015-06-05')

    # givePost(postEmail='DFA_chomu@gmail.com', password='DFA_chomu', ccfsEmail='chomu@gmail.com', start_date='2015-02-27', name='DFA')
    # givePost(postEmail='ADFA_vikas@gmail.com', password='ADFA_vikas', ccfsEmail='vikas@gmail.com', start_date='2015-02-28', name='ADFA')
    # givePost(postEmail='DEPTSEC_satyendra@gmail.com', password='DEPTSEC_satyendra', ccfsEmail='satyendra@gmail.com', start_date='2015-02-27', name='DEPTSEC')

    # print(datetime.date.today())

    #
    # clear_aReg()
    # clear_dir()
    # clear_hod()
    # clear_post()
    # clear_reg()
    # clear_database()
