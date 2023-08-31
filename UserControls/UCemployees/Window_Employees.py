from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import mysql.connector
import datetime
import xlsxwriter
employeesUI,_ = loadUiType('./UserControls/UCemployees/UC_Employees.ui')

class window_employees(QFrame, employeesUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.db = namespace.db
        try:
            self.cur = self.db.cursor()
        except:
            pass
        self.Frame_Employees_Reports.setVisible(False)
        self.InitUi()
        self.Handle_Events()
        self.Fill_Table_Emps()

    def InitUi(self):
        self.btn_employees_frame.clicked.connect(
            lambda: self.Swipe_Owners_frames(self.Frame_Employees_Info)
        )
        self.btn_employees_archieve_frame.clicked.connect(
            lambda: self.Swipe_Owners_frames(self.Frame_Employees_Reports)
        )

    def Swipe_Owners_frames(self, frame):
        if frame == self.Frame_Employees_Info:
            self.Frame_Employees_Info.setVisible(True)
            self.Frame_Employees_Reports.setVisible(False)
        else:
            self.Frame_Employees_Info.setVisible(False)
            self.Frame_Employees_Reports.setVisible(True)

    def Handle_Events(self):
        self.btn_add_employee.clicked.connect(
            lambda: self.Add_Employee()
        )
        self.btn_edit_employee.clicked.connect(
            lambda: self.Edit_Employee()
        )
        self.btn_remove_employee.clicked.connect(
            lambda: self.Delete_Employee()
        )

        self.tbl_emp_info.cellClicked.connect(
            lambda: (
                self.btn_edit_employee.setEnabled(True),
                self.btn_remove_employee.setEnabled(True),
                self.Fill_Text_Emps()
            )
        )

        self.Fill_CbxEmp()

        self.btn_action_search.clicked.connect(
            lambda: self.Get_Actions_Info()
        )
        self.cbxEmp.currentIndexChanged.connect(
            lambda: (
                self.cbxActionTypes.setEnabled(True) if self.cbxEmp.currentIndex() > 0
                else self.cbxActionTypes.setEnabled(False), self.cbxActionTypes.setCurrentIndex(0)
            )
        )
        self.btn_print.clicked.connect(
            lambda: self.Print_Actions_Info()
        )
    # -------------------------------------
    # Employee info Events
    def Add_Employee(self):
        try:
            empID = self.txtEmpID.text().strip().replace("'", '')
            empName = self.txtEmpName.text().strip().replace("'", '')
            empPhone = self.txtEmpPhone.text().strip().replace("'", '')
            empSalary = self.txtEmpSalary.text().strip().replace("'", '')
            if empID != '':
                if empName != '':
                    if empPhone != '':
                        if empSalary != '':
                            empMail = self.txtEmpMail.text().strip().replace("'", '')
                            empAddress = self.txtEmpAddress.text().strip().replace("'", '')
                            empStartDate = str(self.dtEmpStartWork.date().toPyDate())
                            empDep = self.cbxEmpDep.currentText()
                            self.cur.execute(f'''
                                insert into employee(ID_Num, name, phone, email, address, department , salary, start_date,working)
                                 values ('{empID}', '{empName}', '{empPhone}', '{empMail}', '{empAddress}', '{empDep}', '{empSalary}', '{empStartDate}', 'yes')
                            ''')
                            self.db.commit()
                            self.txtEmpID.setText('')
                            self.txtEmpName.setText('')
                            self.txtEmpPhone.setText('')
                            self.txtEmpSalary.setText('')
                            self.txtEmpMail.setText('')
                            self.txtEmpAddress.setText('')
                            self.cbxEmpDep.setCurrentIndex(-1)
                            self.dtEmpStartWork.setDate(QDate(datetime.date.today()))
                            self.txtEmpID.setFocus()
                            self.Fill_Table_Emps()
                            self.btn_edit_employee.setEnabled(False)
                            self.btn_remove_employee.setEnabled(False)
                            self.namespace.Handle_Status('تم اضافة موظف', 1)
                        else:
                            self.txtEmpSalary.setFocus()
                            self.namespace.Handle_Status('أدخل الراتب', 3)
                    else:
                        self.txtEmpPhone.setFocus()
                        self.namespace.Handle_Status('أدخل رقم الهاتف', 3)
                else:
                    self.txtEmpName.setFocus()
                    self.namespace.Handle_Status('أدخل إسم الموظف', 3)
            else:
                self.txtEmpID.setFocus()
                self.namespace.Handle_Status('أدخل الرقم القومى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Employee(self):
        try:
            empID = self.txtEmpID.text().strip().replace("'", '')
            empName = self.txtEmpName.text().strip().replace("'", '')
            empPhone = self.txtEmpPhone.text().strip().replace("'", '')
            empSalary = self.txtEmpSalary.text().strip().replace("'", '')
            if empID != '':
                if empName != '':
                    if empPhone != '':
                        if empSalary != '':
                            empMail = self.txtEmpMail.text().strip().replace("'", '')
                            empAddress = self.txtEmpAddress.text().strip().replace("'", '')
                            empStartDate = str(self.dtEmpStartWork.date().toPyDate())
                            empDep = self.cbxEmpDep.currentText()
                            msgbx = QMessageBox.warning(
                                self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                                )
                            if msgbx == QMessageBox.Yes:
                                self.cur.execute(f'''
                                update employee set name='{empName}', phone='{empPhone}', email='{empMail}',
                                address='{empAddress}', department='{empDep}' , salary='{empSalary}', start_date='{empStartDate}'
                                where ID_Num='{empID}'
                                ''')
                                self.db.commit()
                                self.txtEmpID.setText('')
                                self.txtEmpName.setText('')
                                self.txtEmpPhone.setText('')
                                self.txtEmpSalary.setText('')
                                self.txtEmpMail.setText('')
                                self.txtEmpAddress.setText('')
                                self.cbxEmpDep.setCurrentIndex(-1)
                                self.dtEmpStartWork.setDate(QDate(datetime.date.today()))
                                self.txtEmpID.setFocus()
                                self.Fill_Table_Emps()
                                self.btn_edit_employee.setEnabled(False)
                                self.btn_remove_employee.setEnabled(False)
                                self.namespace.Handle_Status('تم تعديل موظف', 1)
                        else:
                            self.txtEmpSalary.setFocus()
                            self.namespace.Handle_Status('أدخل الراتب', 3)
                    else:
                        self.txtEmpPhone.setFocus()
                        self.namespace.Handle_Status('أدخل رقم الهاتف', 3)
                else:
                    self.txtEmpName.setFocus()
                    self.namespace.Handle_Status('أدخل إسم الموظف', 3)
            else:
                self.txtEmpID.setFocus()
                self.namespace.Handle_Status('أدخل الرقم القومى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Employee(self):
        try:
            empID = self.txtEmpID.text().strip().replace("'", '')
            if empID != '':
                msgbx = QMessageBox.warning(
                    self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                if msgbx == QMessageBox.Yes:
                    self.cur.execute(f'''
                    update employee set working='no'
                    where ID_Num='{empID}'
                    ''')
                    self.db.commit()
                    self.txtEmpID.setText('')
                    self.txtEmpName.setText('')
                    self.txtEmpPhone.setText('')
                    self.txtEmpSalary.setText('')
                    self.txtEmpMail.setText('')
                    self.txtEmpAddress.setText('')
                    self.cbxEmpDep.setCurrentIndex(-1)
                    self.dtEmpStartWork.setDate(QDate(datetime.date.today()))
                    self.txtEmpID.setFocus()
                    self.Fill_Table_Emps()
                    self.btn_edit_employee.setEnabled(False)
                    self.btn_remove_employee.setEnabled(False)
                    self.namespace.Handle_Status('تم حذف موظف', 1)
            else:
                self.txtEmpID.setFocus()
                self.namespace.Handle_Status('أدخل الرقم القومى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Table_Emps(self):
        try:
            self.cur.execute('''
            select ID_Num, name, phone, email, address, department , salary, start_date  from employee
            where working='yes'
            ''')
            tblEmps = self.cur.fetchall()
            self.tbl_emp_info.setRowCount(0)
            if len(tblEmps) != 0:
                self.tbl_emp_info.insertRow(0)
                for rownum, row in enumerate(tblEmps):
                    for colnum, col in enumerate(row):
                        self.tbl_emp_info.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_emp_info.rowCount()
                    if rowPosition == len(tblEmps):
                        break
                    self.tbl_emp_info.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Text_Emps(self):
        rowData = self.tbl_emp_info.selectedIndexes()
        self.txtEmpID.setText(str(rowData[0].data()))
        self.txtEmpName.setText(rowData[1].data())
        self.txtEmpPhone.setText(str(rowData[2].data()))
        self.txtEmpMail.setText(str(rowData[3].data()))
        self.txtEmpAddress.setText(str(rowData[4].data()))
        self.cbxEmpDep.setCurrentText(str(rowData[5].data()))
        self.txtEmpSalary.setText(str(rowData[6].data()))
        self.dtEmpStartWork.setDate(QDate.fromString(rowData[7].data(), 'yyyy-MM-dd'))


    # -------------------------------------
    # Employee Actions Archieve Events

    def Get_Actions_Info(self):
        try:
            empFilter = ''
            if self.cbxEmp.currentIndex() > 0:
                empFilter = f"where employee.name = '{self.cbxEmp.currentText()}'"
            actionFilter = ''
            if self.cbxActionTypes.currentIndex() > 0:
                actionFilter = f" and employee_actions.action_type like'%{self.cbxActionTypes.currentText().strip()}%'"
            self.cur.execute(f'''
            select employee_actions.emp_id,employee.name, employee_actions.action_type, employee_actions.date_time,
            employee_actions.target from employee_actions
            join employee on employee.ID_Num = employee_actions.emp_id 
            {empFilter} {actionFilter}
            ''')
            tblEmpActions = self.cur.fetchall()
            self.tblEmpActions.setRowCount(0)
            if len(tblEmpActions) != 0:
                self.tblEmpActions.insertRow(0)
                for rownum, row in enumerate(tblEmpActions):
                    for colnum, col in enumerate(row):
                        self.tblEmpActions.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tblEmpActions.rowCount()
                    if rowPosition == len(tblEmpActions):
                        break
                    self.tblEmpActions.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxEmp(self):
        try:
            self.cur.execute('''
            select ID_Num, name  from employee
            ''')
            self.tblEmps = self.cur.fetchall()
            self.cbxEmp.addItem('- - - - - - -')
            for emp in self.tblEmps:
                self.cbxEmp.addItem(str(emp[1]))
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Print_Actions_Info(self):
        try:
            empFilter = ''
            if self.cbxEmp.currentIndex() > 0:
                empFilter = f"where employee.name = '{self.cbxEmp.currentText()}'"
            actionFilter = ''
            if self.cbxActionTypes.currentIndex() > 0:
                actionFilter = f" and employee_actions.action_type like'%{self.cbxActionTypes.currentText().strip()}%'"
            self.cur.execute(f'''
            select employee_actions.emp_id,employee.name, employee_actions.action_type, employee_actions.date_time,
            employee_actions.target from employee_actions
            join employee on employee.ID_Num = employee_actions.emp_id 
            {empFilter} {actionFilter}
            ''')
            tblEmpActions = self.cur.fetchall()

            try:
                fileName = QFileDialog.getSaveFileName(self, 'save', 'report.xlsx.xlsx', '.xlsx')
                wb = xlsxwriter.Workbook(fileName[0])
                sheet1 = wb.add_worksheet()
                #sheet1.insert_image('A4', 'pics/logo1.png', {'x_scale': 1, 'y_scale': 1})
                sheet1.write(9,0,'التسلسلى ')
                sheet1.write(9,1,'الرقم القومى')
                sheet1.write(9,2,'الإسم')
                sheet1.write(9,3,'نوع النشاط')
                sheet1.write(9,4,'التاريخ')
                sheet1.write(9,5,'التفاصيل')
                row_number = 10
                m = 1
                for row in tblEmpActions:
                    column = 0
                    sheet1.write(row_number,column,m)
                    m += 1
                    column += 1
                    for item in row:
                        sheet1.write(row_number,column,str(item))
                        column += 1
                    row_number += 1
                sheet1.add_table(f'A10:F{row_number}', {
                    'columns': [
                        {'header': 'التسلسلى'},
                        {'header': 'الرقم القومى'},
                        {'header': 'رقم الطلبالإسم'},
                        {'header': 'نوع النشاط'},
                        {'header': 'التاريخ'},
                        {'header': 'التفاصيل'},
                        ]
                    })
                wb.close()
                self.namespace.Handle_Status('تم طباعة التقرير', 1)

            except Exception as er:
                QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)
