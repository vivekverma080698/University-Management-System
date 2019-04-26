import os
import django

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from django.db import connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EMSystem.settings')
django.setup()

from authentication.models import AuthTable
from authentication.models import Employee

# def my_custom_sql():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM employee;")
#         return cursor.fetchall()
#
#
# def register_emp_in_auth_table(email, password, role):
#     encrypt_password = pbkdf2_sha256.hash(password)
#     with connection.cursor() as cursor:
#         cursor.execute("INSERT INTO authtable VALUES(%s, %s, %s);",[email,encrypt_password,role])
#
#
# def register_emp_in_employee_table(emp_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, _current_role, leave_available, borrow_available, grade, past_exp):
#     with connection.cursor() as cursor:
#         cursor.execute("INSERT INTO employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",[emp_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, _current_role, leave_available, borrow_available, grade, past_exp])
#
#
# def create_department(dept_ID,dept_name):
#     with connection.cursor() as cursor:
#         cursor.execute("INSERT INTO department VALUES(%s, %s);",[dept_ID, dept_name])
#     print('hello')
#
#
# def create_hod(hod_id,password, faculty_id, start_date):
#     encrypt_password = pbkdf2_sha256.hash(password)
#     register_emp_in_auth_table(hod_id, encrypt_password, 'HOD')
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT "hod_id" , "faculty_id" from hod where end_date is null;')
#         result = cursor.fetchall()
#         if len(result) > 0:
#             cursor.execute('UPDATE hod set end_date = now() where "hod_id" = %s;', [result[0][0]])
#             print('Previous HOD removed')
#         cursor.execute('UPDATE employee set "current_role" = \'HOD\' where "emp_id" = %s;',[faculty_id])
#         cursor.execute('INSERT INTO hod("hod_id","faculty_id","start_date") VALUES(%s, %s, %s);', [hod_id, faculty_id, start_date])
#         print('HOD created')
#
#
# def create_director(dir_ID, password, faculty_ID, start_date):
#     encrypt_password = pbkdf2_sha256.hash(password)
#     register_emp_in_auth_table(dir_ID, encrypt_password, 'DIRECTOR')
#     with connection.cursor() as cursor:
#         cursor.execute('INSERT INTO')
#         cursor.execute('SELECT "dir_id" , "faculty_id" from director where end_date is null;')
#         result = cursor.fetchall()
#         if len(result) > 0:
#             cursor.execute('UPDATE director set end_date = now() where "dir_id" = %s;', [result[0][0]])
#             print('Previous director removed')
#         cursor.execute('UPDATE employee set "current_role" = \'DIRECTOR\' where "emp_id" = %s;',[faculty_ID])
#         cursor.execute('INSERT INTO director("dir_id","faculty_id","start_date") VALUES(%s, %s, %s);', [dir_ID, faculty_ID, start_date])
#         print('Director created')
#
#
# def create_registrar(reg_ID, password, faculty_ID, start_date):
#     encrypt_password = pbkdf2_sha256.hash(password)
#     register_emp_in_auth_table(reg_ID, encrypt_password, 'REGISTRAR')
#
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT "dir_id" , "faculty_id" from registrar where end_date is null;')
#         result = cursor.fetchall()
#         if len(result) > 0:
#             cursor.execute('UPDATE registrar set end_date = now() where "reg_id" = %s;', [result[0][0]])
#             print('Previous director removed')
#         cursor.execute('UPDATE employee set "current_role" = \'REGISTRAR\' where "emp_id" = %s;',[faculty_ID])
#         cursor.execute('INSERT INTO registrar("reg_id","faculty_id","start_date") VALUES(%s, %s, %s);', [reg_ID, faculty_ID, start_date])
#         print('Director created')
#
#
# def create_assist_registrar(areg_ID, password, faculty_ID, start_date):
#     encrypt_password = pbkdf2_sha256.hash(password)
#     register_emp_in_auth_table(areg_ID, encrypt_password, 'ASSIST_REGISTRAR')
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT "areg_ID" , "staff_id" from assist_registrar where end_date is null;')
#         result = cursor.fetchall()
#         if len(result) > 0:
#             cursor.execute('UPDATE assist_registrar set end_date = now() where "staff_id" = %s;', [result[0][0]])
#             print('Previous director removed')
#         cursor.execute('UPDATE employee set "current_role" = \'ASSIST_REGISTRAR\' where "emp_id" = %s;',[faculty_ID])
#         cursor.execute('INSERT INTO assist_registrar("areg_ID","staff_id","start_date") VALUES(%s, %s, %s);', [areg_ID, faculty_ID, start_date])
#         print('Director created')
#
#
# def giveBonus(month, year, bonus):
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT bonus FROM calender where month=%s and year = %s;',[month,year])
#         result = cursor.fetchall()
#         if len(result) > 0:
#             print('Bonus already given')
#         else:
#             cursor.execute('INSERT INTO calender(month,year,bonus) VALUES(%s, %s, %s);',[month,year,bonus])
#             print('Bonus given')
#
# def createFaculty(faculty_ID, dept_ID):
#     with connection.cursor() as cursor:
#         cursor.execute('UPDATE employee set "current_role" = \'FACULTY\' where "emp_id" = %s;',[faculty_ID])
#         cursor.execute('INSERT INTO faculty VALUES(%s, %s);',[faculty_ID,dept_ID])
#
#
# def createSTAFF(staff_ID, dept_ID):
#     with connection.cursor() as cursor:
#         cursor.execute('UPDATE employee set "current_role" = \'STAFF\' where "emp_id" = %s;',[staff_ID])
#         cursor.execute('INSERT INTO staff VALUES(%s, %s);',[staff_ID,dept_ID])
#
#
# def createCCFS(ccfs_ID, dept_ID):
#     with connection.cursor() as cursor:
#         cursor.execute('UPDATE employee set "current_role" = \'CCFS\' where "emp_id" = %s;',[ccfs_ID])
#         cursor.execute('INSERT INTO faculty VALUES(%s, %s);',[ccfs_ID,dept_ID])


