from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import datetime
import mysql.connector
ownersUI,_ = loadUiType('./UserControls/UCowners/UC_Owners.ui')

class window_owners(QFrame, ownersUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.db = namespace.db
        try:
            self.cur = self.db.cursor()
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        self.Frame_Owners_Reports.setVisible(False)
        self.InitUi()
        self.Handle_Events()
        self.Fill_Table_Owners()

    def InitUi(self):
        self.btn_owners_frame.clicked.connect(
            lambda: self.Swipe_Owners_frames(self.Frame_Owners_Info)
        )
        self.btn_owners_archieve_frame.clicked.connect(
            lambda: self.Swipe_Owners_frames(self.Frame_Owners_Reports)
        )

    def Swipe_Owners_frames(self, frame):
        if frame == self.Frame_Owners_Info:
            self.Frame_Owners_Info.setVisible(True)
            self.Frame_Owners_Reports.setVisible(False)
        else:
            self.Frame_Owners_Info.setVisible(False)
            self.Frame_Owners_Reports.setVisible(True)

    def Handle_Events(self):
        self.btn_add_owner.clicked.connect(
            lambda: self.Add_Owner()
        )
        self.btn_edit_owner.clicked.connect(
            lambda: self.Edit_Owner()
        )
        self.btn_remove_owner.clicked.connect(
            lambda: self.Delete_Owner()
        )

        self.tbl_owners_info.cellClicked.connect(
            lambda: (
                self.btn_edit_owner.setEnabled(True),
                self.btn_remove_owner.setEnabled(True),
                self.chkbxIsClient.setChecked(False),
                self.Fill_Text_Owners(),

            )
        )

        self.txtOwnerSearch.textChanged.connect(
            lambda: self.Fill_Table_Owners(self.txtOwnerSearch.text().strip().replace("'",''))
        )
        self.chkbxIsClient.stateChanged.connect(
            lambda: self.chxClients_Toggled()
        )

        self.cbxClientsNames.currentIndexChanged.connect(
            lambda: (
                self.Get_From_Clients(self.cbxClientsNames.currentIndex())
            )
        )

    # -------------------------------------
    # Owners info Events
    def Add_Owner(self):
        try:
            ownerName = self.txtOwnerName.text().strip().replace("'", '')
            ownerPhone1 = self.txtOwnerPhone1.text().strip().replace("'", '')
            if ownerName != '':
                if ownerPhone1 != '':
                    ownerMail = self.txtOwnerMail.text().strip().replace("'", '')
                    ownerAddress = self.txtOwnerAddress.text().strip().replace("'", '')
                    ownerPhone2 = self.txtOwnerPhone2.text().strip().replace("'", '')
                    ownerTrader = 'لا'
                    ownerClient = 'لا'
                    if self.chkbxIsTrader.isChecked():
                        ownerTrader = 'نعم'
                    if self.chkbxIsClient.isChecked():
                        ownerClient = 'نعم'
                    if self.cbxClientsNames.currentIndex() >= 0:
                        self.cur.execute(f'''
                        update persons set is_owner='نعم'
                        where phone1='{ownerPhone1}' 
                    ''')
                    else:
                        self.cur.execute(f'''
                            insert into persons(name, phone1 , phone2 , address , email  , is_trader ,is_owner is_client) values
            ('{ownerName}','{ownerPhone1}','{ownerPhone2}','{ownerAddress}','{ownerMail}','{ownerTrader}','نعم', '{ownerClient}')
                        ''')
                    self.cur.execute(f'''
                        insert into employee_actions (emp_id, date_time, action_type, target)
                        values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'أضاف مالك', '{ownerPhone1}')
                    ''')
                    self.db.commit()
                    self.txtOwnerName.setText('')
                    self.txtOwnerPhone1.setText('')
                    self.txtOwnerMail.setText('')
                    self.txtOwnerAddress.setText('')
                    self.txtOwnerPhone2.setText('')
                    self.chkbxIsTrader.setChecked(False)
                    self.chkbxIsClient.setChecked(False)
                    self.cbxClientsNames.setCurrentIndex(-1)
                    self.cbxClientsNames.setEnabled(False)
                    self.txtOwnerName.setFocus()
                    self.Fill_Table_Owners()
                    self.btn_edit_owner.setEnabled(False)
                    self.btn_remove_owner.setEnabled(False)
                    self.namespace.Handle_Status('تم اضافة موظف', 1)

                else:
                    self.txtOwnerPhone1.setFocus()
                    self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)
            else:
                self.txtOwnerName.setFocus()
                self.namespace.Handle_Status('أدخل إسم المالك', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Owner(self):
        try:
            ownerName = self.txtOwnerName.text().strip().replace("'", '')
            ownerPhone1 = self.txtOwnerPhone1.text().strip().replace("'", '')
            if ownerName != '':
                if ownerPhone1 != '':
                    ownerMail = self.txtOwnerMail.text().strip().replace("'", '')
                    ownerAddress = self.txtOwnerAddress.text().strip().replace("'", '')
                    ownerPhone2 = self.txtOwnerPhone2.text().strip().replace("'", '')
                    ownerTrader = 'لا'
                    ownerClient = 'لا'
                    if self.chkbxIsTrader.isChecked():
                        ownerTrader = 'نعم'
                    if self.chkbxIsClient.isChecked():
                        ownerClient = 'نعم'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                            update persons set name='{ownerName}', phone1='{ownerPhone1}' , phone2='{ownerPhone2}',
                            address='{ownerAddress}' , email='{ownerMail}'  , is_trader='{ownerTrader}' , is_client='{ownerClient}'
                            where phone1='{ownerPhone1}' and is_client = 'نعم'
                        ''')
                        self.cur.execute(f'''
                        insert into employee_actions (emp_id, date_time, action_type, target)
                        values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'تعديل مالك', '{ownerPhone1}')
                    ''')
                        self.db.commit()
                        self.txtOwnerName.setText('')
                        self.txtOwnerPhone1.setText('')
                        self.txtOwnerMail.setText('')
                        self.txtOwnerAddress.setText('')
                        self.txtOwnerPhone2.setText('')
                        self.chkbxIsTrader.setChecked(False)
                        self.chkbxIsClient.setChecked(False)
                        self.cbxClientsNames.setCurrentIndex(-1)
                        self.cbxClientsNames.setEnabled(False)
                        self.txtOwnerName.setFocus()
                        self.Fill_Table_Owners()
                        self.btn_edit_owner.setEnabled(False)
                        self.btn_remove_owner.setEnabled(False)
                        self.namespace.Handle_Status('تم تعديل موظف', 1)

                else:
                    self.txtOwnerPhone1.setFocus()
                    self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)
            else:
                self.txtOwnerName.setFocus()
                self.namespace.Handle_Status('أدخل إسم المالك', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Owner(self):
        try:
            ownerPhone1 = self.txtOwnerPhone1.text().strip().replace("'", '')
            if ownerPhone1 != '':
                msgbx = QMessageBox.warning(
                    self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                if msgbx == QMessageBox.Yes:
                    self.cur.execute(f'''
                        update persons set is_owner='لا'
                        where phone1='{ownerPhone1}' 
                    ''')
                    self.cur.execute(f'''
                            insert into employee_actions (emp_id, date_time, action_type, target)
                            values('{self.namespace.currentEmployee}', '{datetime.datetime.today()}', 'حذف مالك', '{ownerPhone1}')
                        ''')
                    self.db.commit()
                    self.txtOwnerName.setText('')
                    self.txtOwnerPhone1.setText('')
                    self.txtOwnerMail.setText('')
                    self.txtOwnerAddress.setText('')
                    self.txtOwnerPhone2.setText('')
                    self.chkbxIsTrader.setChecked(False)
                    self.chkbxIsClient.setChecked(False)
                    self.cbxClientsNames.setCurrentIndex(-1)
                    self.cbxClientsNames.setEnabled(False)
                    self.txtOwnerName.setFocus()
                    self.Fill_Table_Owners()
                    self.btn_edit_owner.setEnabled(False)
                    self.btn_remove_owner.setEnabled(False)
                    self.namespace.Handle_Status('تم حذف موظف', 1)

            else:
                self.txtOwnerPhone1.setFocus()
                self.namespace.Handle_Status('أدخل رقم الهاتف الاساسى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)

        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('خطأ فى البيانات المدخله تأكد من أن بيانات الموظف غير موجوده مسبقا', 2)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Table_Owners(self, name = ''):
        try:
            nameFlter = ''
            if name != '':
                nameFlter = f"and name like'{name}%'"
            self.cur.execute(f'''
            select name, phone1 , phone2 , address , email  , is_trader , is_client from persons
            where is_owner='نعم' {nameFlter}
            ''')
            tblOwners = self.cur.fetchall()
            self.tbl_owners_info.setRowCount(0)
            if len(tblOwners) != 0:
                self.tbl_owners_info.insertRow(0)
                for rownum, row in enumerate(tblOwners):
                    for colnum, col in enumerate(row):
                        self.tbl_owners_info.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_owners_info.rowCount()
                    if rowPosition == len(tblOwners):
                        break
                    self.tbl_owners_info.insertRow(rowPosition)
        except AttributeError as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Text_Owners(self):
        rowData = self.tbl_owners_info.selectedIndexes()
        self.txtOwnerName.setText(str(rowData[0].data()))
        self.txtOwnerPhone1.setText(rowData[1].data())
        self.txtOwnerPhone2.setText(str(rowData[2].data()))
        self.txtOwnerAddress.setText(str(rowData[3].data()))
        self.txtOwnerMail.setText(str(rowData[4].data()))
        if str(rowData[5].data()) == 'نعم':
            self.chkbxIsTrader.setChecked(True)


    def Fill_CbxClients(self):
        try:

            self.cur.execute('''
                select name, phone1 , phone2, address, email from persons
                where is_client='نعم' and is_owner = 'لا'
            ''')
            self.clientsInfo = self.cur.fetchall()
            self.cbxClientsNames.clear()
            self.cbxClientsNames.setCurrentIndex(-1)
            for client in self.clientsInfo:
                self.cbxClientsNames.addItem(client[0])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def chxClients_Toggled(self):
        if self.chkbxIsClient.isChecked():
            self.Fill_CbxClients()
        else:
            self.cbxClientsNames.clear()
            self.txtOwnerName.setText('')
            self.txtOwnerPhone1.setText('')
            self.txtOwnerMail.setText('')
            self.txtOwnerAddress.setText('')
            self.txtOwnerPhone2.setText('')

    def Get_From_Clients(self, client):
        self.txtOwnerName.setText(self.clientsInfo[client][0])
        self.txtOwnerPhone1.setText(self.clientsInfo[client][1])
        self.txtOwnerPhone2.setText(self.clientsInfo[client][2])
        self.txtOwnerAddress.setText(self.clientsInfo[client][3])
        self.txtOwnerMail.setText(self.clientsInfo[client][4])
