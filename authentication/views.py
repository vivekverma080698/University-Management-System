from django.views import generic
from django.shortcuts import render, redirect
from authentication.models import AuthTable, Employee, Faculty, Director, Hod, Registrar, Staff, Post, AssistRegistrar, \
    Ccfs
from salary.models import Payslip, Cfti, Calender, paperTrailPayslip
from passlib.hash import pbkdf2_sha256
import datetime
from django.contrib.auth import logout
from decimal import Decimal

def logout_view(request):
    logout(request)
    return redirect('authentication:Index')

# Function for updating the value in the paperTrailPaySlip Table in database
def updateValue(payslip_id,comment,role, empIDGen,status):
    obj = paperTrailPayslip()
    obj.payslip_id = payslip_id
    obj.comment = comment
    obj.role = role
    obj.empIDGen = empIDGen
    obj.status = status
    obj.save()



class IndexView(generic.FormView):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            del request.session['ROLE']
        except KeyError:
            pass
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        for users in AuthTable.objects.all():
            if users.emailID == request.POST['email'] and pbkdf2_sha256.verify(request.POST['passwd'],users.password):
                request.session['ROLEID'] = users.emailID
                request.session['ROLE'] = users.role

                if users.role == 'DIRECTOR':
                    print('I am Director', users.emailID)
                    temp = Director.objects.get(dirEmail=users.emailID)
                    print('I am Director' , temp)
                    request.session['EMPID'] = temp.faculty_ID.faculty_id.emp_ID.emailID
                    return redirect('director/')

                elif users.role == 'REGISTRAR':
                    print('I am reg')
                    temp = Registrar.objects.all().get(regEmail=users.emailID)
                    request.session['EMPID'] = temp.staff_id.staff_id.emp_ID.emailID
                    return redirect('registrar/')

                elif users.role == 'ASSIST_REGISTRAR':
                    print('I am areg ', users.emailID)
                    temp = AssistRegistrar.objects.all().get(assRegEmail=users.emailID)
                    print(temp.staff_id.staff_id.emp_ID.emailID)
                    request.session['EMPID'] = temp.staff_id.staff_id.emp_ID.emailID
                    return redirect('assistreg/')

                elif users.role == 'HOD':
                    print('I am HOD')
                    temp = Hod.objects.all().get(hodEmail=users.emailID)
                    request.session['EMPID'] = temp.faculty_ID.faculty_id.emp_ID.emailID
                    return redirect('hod/')

                elif users.role == 'DFA':
                    print('I am DFA')
                    temp = Post.objects.all().get(postEmail=users.emailID)
                    request.session['EMPID'] = temp.ccfs.ccfs_id.emp_ID.emailID
                    return redirect('dfa/')

                elif users.role == 'ADFA':
                    print('i am ADFA')
                    temp = Post.objects.all().get(postEmail=users.emailID)
                    request.session['EMPID'] = temp.ccfs.ccfs_id.emp_ID.emailID
                    return redirect('adfa/')

                elif users.role == 'DEPTSEC':
                    print('I am deptsec')
                    temp = Post.objects.get(postEmail=users.emailID)
                    request.session['EMPID'] = temp.ccfs.ccfs_id.emp_ID.emailID
                    return redirect('deptsec/')

                elif users.role == 'CCFS':
                    print('I am ccfs')
                    request.session['EMPID'] = users.emailID
                    return redirect('ccfs/')

                elif users.role == 'STAFF':
                    print('I am staff')
                    request.session['EMPID'] = users.emailID
                    return redirect('staff/')

                elif users.role == 'FACULTY':
                    print('I am faculty')
                    print(users.emailID)
                    request.session['EMPID'] = users.emailID
                    return redirect('faculty/')

                else:
                    print('Wrong')

        return render(request, self.template_name, {'message_state':True, 'messages':'You are not member of organization'})