# def Faculty(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, leave_available, borrow_available, grade, past_exp):
#     register_emp_in_auth_table(emp_ID, password, 'FACULTY')
#     with connection.cursor() as cursor:
#         cursor.execute('INSERT INTO employee("emp_id", "first_name", "last_name", "date_of_birth", "gender", "address", "pan", "date_of_join", "current_role", "leave_available", "borrow_available", "grade_of_employment", "past_experience") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',[emp_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, 'FACULTY', leave_available, borrow_available, grade, past_exp])
#         cursor.execute('INSERT INTO faculty("faculty_id","dept_id") VALUES(%s, %s);',[emp_ID,dept_ID])
#
#
# def Staff(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, leave_available, borrow_available, grade, past_exp):
#     register_emp_in_auth_table(emp_ID, password,'STAFF')
#     with connection.cursor() as cursor:
#         cursor.execute('INSERT INTO employee("emp_id", "first_name", "last_name", "date_of_birth", "gender", "address", "pan", "date_of_join", "current_role", "leave_available", "borrow_available", "grade_of_employment", "past_experience") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',[emp_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, 'STAFF', leave_available, borrow_available, grade, past_exp])
#         cursor.execute('INSERT INTO staff VALUES(%s, %s);',[emp_ID,dept_ID])
#
#
# def CCFS(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, leave_available, borrow_available, grade, past_exp):
#     register_emp_in_auth_table(emp_ID, password,'CCFS')
#     with connection.cursor() as cursor:
#         cursor.execute('INSERT INTO employee("emp_id", "first_name", "last_name", "date_of_birth", "gender", "address", "pan", "date_of_join", "current_role", "leave_available", "borrow_available", "grade_of_employment", "past_experience") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',[emp_ID, first_name, last_name, date_of_birth, gender, address, PAN, date_of_join, 'CCFS', leave_available, borrow_available, grade, past_exp])
#         cursor.execute('INSERT INTO ccfs VALUES(%s, %s);',[emp_ID,dept_ID])

def createFaculty(emp_ID, password, dept_ID, first_name, last_name, date_of_birth, gender, address, PAN,
            date_of_join, leave_available, borrow_available, grade, past_exp):
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
    empObj.save()

    FacultyObj = Faculty()
    FacultyObj.faculty_id = emp_ID
    FacultyObj.dept_ID = dept_ID
    FacultyObj.save()

