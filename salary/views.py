import datetime
from django.shortcuts import render, redirect
from django.views import generic
from authentication.models import Ccfs, AssistRegistrar, AuthTable
from salary.models import Payslip, Cfti, Calender, paperTrailPayslip
from authentication.models import Employee
from decimal import Decimal


# Function for updating the value in the paperTrailPaySlip Table in database
def updateValue(payslip_id,comment,role, empIDGen,status):
    obj = paperTrailPayslip()
    obj.payslip_id = payslip_id
    obj.comment = comment
    obj.role = role
    obj.empIDGen = empIDGen
    obj.status = status
    obj.save()



class CcfsView(generic.TemplateView):
    template_name = 'salary/ccfs.html'

    def get(self, request, *args, **kwargs):
        request.session['ISACCOUNT'] = False
        emplist = []

        AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        emp = Employee.objects.get(emp_ID=AuthObj)

        DeptObj = Ccfs.objects.get(ccfs_id=emp)

        if DeptObj.dept_ID.dept_name == 'ACCOUNT':
            request.session['ISACCOUNT']=True
            try:
                emplist = self.getEmpPaylist()
                print('It is from get method', emplist)
            except Exception as e:
                print(str(e))
                print('No PaySlip generated by authority')
        try:
            if request.session['ROLE'] == 'CCFS':
                AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
                emp = Employee.objects.get(emp_ID=AuthObj)
                DeptObj = Ccfs.objects.get(ccfs_id=emp)
                return render(request, self.template_name, {'EMPNAME':request.session.get('ROLEID'), 'Department':DeptObj.dept_ID.dept_name, 'role':request.session.get('ROLE'), 'first_name':emp.first_name, 'last_name':emp.last_name, 'leave_available':emp.leave_available,'ISACCOUNT':request.session['ISACCOUNT'],'emplist':emplist})

        except Exception as e:
            print('CCFS ERROR: ' + str(e))
            pass
        return redirect('authentication:logout')

    def post(self, request, *args, **kwargs):
        AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
        emp = Employee.objects.get(emp_ID=AuthObj)
        DeptObj = Ccfs.objects.get(ccfs_id=emp)
        emplist = []
        messageStatus = False
        messageStatusSee = False
        seePayslipList = []
        try:
            print(request.POST['button'])
            if 'reject' in request.POST['button']:
                self.completePayslip(request, request.POST['button'][6:] , request.session.get('ROLEID'), False)
                print('Reject button pressed')
                try:
                    emplist = self.getEmpPaylist()
                except Exception as e:
                    print('POST',str(e))
            elif 'approve' in request.POST['button']:
                print('Start complete payslip', request.POST['button'][7:])
                self.completePayslip(request,request.POST['button'][7:],request.session.get('ROLEID'), True)
                print('Done complete payslip')
                try:
                    emplist = self.getEmpPaylist()
                except Exception as e:
                    print(str(e))

            elif request.POST['button'] == 'see':
                messageStatus = False
                messageStatusSee = False
                print(request.POST)
                try:
                    print('emplist Hola')
                    payObject = Payslip.objects.get(payslip_id=str(request.POST['start']) +'_'+str(request.session.get('EMPID')))
                    print(payObject)
                    emplist = self.getpaySlip(payObject)
                    print('emplist ', emplist)
                    messageStatusSee = True
                    messageSee = ''
                except:
                    # If payslip not exit in table
                    messageSee = 'Payslip does not exit. Please generate it.'
                    messageStatus = True

                return render(request, self.template_name,
                              {'messageStatus':messageStatus,'messageStatusSee':messageStatusSee,'messageSee':messageSee,
                               'Department':DeptObj.dept_ID.dept_name, 'EMPNAME': request.session.get('ROLEID'),
                               'role': request.session.get('ROLE'),'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available, 'emplist':emplist,'ISACCOUNT':request.session['ISACCOUNT']})


            elif request.POST['button'] == 'generate':
                messageforUserFlag = True
                messageforUser = self.avoidMultipleGenerate(request, int(request.POST['start'].split('-')[1]),int(request.POST['start'].split('-')[0]),emp)
                print('Button generate pressed', request.POST['start'])
                return render(request, self.template_name,
                              {'messageforUserFlag':messageforUserFlag,'messageforUser':messageforUser, 'Department':DeptObj.dept_ID.dept_name, 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                               'first_name': emp.first_name, 'last_name': emp.last_name,
                               'leave_available': emp.leave_available,'ISACCOUNT':request.session['ISACCOUNT']})

        except Exception as e:
            print('Wrong' , str(e))
            pass
        return render(request, self.template_name,
                      {'messageStatus':messageStatus, 'messageStatusSee':messageStatusSee, 'message':'your request sent', 'Department':DeptObj.dept_ID.dept_name, 'EMPNAME': request.session.get('ROLEID'), 'role': request.session.get('ROLE'),
                       'first_name': emp.first_name, 'last_name': emp.last_name,
                       'leave_available': emp.leave_available, 'emplist':emplist, 'ISACCOUNT':request.session['ISACCOUNT'], 'seePayslipList':seePayslipList })


    def getpaySlip(self, payObject):
        emplist=[]
        emplist.append(payObject.payslip_id)
        emplist.append(payObject.payslip_ownerName)
        emplist.append(payObject.grade_of_employment)
        emplist.append(str(payObject.bonus_received))
        emplist.append(str(payObject.base_salary))
        emplist.append(str(payObject.total_salary))
        emplist.append(str(payObject.month))
        emplist.append(str(payObject.year))
        emplist.append(payObject.slip_gen_ar.assRegEmail)
        emplist.append(payObject.slip_gen.ccfs_id.emp_ID.emailID)
        return emplist


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
        elif len(payslip2)>0:
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

    def seePayslip(self, payslipID):
        payslips = Payslip.objects.filter(payslip_id=payslipID).filter(approvedByAccountSection=True).get(approvedByAssistRegistrar=True)
        paysliplist = []
        paysliplist.append(payslips.payslip_id)
        paysliplist.append(payslips.slip_emp.emp_ID)
        paysliplist.append(payslips.payslip_ownerName)
        paysliplist.append(payslips.experience)
        paysliplist.append(payslips.salary)
        paysliplist.append(payslips.bonus_received)
        paysliplist.append(payslips.salary + payslips.bonus_received)
        paysliplist.append(payslips.month)
        paysliplist.append(payslips.year)
        paysliplist.append(payslips.slip_gen.staff_id.emp_ID)
        # paysliplist.append(payslips.slip_gen_ar.areg_ID)

        return paysliplist




    def getEmpPaylist(self):
        emplist=[]
        try:
            payslips = Payslip.objects.filter(approvedByAccountSection=None)
            for slips in payslips.iterator():
                BaseSalary = Cfti.objects.filter(experience=slips.experience).get(grade=slips.grade_of_employment).baseSalary
                try:
                    BONUS = Calender.objects.filter(year=slips.year).get(month=slips.month).bonus
                    TotalSalary = BaseSalary + BaseSalary * (BONUS / 100)
                except:
                    BONUS = 0
                    TotalSalary = BaseSalary
                    pass
                emplist.append([str(slips.payslip_id), str(slips.slip_emp.emp_ID.emailID),
                                slips.slip_emp.first_name + ' ' + slips.slip_emp.last_name,
                                str(slips.experience), str(BaseSalary), str(BONUS), str(TotalSalary), str(slips.month), str(slips.year)])
        except Exception as e:
            print(str(e) , 'Problem is here')
        return emplist


    def completePayslip(self,request, emailID,slip_gen_ID, approvedByAccountSection):
        try:

            payslips = Payslip.objects.filter(payslip_id=emailID).get(approvedByAccountSection=None)

            AuthObj = AuthTable.objects.get(emailID=request.session.get('EMPID'))
            emp = Employee.objects.get(emp_ID=AuthObj)
            Generator = Ccfs.objects.get(ccfs_id=emp)

            print(payslips, payslips.experience , payslips.grade_of_employment)

            BaseSalary = Cfti.objects.filter(experience=payslips.experience).get(grade= payslips.grade_of_employment).baseSalary
            try:
                BONUS = Calender.objects.filter(year=payslips.year).get(month=payslips.month).bonus
                TotalSalary = BaseSalary + BaseSalary * (BONUS / 100)
            except Exception as e1:
                BONUS = 0
                TotalSalary = BaseSalary
                # print('Bonus',str(e1))
                pass
            payslips.approvedByAccountSection = approvedByAccountSection
            payslips.base_salary = BaseSalary
            payslips.slip_gen = Generator
            payslips.total_salary = Decimal(TotalSalary)
            payslips.bonus_received = Decimal(float(BaseSalary) * (BONUS / 100.0))
            payslips.date_of_generation = datetime.date.today()
            payslips.save()

            # Object of PaperTrailPaySlip
            trailObj = paperTrailPayslip()
            trailObj.payslip_id = payslips.ID
            trailObj.date = datetime.date.today()
            trailObj.role = "CCFS"
            trailObj.empIDGen = Generator.ccfs_id.ID
            if approvedByAccountSection==True:
                trailObj.status = "APPROVED"
            else:
                trailObj.status = "REJECTED"
            trailObj.save()
        except Exception as e:
            print('Something wrong here',str(e))