class FacultyView(generic.FormView):
    template_name = 'authentication/faculty.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.session['ROLE'] == 'FACULTY':
                AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
                emp = Employee.objects.get(emp_ID=AuthObj)
                DeptObj = Faculty.objects.get(faculty_id=emp)
                # print(emp ,'  ------- ', DeptObj)
                # print('Department name' , DeptObj.dept_ID.dept_name)
                return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'), 'Department':DeptObj.dept_ID.dept_name, 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})
        except Exception as e:
            print('Faculty ', str(e))
            pass
        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):
        AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        emp = Employee.objects.get(emp_ID=AuthObj)
        DeptObj = Faculty.objects.get(faculty_id=emp)
        emplist = []
        try:
            if request.POST['button'] == 'see':
                # when payslip not exist
                messageStatus = False
                # show table of payslip
                messageSeeStatus= False
                print(request.POST)
                try:
                    payObject = Payslip.objects.get(payslip_id=str(request.POST['start']) +'_'+str(request.session.get('EMPID')))
                    emplist = self.getpaySlip(payObject)
                    messageSee = ''
                    messageSeeStatus = True
                    print('emplist ',emplist)
                except Exception as e:
                    print('Error in see : ',str(e))
                    # If payslip not exit in table
                    messageSee = 'Payslip does not exit. Please generate it.'
                    messageStatus = True

                return render(request, self.template_name,
                              {'messageStatus':messageStatus, 'Department':DeptObj.dept_ID.dept_name,'messageSeeStatus':messageSeeStatus,'messageSee':messageSee, 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                               'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available, 'emplist':emplist})

            if request.POST['button'] == 'generate':
                messageforUserFlag = True
                messageforUser = self.avoidMultipleGenerate(request, int(request.POST['start'].split('-')[1]),int(request.POST['start'].split('-')[0]),emp)
                print('Button generate pressed', request.POST['start'])
                return render(request, self.template_name,
                              {'messageforUserFlag':messageforUserFlag, 'Department':DeptObj.dept_ID.dept_name,'messageforUser':messageforUser, 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                               'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available})

        except Exception as e:
            print('Wrong', str(e))
            pass
        return render(request, self.template_name,
                      {'EMPNAME': request.session.get('ROLEID'), 'Department':DeptObj.dept_ID.dept_name, 'role': request.session.get('ROLE'),
                       'first_name': emp.first_name, 'last_name': emp.last_name,
                       'leave_available': emp.leave_available})

    # check whether payslip already exists or not

    def checkPaySlip(self,request, month, year, empID):
        payslip = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(approvedByAccountSection=True)
        if len(payslip) > 0:
            return "PaySlip exits for the requested year and month. Please check in your paySlip list."
        else:
            # Creating PaySlip For Employee
            payObject = Payslip()
            payObject.payslip_id = str(request.POST['start']) +'_'+str(request.session.get('EMPID'))
            payObject.slip_emp = empID
            payObject.payslip_ownerName = empID.first_name + ' ' + empID.last_name
            payObject.experience = empID.past_experience
            payObject.grade_of_employment = empID.grade_of_employment
            payObject.month = int(request.POST['start'].split('-')[1])
            payObject.year = int(request.POST['start'].split('-')[0])
            payObject.save()
            return "Request has been sent. Please wait."

    # For avoiding multiple generate
    def avoidMultipleGenerate(self,request, month, year, empID):
        payslip = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(approvedByAccountSection=None)
        payslip1 = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(
            approvedByAccountSection=True).filter(approvedByAssistRegistrar=None)
        payslip2 = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(
            approvedByAccountSection=True).filter(approvedByAssistRegistrar=True)
        if len(payslip) > 0:
            return "Your request is pending for approval from authority."
        elif len(payslip1) > 0:
            return "Pending from assistant registrar.Please wait."
        elif len(payslip2) > 0:
            return "Payslip exists for this month. Please check it in PaySlip list."

        else:
            # Creating PaySlip For Employee
            payObject = Payslip()
            payObject.payslip_id = str(request.POST['start']) +'_'+str(request.session.get('EMPID'))
            payObject.slip_emp = empID
            payObject.payslip_ownerName = empID.first_name + ' ' + empID.last_name
            payObject.experience = empID.past_experience
            payObject.grade_of_employment = empID.grade_of_employment
            payObject.month = int(request.POST['start'].split('-')[1])
            payObject.year = int(request.POST['start'].split('-')[0])
            payObject.save()
            return "Request has been sent. Please wait."

    def getpaySlip(self, payObject):
        emplist=[]
        emplist.append(payObject.payslip_id)
        emplist.append(payObject.payslip_ownerName)
        emplist.append(payObject.grade_of_employment)
        emplist.append(payObject.bonus_received)
        emplist.append(payObject.base_salary)
        emplist.append(payObject.total_salary)
        emplist.append(payObject.month)
        emplist.append(payObject.year)
        emplist.append(payObject.slip_gen_ar.assRegEmail)
        emplist.append(payObject.slip_gen.ccfs_id.emp_ID.emailID)
        return emplist


class StaffView(generic.FormView):
    template_name = 'authentication/staff.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.session['ROLE'] == 'STAFF':

                AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
                emp = Employee.objects.get(emp_ID=AuthObj)
                DeptObj = Staff.objects.get(staff_id=emp)
                return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'), 'Department':DeptObj.dept_ID.dept_name, 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})
        except Exception as e:
            print('Staff ', str(e))
            pass
        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):
        AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        emp = Employee.objects.get(emp_ID=AuthObj)
        emplist = []
        try:
            if request.POST['button'] == 'see':
                messageStatus = False
                print(request.POST)
                try:
                    payObject = Payslip.objects.get(
                        payslip_id=str(request.POST['start']) + '_' + str(request.session.get('EMPID')))
                    emplist = self.getpaySlip(payObject)
                except:
                    messageSee = 'Payslip does not exit. Please generate it.'
                    messageStatus = True

                return render(request, self.template_name,
                              {'messageStatus': messageStatus, 'messageSee': messageSee,
                               'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                               'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available, 'emplist': emplist})

            if request.POST['button'] == 'generate':
                messageforUserFlag = True
                messageforUser = self.avoidMultipleGenerate(request, int(request.POST['start'].split('-')[1]),int(request.POST['start'].split('-')[0]),emp)
                print('Button generate pressed', request.POST['start'])
                return render(request, self.template_name,
                              {'messageforUserFlag':messageforUserFlag,'messageforUser':messageforUser, 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                               'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available})

        except Exception as e:
            print('Wrong', str(e))
            pass
        return render(request, self.template_name,
                      {'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                       'first_name': emp.first_name, 'last_name': emp.last_name,
                       'leave_available': emp.leave_available})

    # check whether payslip already exists or not

    def checkPaySlip(self,request, month, year, empID):
        payslip = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(approvedByAccountSection=True)
        if len(payslip) > 0:
            return "PaySlip exits for the requested year and month. Please check in your paySlip list."
        else:
            payObject = Payslip()
            payObject.payslip_id = str(request.POST['start']) +'_'+str(request.session.get('EMPID'))
            payObject.slip_emp = empID
            payObject.payslip_ownerName = empID.first_name + ' ' + empID.last_name
            payObject.experience = empID.past_experience
            payObject.grade_of_employment = empID.grade_of_employment
            payObject.month = int(request.POST['start'].split('-')[1])
            payObject.year = int(request.POST['start'].split('-')[0])
            payObject.save()

            return "Request has been sent. Please wait."

    # For avoiding multiple generate

    def avoidMultipleGenerate(self, request, month, year, empID):
        payslip = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(
            approvedByAccountSection=None)
        payslip1 = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(
            approvedByAccountSection=True).filter(approvedByAssistRegistrar=None)
        payslip2 = Payslip.objects.filter(slip_emp=empID).filter(month=month).filter(year=year).filter(
            approvedByAccountSection=True).filter(approvedByAssistRegistrar=True)
        if len(payslip) > 0:
            return "Your request is pending for approval from authority."
        elif len(payslip1) > 0:
            return "Pending from assistant registrar.Please wait."
        elif len(payslip2) > 0:
            return "Payslip exists for this month. Please check it in PaySlip list."
        else:
            # Creating PaySlip For Employee
            payObject = Payslip()
            payObject.payslip_id = str(request.POST['start']) + '_' + str(request.session.get('EMPID'))
            payObject.slip_emp = empID
            payObject.payslip_ownerName = empID.first_name + ' ' + empID.last_name
            payObject.experience = empID.past_experience
            payObject.grade_of_employment = empID.grade_of_employment
            payObject.month = int(request.POST['start'].split('-')[1])
            payObject.year = int(request.POST['start'].split('-')[0])
            payObject.save()
            return "Request has been sent. Please wait."

    def getpaySlip(self, payObject):
        emplist=[]
        emplist.append(payObject.payslip_id)
        emplist.append(payObject.payslip_ownerName)
        emplist.append(payObject.grade_of_employment)
        emplist.append(payObject.bonus_received)
        emplist.append(payObject.base_salary)
        emplist.append(payObject.total_salary)
        emplist.append(payObject.month)
        emplist.append(payObject.year)
        emplist.append(payObject.slip_gen_ar.areg_ID)
        emplist.append(payObject.slip_gen.ccfs_id.emp_ID.emailID)
        return emplist



class AssistRegView(generic.FormView):
    template_name = 'authentication/assistReg.html'
    def get(self, request, *args, **kwargs):
        request.session['ISACCOUNT'] = False
        emplist = []
        # AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        # emp = Employee.objects.get(emp_ID=AuthObj)
        AregObj = AssistRegistrar.objects.get(assRegEmail= request.session.get('ROLEID'))
        print(AregObj.staff_id.dept_ID.dept_name)
        if AregObj.staff_id.dept_ID.dept_name == 'ACCOUNT':
            request.session['ISACCOUNT']=True
            try:
                emplist = self.getEmpPaylist()
                print('It is from get method', emplist)
            except Exception as e:
                print(str(e))
                print('No PaySlip generated by authority')
        try:
            if request.session['ROLE'] == 'ASSIST_REGISTRAR':
                AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
                emp = Employee.objects.get(emp_ID=AuthObj)
                # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
                return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'), 'Department':AregObj.staff_id.dept_ID.dept_name, 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available,'ISACCOUNT':request.session['ISACCOUNT'],'emplist':emplist})
        except Exception as e:
            print('CCFS ERROR: ' + str(e))
            pass
        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):
        AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        emp = Employee.objects.get(emp_ID=AuthObj)
        emplist = []
        messageStatus = False
        messageStatusSee = False
        seePayslipList = []
        try:
            print(request.POST['button'])
            if 'reject' in request.POST['button']:
                self.completePayslip(request.POST['button'][6:] , request.session.get('ROLEID'), False)
                print('Reject button pressed')
                try:
                    emplist = self.getEmpPaylist()
                except Exception as e:
                    print('POST',str(e))
            elif 'approve' in request.POST['button']:
                print('Start complete payslip', request.POST['button'][7:])
                self.completePayslip(request.POST['button'][7:],request.session.get('ROLEID'), True)
                print('Done complete payslip')
                try:
                    emplist = self.getEmpPaylist()
                except Exception as e:
                    print(str(e))

        except Exception as e:
            print('Wrong' , str(e))
            pass
        return render(request, self.template_name,
                      {'messageStatus':messageStatus, 'messageStatusSee':messageStatusSee, 'message':'your request sent', 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                       'first_name': emp.first_name, 'last_name': emp.last_name,
                       'leave_available': emp.leave_available, 'emplist':emplist, 'ISACCOUNT':request.session['ISACCOUNT']})

    def getEmpPaylist(self):
        emplist=[]
        try:
            payslips = Payslip.objects.filter(approvedByAccountSection=True).filter(approvedByAssistRegistrar=None)
            print(payslips)
            for slips in payslips.iterator():
                BaseSalary = Cfti.objects.filter(experience=slips.experience).get(grade=slips.grade_of_employment).baseSalary
                try:
                    BONUS = Calender.objects.filter(year=slips.year).get(month=slips.month).bonus
                    TotalSalary = BaseSalary + BaseSalary * (BONUS / 100)
                except:
                    BONUS = 0
                    TotalSalary = BaseSalary
                    pass
                emplist.append([slips.payslip_id, slips.slip_emp.emp_ID.emailID,
                                slips.slip_emp.first_name + ' ' + slips.slip_emp.last_name,
                                slips.experience, BaseSalary, BONUS, TotalSalary, slips.month, slips.year])

        except Exception as e:
            print(str(e) , 'Problem is here')
        return emplist

    def completePayslip(self,emailID, slip_gen_ID, approvedByAssistRegistrar):
        try:
            print(emailID)

            payslips = Payslip.objects.filter(payslip_id=emailID).filter(approvedByAccountSection=True).get(approvedByAssistRegistrar=None)
            payslips.approvedByAssistRegistrar = approvedByAssistRegistrar

            payslips.slip_gen_ar = AssistRegistrar.objects.get(assRegEmail = slip_gen_ID)
            print('Done')
            payslips.save()

            # PaperTrailslip object

            trailObj = paperTrailPayslip()
            trailObj.payslip_id = payslips.ID
            trailObj.date = datetime.date.today()
            trailObj.role = "ASSIST_REGISTRAR"
            # Storing the employee ID of the assistant registrar
            id = int(AssistRegistrar.objects.get(assRegEmail=slip_gen_ID).staff_id.staff_id.ID)
            trailObj.empIDGen = id
            if approvedByAssistRegistrar == True:
                trailObj.status = "APPROVED"
            else:
                trailObj.status = "REJECTED"
            # trailObj.status = approvedByAccountSection
            trailObj.save()
        except Exception as e:
            print('Something wrong here',str(e))


class DirectorView(generic.FormView):
    template_name = 'authentication/director.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DIRECTOR':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            # directorObj = Director.objects.get(dirEmail=email)
            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'),'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DIRECTOR':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)

            return render(request, self.template_name,
                          {'message':'your request sent', 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available,'ISACCOUNT':request.session['ISACCOUNT']})

        return redirect('authentication:logout')



class RegistrarView(generic.FormView):
    template_name = 'authentication/registrar.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'REGISTRAR':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            # directorObj = Director.objects.get(dirEmail=email)
            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'),'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'REGISTRAR':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)

            if request.POST['button'] == 'bonus':
                self.giveBonus(request.POST['start'].split('-')[1],request.POST['start'].split('-')[0],request.POST['bonusrate'])

            return render(request, self.template_name,
                          {'message':'your request sent', 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available})

        return redirect('authentication:logout')

    def giveBonus(self, month, year, bonus):
        print('month: ',month)
        print('year: ',year)
        print('bonus: ',bonus)

        try:
            CalObj = Calender.objects.filter(year=int(year)).get(month=month)
            CalObj.month = int(month)
            CalObj.year = int(year)
            CalObj.bonus = Decimal(bonus)
            CalObj.save()
        except Exception as e:
            print('Wrong in Bonus')
            CalObj2 = Calender()
            CalObj2.month = int(month)
            CalObj2.year = int(year)
            CalObj2.bonus = Decimal(bonus)
            CalObj2.save()

            pass



class HodView(generic.FormView):
    template_name = 'authentication/hod.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'HOD':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            Department = Hod.objects.get(hodEmail=request.session.get('ROLEID')).faculty_ID.dept_ID.dept_name

            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'), 'Department':Department ,'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'HOD':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            Department = Hod.objects.get(hodEmail=request.session.get('ROLEID')).faculty_ID.dept_ID.dept_name

            return render(request, self.template_name,
                          {'EMPNAME': request.session.get('ROLEID'), 'Department':Department, 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available})

        return redirect('authentication:logout')


class DfaView(generic.FormView):
    template_name = 'authentication/dfa.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DFA':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            # directorObj = Director.objects.get(dirEmail=email)
            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'),'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DFA':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)

            return render(request, self.template_name,
                          {'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available})

        return redirect('authentication:logout')


class AdfaView(generic.FormView):
    template_name = 'authentication/adfa.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'ADFA':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            # directorObj = Director.objects.get(dirEmail=email)
            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'),'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'ADFA':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)

            return render(request, self.template_name,
                          {'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available})

        return redirect('authentication:logout')


class DeptSecView(generic.FormView):
    template_name = 'authentication/deptsec.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DEPTSEC':
            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            # Department = Hod.objects.get(hodEmail=request.session.get('ROLEID')).faculty_ID.dept_ID.dept_name
            # directorObj = Director.objects.get(dirEmail=email)
            # emp = Employee.objects.get(emp_ID=request.session.get('EMPID'))
            return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'),'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available})

        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):

        if request.session.get('ROLE') == 'DEPTSEC':

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            Department = Hod.objects.get(hodEmail=request.session.get('ROLEID')).faculty_ID.dept_ID.dept_name

            return render(request, self.template_name,
                          {'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                           'first_name': emp.first_name, 'last_name': emp.last_name,
                           'leave_available': emp.leave_available})

        return redirect('authentication:logout')