# Doubt
# def create_assist_registrar(areg_ID, faculty_ID, start_date):
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT "areg_ID" , "staff_id" from assist_registrar where end_date is null;')
#         result = cursor.fetchall()
#         if len(result) > 0:
#             cursor.execute('UPDATE assist_registrar set end_date = now() where "staff_id" = %s;', [result[0][0]])
#             print('Previous director removed')
#         cursor.execute('UPDATE employee set "current_role" = \'ASSIST_REGISTRAR\' where "emp_id" = %s;',[faculty_ID])
#         cursor.execute('INSERT INTO assist_registrar("areg_ID","staff_id","start_date") VALUES(%s, %s, %s);', [areg_ID, faculty_ID, start_date])
#         print('Director created')


def delete_employee(emailID):
    AuthOBJ = AuthTable.objects.get(emailID=emailID)
    AuthOBJ.delete()

if __name__ == '__main__':

    print('Hello')

    # print(my_custom_sql())
    # register employee
    #
    # print(register_emp_in_auth_table('vivek@gmail.com', 'vivek','FACULTY'))
    # print(register_emp_in_auth_table('ram@gmail.com', 'ram'))
    # print(register_emp_in_auth_table('shailza@gmail.com', 'shailza'))
    # print(register_emp_in_auth_table('sarit@gmail.com', 'sarit'))
    # print(register_emp_in_auth_table('anil@gmail.com', 'anil'))
    # print(register_emp_in_auth_table('sodhi@gmail.com', 'sodhi'))
    # print(register_emp_in_auth_table('vineet@gmail.com', 'vineet'))
    # print(register_emp_in_auth_table('shyam@gmail.com', 'shyam'))
    # print(register_emp_in_auth_table('sonu@gmail.com', 'sonu'))
    # print(register_emp_in_auth_table('prinshu@gmail.com', 'prinshu'))
    # print(register_emp_in_auth_table('abhisheik@gmail.com', 'abhisheik'))
    # print(register_emp_in_auth_table('gunturi@gmail.com', 'gunturi'))
    # print(register_emp_in_auth_table('hcverma@gmail.com', 'hcverma'))
    # print(register_emp_in_auth_table('ckn@gmail.com', 'ckn'))
    # print(register_emp_in_auth_table('krishna@gmail.com', 'krishna'))
    # print(register_emp_in_auth_table('ganesh@gmail.com', 'ganesh'))
    # print(register_emp_in_auth_table('praveen@gmail.com', 'praveen'))
    # print(register_emp_in_auth_table('hamid@gmail.com', 'hamid'))
    # print(register_emp_in_auth_table('prerna@gmail.com', 'prerna'))
    # print(register_emp_in_auth_table('komal@gmail.com', 'komal'))
    # print(register_emp_in_auth_table('chomu@gmail.com', 'chomu'))
    # print(register_emp_in_auth_table('vikas@gmail.com', 'vikas'))
    # print(register_emp_in_auth_table('satyendra@gmail.com', 'satyendra'))
    # print(register_emp_in_auth_table('asif@gmail.com', 'asif'))
    # print(register_emp_in_auth_table('atif@gmail.com', 'atif'))
    # print(register_emp_in_auth_table('kartik@gmail.com', 'kartik'))
    # print(register_emp_in_auth_table('yash@gmail.com', 'yash'))
    # print(register_emp_in_auth_table('mohit@gmail.com', 'mohit'))
    # print(register_emp_in_auth_table('prakash@gmail.com', 'prakash'))
    # print(register_emp_in_auth_table('rohit@gmail.com', 'rohit'))
    #
    # # filling employee info
    #
    # register_emp_in_employee_table('vivek@gmail.com', 'Vivek', 'Verma', '1998-11-08', 'Male', 'SW-110 IIT Ropar', 'XXXX-XXXX-XXXX', '2019-01-01', 'EMP',20,20,'A',12)
    # register_emp_in_employee_table('ram@gmail.com', 'Ram', 'Krishna', '1999-05-04', 'Male', 'SE-137 IIT Ropar', 'XXXX-XXXX-XXXX', '2018-04-03', 'EMP',20,20,'B',10)
    # register_emp_in_employee_table('shailza@gmail.com', 'Shailza', 'Virmani', '2001-04-27', 'Female', 'Kanpur', 'XXXX-XXXX-XXXX', '2018-11-04', 'EMP',20,20,'C',5)
    # register_emp_in_employee_table('sarit@gmail.com', 'Sarit', 'Das', '1965-12-08', 'Male', 'SW-110 IIT Ropar', 'XXXX-XXXX-XXXX', '2011-01-01', 'EMP',12,20,'A',7)
    # register_emp_in_employee_table('anil@gmail.com', 'Anil', 'Shukla', '1985-04-04', 'Male', 'SE-137 IIT Ropar', 'XXXX-XXXX-XXXX', '2012-02-03', 'EMP',0,20,'B',4)
    # register_emp_in_employee_table('sodhi@gmail.com', 'Balwinder', 'Sodhi', '1975-01-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2013-03-04', 'EMP',18,20,'C',5)
    # register_emp_in_employee_table('vineet@gmail.com', 'Vineet', 'Mehta', '1998-11-06', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2014-04-01', 'EMP',7,20,'A',5)
    # register_emp_in_employee_table('shyam@gmail.com', 'Shyam', 'Shunder', '1965-05-04', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2015-05-03', 'EMP',5,20,'B',3)
    # register_emp_in_employee_table('sonu@gmail.com', 'Sonu', 'Singh', '1999-09-17', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2016-06-04', 'EMP',14,20,'C',9)
    # register_emp_in_employee_table('prinshu@gmail.com', 'Prinshu', 'Kumar', '1998-04-08', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2017-07-01', 'EMP',13,20,'A',1)
    # register_emp_in_employee_table('abhisheik@gmail.com', 'Abhisheik', 'Singh', '1999-05-10', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2018-08-03', 'EMP',8,20,'B',10)
    # register_emp_in_employee_table('gunturi@gmail.com', 'Gunturi', 'Sir', '1975-04-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2014-09-04', 'EMP',0,14,'C',11)
    # register_emp_in_employee_table('hcverma@gmail.com', 'Harish', 'Verma', '1960-09-08', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2008-10-01', 'EMP',7,20,'A',23)
    # register_emp_in_employee_table('ckn@gmail.com', 'CKN', 'Narayan', '1970-02-04', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2009-11-03', 'EMP',19,20,'B',5)
    # register_emp_in_employee_table('krishna@gmail.com', 'Krishna', 'Das', '1993-07-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2010-12-04', 'EMP',8,20,'C',4)
    # register_emp_in_employee_table('ganesh@gmail.com', 'Ganesh', 'Sharma', '1998-11-08', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2019-01-01', 'EMP',20,20,'A',12)
    # register_emp_in_employee_table('praveen@gmail.com', 'Praveen', 'Kumar', '1999-05-04', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2018-04-03', 'EMP',20,20,'B',10)
    # register_emp_in_employee_table('hamid@gmail.com', 'Hamid', 'Ansari', '2001-04-27', 'Male', 'Kanpur', 'XXXX-XXXX-XXXX', '2018-11-04', 'EMP',20,20,'C',5)
    # register_emp_in_employee_table('prerna@gmail.com', 'Prerna', 'Singh', '1965-12-08', 'Female', 'SW-110 IIT Ropar', 'XXXX-XXXX-XXXX', '2011-01-01', 'EMP',12,20,'A',7)
    # register_emp_in_employee_table('komal@gmail.com', 'Komal', 'Chugh', '1985-04-04', 'Female', 'SE-137 IIT Ropar', 'XXXX-XXXX-XXXX', '2012-02-03', 'EMP',0,20,'B',4)
    # register_emp_in_employee_table('chomu@gmail.com', 'Chomu', 'Chomu', '1975-01-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2013-03-04', 'EMP',18,20,'C',5)
    # register_emp_in_employee_table('vikas@gmail.com', 'Vikas', 'Singh', '1998-11-06', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2014-04-01', 'EMP',7,20,'A',5)
    # register_emp_in_employee_table('satyendra@gmail.com', 'Satyendra', 'Nath', '1965-05-04', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2015-05-03', 'EMP',5,20,'B',3)
    # register_emp_in_employee_table('asif@gmail.com', 'Asif', 'Ansari', '1999-09-17', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2016-06-04', 'EMP',14,20,'C',9)
    # register_emp_in_employee_table('atif@gmail.com', 'Atif', 'Aslam', '1998-04-08', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2017-07-01', 'EMP',13,20,'A',1)
    # register_emp_in_employee_table('kartik@gmail.com', 'Kartik', 'Vishkarma', '1999-05-10', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2018-08-03', 'EMP',8,20,'B',10)
    # register_emp_in_employee_table('yash@gmail.com', 'Yash', 'Agrawal', '1975-04-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2014-09-04', 'EMP',0,14,'C',11)
    # register_emp_in_employee_table('mohit@gmail.com', 'Mohit', 'Suri', '1960-09-08', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2008-10-01', 'EMP',7,20,'A',23)
    # register_emp_in_employee_table('prakash@gmail.com', 'Prakash', 'Naglot', '1970-02-04', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2009-11-03', 'EMP',19,20,'B',5)
    # register_emp_in_employee_table('rohit@gmail.com', 'Rohit', 'Kumar', '1993-07-27', 'Male', 'IIT Ropar', 'XXXX-XXXX-XXXX', '2010-12-04', 'EMP',8,20,'C',4)
    #
    # # cretaing department
    #

    # create_department(10001,'CSE')
    # create_department(10002,'ME')
    # create_department(10003,'EE')
    # create_department(10004,'ACCOUNT')
    # create_department(10005,'PURCHASE')
    # create_department(10006,'ESTABLISHMENT')

    # create_director('dir_sarit@gmail.com','sarit@gmail.com','2015-07-01')
    # Faculty(emp_ID='vivek@gmail.com', password='vivek', dept_ID=10001, first_name='Vivek', last_name='Verma', date_of_birth='1999-08-08', gender='MALE', address='IIT', PAN='XXXXXX',date_of_join='1999-09-09', leave_available=10, borrow_available=10, grade='A', past_exp=10)
    delete_employee('vivek@gmail.com')



