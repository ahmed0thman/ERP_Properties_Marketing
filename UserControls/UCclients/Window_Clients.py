from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import mysql.connector
import datetime
clientsUI,_ = loadUiType('./UserControls/UCclients/UC_clients.ui')

class window_clients(QFrame, clientsUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.db = namespace.db
        try:
            self.cur = self.db.cursor()
        except:
            pass
        self.Frame_Clients_Reports.setVisible(False)
        self.InitUi()
        self.Handle_Buttons()
        self.Fill_table_client()

    def InitUi(self):
        self.btn_clients_frame.clicked.connect(
            lambda: self.Swipe_Clients_frames(self.Frame_Clients_Info)
        )
        self.btn_clients_archieve_frame.clicked.connect(
            lambda: self.Swipe_Clients_frames(self.Frame_Clients_Reports)
        )

    def Swipe_Clients_frames(self, frame):
        if frame == self.Frame_Clients_Info:
            self.Frame_Clients_Info.setVisible(True)
            self.Frame_Clients_Reports.setVisible(False)
        else:
            self.Frame_Clients_Info.setVisible(False)
            self.Frame_Clients_Reports.setVisible(True)

    def Handle_Buttons(self):
        self.btn_add_client.clicked.connect(
            lambda: self.Add_Client()
        )
        self.btn_edit_client.clicked.connect(
            lambda: self.Edit_Client()
        )
        self.btn_remove_client.clicked.connect(
            lambda: self.Delete_Client()
        )

        self.tbl_client.cellClicked.connect(
            lambda: (
                self.btn_edit_client.setEnabled(True),
                self.btn_remove_client.setEnabled(True),
                self.chxOwners.setChecked(False),
                self.Fill_Text_client()
            )
        )

        self.txtClienSearch.textChanged.connect(
            lambda: self.Fill_table_client(self.txtClienSearch.text().strip().replace("'", ''))
        )

        self.chxOwners.stateChanged.connect(
            lambda: self.chxOwners_Toggled()
        )

        self.cbxOwners.currentIndexChanged.connect(
            lambda: self.Get_From_Owners(self.cbxOwners.currentIndex())
        )
    def Add_Client(self):
        try:
            Name = self.txtName.text().strip().replace("'", '')
            Phone1 = self.txtPhone1.text().strip().replace("'", '')
            if Name != '':
                if Phone1 != '':
                    Email = self.txtEmail.text().strip().replace("'", '')
                    Address = self.txtAddress.text().strip().replace("'", '')
                    Phone2 = self.txtPhone2.text().strip().replace("'", '')
                    clientowener = 'لا'
                    if self.chxOwners.isChecked():
                        clientowener = 'نعم'
                    if self.cbxOwners.currentIndex() >= 0:
                        self.cur.execute(f'''
                        update persons set is_client='نعم'
                        where phone1='{Phone1}' 
                    ''')
                    else:
                        self.cur.execute(f'''
                            insert into persons(name, phone1 , phone2 , address , email, is_client  ,is_owner) values
                        ('{Name}','{Phone1}','{Phone2}','{Address}','{Email}', 'نعم' ,'{clientowener}')
                        ''')
                    self.cur.execute(f'''
                            insert into employee_actions (emp_id, date_time, action_type, target)
                            values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'اضاف عميل', '{Phone1}')
                        ''')
                    self.db.commit()
                    self.cbxOwners.clear()
                    self.txtName.setText('')
                    self.txtPhone1.setText('')
                    self.txtEmail.setText('')
                    self.txtAddress.setText('')
                    self.txtPhone2.setText('')
                    self.chxOwners.setChecked(False)
                    self.txtName.setFocus()
                    self.Fill_table_client()
                    self.btn_edit_client.setEnabled(False)
                    self.btn_remove_client.setEnabled(False)
                    self.namespace.Handle_Status('تم اضافة عميل', 1)

                else:
                    self.txtPhone1.setFocus()
                    self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)
            else:
                self.txtName.setFocus()
                self.namespace.Handle_Status('أدخل إسم العميل', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Edit_Client(self):
        try:
            Name = self.txtName.text().strip().replace("'", '')
            Phone1 = self.txtPhone1.text().strip().replace("'", '')
            if Name != '':
                if Phone1 != '':
                    Email = self.txtEmail.text().strip().replace("'", '')
                    Address = self.txtAddress.text().strip().replace("'", '')
                    Phone2 = self.txtPhone2.text().strip().replace("'", '')
                    clientowener = 'لا'
                    if self.chxOwners.isChecked():
                        clientowener = 'نعم'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                                   update persons set name='{Name}', phone1='{Phone1}' , phone2='{Phone2}',
                                   address='{Address}' , email='{Email}'  ,  is_owner='{clientowener}'
                                   where phone1='{Phone1}' and is_owner = 'نعم' 
                               ''')
                        self.cur.execute(f'''
                            insert into employee_actions (emp_id, date_time, action_type, target)
                            values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'تعديل عميل', '{Phone1}')
                        ''')
                        self.db.commit()
                        self.txtName.setText('')
                        self.txtPhone1.setText('')
                        self.txtEmail.setText('')
                        self.txtAddress.setText('')
                        self.txtPhone2.setText('')
                        self.chxOwners.setChecked(False)
                        self.cbxOwners.clear()
                        self.txtName.setFocus()
                        self.Fill_table_client()
                        self.btn_edit_client.setEnabled(False)
                        self.btn_remove_client.setEnabled(False)
                        self.namespace.Handle_Status('تم تعديل العميل', 1)

                else:
                    self.txtPhone1.setFocus()
                    self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)
            else:
                self.txtOwnerName.setFocus()
                self.namespace.Handle_Status('أدخل إسم العميل', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Delete_Client(self):
        try:
            Phone1 = self.txtPhone1.text().strip().replace("'", '')
            if Phone1 != '':
                msgbx = QMessageBox.warning(
                    self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                if msgbx == QMessageBox.Yes:
                    self.cur.execute(f'''
                        update persons set is_client='لا'
                        where phone1='{Phone1}' 
                    ''')
                    self.cur.execute(f'''
                            insert into employee_actions (emp_id, date_time, action_type, target)
                            values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'حذف عميل', '{Phone1}')
                        ''')
                    self.db.commit()
                    self.txtName.setText('')
                    self.txtPhone1.setText('')
                    self.txtEmail.setText('')
                    self.txtAddress.setText('')
                    self.txtPhone2.setText('')
                    self.chxOwners.setChecked(False)
                    self.cbxOwners.clear()
                    self.txtName.setFocus()
                    self.Fill_table_client()
                    self.btn_edit_client.setEnabled(False)
                    self.btn_remove_client.setEnabled(False)
                    self.namespace.Handle_Status('تم حذف عميل', 1)

            else:
                self.txtPhone1.setFocus()
                self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_table_client(self, name=''):
        try:
            nameFlter = ''
            if name != '':
                nameFlter = f"and name like'{name}%'"
            self.cur.execute(f'''
            select name, phone1, phone2, address, email, is_owner  from persons
            where is_client='نعم' {nameFlter}
            ''')
            tblclients = self.cur.fetchall()
            self.tbl_client.setRowCount(0)
            if len(tblclients) != 0:
                self.tbl_client.insertRow(0)
                for rownum, row in enumerate(tblclients):
                    for colnum, col in enumerate(row):
                        self.tbl_client.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_client.rowCount()
                    if rowPosition == len(tblclients):
                        break
                    self.tbl_client.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_Text_client(self):
        rowData = self.tbl_client.selectedIndexes()
        self.txtName.setText(rowData[0].data())
        self.txtPhone1.setText(str(rowData[1].data()))
        self.txtPhone2.setText(str(rowData[2].data()))
        self.txtAddress.setText(str(rowData[3].data()))
        self.txtEmail.setText(str(rowData[4].data()))


    def Fill_CbxOwners(self):
        try:
            self.cur.execute('''
                select name, phone1, phone2, address, email from persons
                where is_client='لا' and is_owner = 'نعم'
            ''')
            self.ownersInfo = self.cur.fetchall()
            self.cbxOwners.clear()
            self.cbxOwners.setCurrentIndex(-1)
            for owner in self.ownersInfo:
                self.cbxOwners.addItem(owner[0])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def chxOwners_Toggled(self):
        if self.chxOwners.isChecked():
            self.Fill_CbxOwners()
        else:
            self.cbxOwners.clear()
            self.txtName.setText('')
            self.txtPhone1.setText('')
            self.txtEmail.setText('')
            self.txtAddress.setText('')
            self.txtPhone2.setText('')
            
    def Get_From_Owners(self, owner):
        self.txtName.setText(self.ownersInfo[owner][0])
        self.txtPhone1.setText(self.ownersInfo[owner][1])
        self.txtPhone2.setText(self.ownersInfo[owner][2])
        self.txtAddress.setText(self.ownersInfo[owner][3])
        self.txtEmail.setText(self.ownersInfo[owner][4])