# class EmployeeView(generic.FormView):
#     template_name = 'authentication/employee.html'
#
#     def get(self, request, *args, **kwargs):
#         emp = Employee.objects.all().get(emp_ID=request.session.get('EMPNAME'))
#         emplist = []
#         try:
#             payslips = Payslip.objects.all().get(slip_staff = request.session.get('EMPNAME'))
#             for slips in payslips.iterator():
#                 emplist.append([slips.slip_gen, slips.month, slips.year, slips.experience, slips.salary])
#             print(emplist)
#         except:
#             payslips = 'No PaySlip generated by authority'
#
#         print(request.session.get('EMPNAME'), 'OK')
#         return render(request, self.template_name, {'EMPNAME':request.session.get('EMPNAME'), 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available,'payslip':payslips, 'emplist':emplist})
#
#     def post(self, request, *args, **kwargs):
#
#         if request.POST['button'] == 'see':
#             print('Button see pressed', request.POST['start'])
#
#         if request.POST['button'] == 'generate':
#             # payObject = Payslip()
#             # payObject.slip_gen = 1    ## establishment staff id staff
#             # payObject.slip_staff = 1  ##
#             # payObject.month = 1
#             # payObject.year = 1
#             # payObject.experience = 1
#             # payObject.salary = 1
#             # payObject.save()
#
#             print('Button generate pressed', request.POST['start'])
#
#         emp = Employee.objects.all().get(emp_ID=request.session.get('EMPNAME'))
#         emplist = []
#         try:
#             payslips = Payslip.objects.all().get(slip_staff = request.session.get('EMPNAME'))
#             for slips in payslips.iterator():
#                 emplist.append([slips.slip_gen, slips.month, slips.year, slips.experience, slips.salary])
#             print(emplist)
#         except:
#             payslips = 'No PaySlip generated by authority'
#
#         print(request.session.get('EMPNAME'), 'OK')
#         return render(request, self.template_name, {'EMPNAME':request.session.get('EMPNAME'), 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available,'payslip':payslips, 'emplist':emplist})
#
