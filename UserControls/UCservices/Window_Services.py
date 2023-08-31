from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from win32api import GetSystemMetrics
from PyQt5.uic import loadUiType
import os
import mysql.connector
import shutil

servicesUI,_ = loadUiType('./UserControls/UCservices/UC_Services.ui')

class window_services(QFrame, servicesUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.InitUi()
        self.Init_Events()
        self.services_list.setCurrentRow(0)
        self.images = []  # Pictures of Hospital
        self.images1 = []  # Pictures of School
        self.images2 = []  # Pictures of Build
        self.images3 = []  # Pictures of Unit
        self.Handle_Event()
        self.Handle_Function()
        self.Handle_Btn()

    def InitUi(self):
        self.services_panels = [
            self.frame_trade,
            self.frame_eductional,
            self.frame_hospital
        ]

        self.services_btns = [
            self.btn_building_frame,
            self.btn_madrasa_frame,
            self.btn_hospital_frame
        ]

        self.se7i_panels = [
            self.Services_Hospital_Propreties,
            self.Services_Hospital_Archieve
        ]

        self.ta3limi_panels = [
            self.Services_Eductional_Propreties,
            self.Services_Eductional_Archieve
        ]

        self.trade_panels = [
            self.Services_Trading_Building,
            self.Services_Trading_Building_Arechieve,
            self.Services_Trading_Units,
            self.Services_Trading_Units_Arechieve,
        ]

    def View_Target_Frame(self, parent, child):
        for frame in parent:
            if frame == parent[child]:
                frame.setVisible(True)
            else:
                frame.setVisible(False)

    def Init_Events(self):
        self.services_list.currentRowChanged.connect(
            lambda: (
                self.View_Target_Frame(self.services_panels, self.services_list.currentRow()),
                self.services_btns[self.services_list.currentRow()].click(),
                self.services_btns[self.services_list.currentRow()].setFocus(),
            )
        )
        self.btn_madrasa_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.ta3limi_panels, 0)
        )
        self.btn_madrasa_archieve_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.ta3limi_panels, 1)
        )
        self.btn_building_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.trade_panels, 0)
        )
        self.btn_building_archieve_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.trade_panels, 1)
        )
        self.btn_units_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.trade_panels, 2)
        )
        self.btn_units_archieve_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.trade_panels, 3)
        )
        self.btn_hospital_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.se7i_panels, 0)
        )
        self.btn_hospital_archieve_frame.clicked.connect(
            lambda: self.View_Target_Frame(self.se7i_panels, 1)
        )

    def Handle_Event(self):
        #   Hospital
        self.cbxCityHospital.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxStreet(self.cbxStreetHospital, self.cbxCityHospital)
        )
        self.cbxStreetHospital.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxBlock(self.cbxBlockHospital, self.cbxStreetHospital)
        )
        self.cbxStatusHospital.currentIndexChanged.connect(
            lambda: (
                self.txtRestHospital.setEnabled(True) if self.cbxStatusHospital.currentIndex() == 1
                else self.txtRestHospital.setEnabled(False), self.txtRestHospital.setText('')
            )
        )
        self.txtPhoneHospital.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerHospital, self.txtPhoneHospital)
        )

        #    School
        self.cbxCitySchool.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxStreet(self.cbxStreetSchool, self.cbxCitySchool)
        )
        self.cbxStreetSchool.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxBlock(self.cbxBlockSchool, self.cbxStreetSchool)
        )
        self.cbxStatusSchool.currentIndexChanged.connect(
            lambda: (
                self.txtRestSchool.setEnabled(True) if self.cbxStatusSchool.currentIndex() == 1
                else self.txtRestSchool.setEnabled(False), self.txtRestSchool.setText('')
            )
        )
        self.txtPhoneSchool.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerSchool, self.txtPhoneSchool)
        )
        #   Build
        self.cbxCityBuild.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxStreet(self.cbxStreetBuild, self.cbxCityBuild)
        )
        self.cbxStreetBuild.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxBlock(self.cbxBlockBuild, self.cbxStreetBuild)
        )
        self.cbxStatusBuild.currentIndexChanged.connect(
            lambda: (
                self.txtRestBuild.setEnabled(True) if self.cbxStatusBuild.currentIndex() == 1
                else self.txtRestBuild.setEnabled(False), self.txtRestBuild.setText('')
            )
        )
        self.txtPhoneBuild.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerBuild, self.txtPhoneBuild)
        )

        # Unit
        self.cbxCityUnit.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxStreet(self.cbxStreetUnit, self.cbxCityUnit)
        )
        self.cbxStreetUnit.currentIndexChanged.connect(
            lambda:
            self.Fill_CbxBlock(self.cbxBlockUnit, self.cbxStreetUnit)
        )
        self.cbxStatusUnit.currentIndexChanged.connect(
            lambda: (
                self.txtRestUnit.setEnabled(True) if self.cbxStatusUnit.currentIndex() == 1
                else self.txtRestUnit.setEnabled(False), self.txtRestUnit.setText('')
            )
        )
        self.txtPhoneUnit.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerUnit, self.txtPhoneUnit)
        )

    def Handle_Btn(self):

        #   Hospital

        self.btn_add_Hospital.clicked.connect(
            lambda: self.Add_Hospital()
        )
        self.btn_edit_Hospital.clicked.connect(
            lambda: self.Edit_Hospital()
        )
        self.btn_remove_Hospital.clicked.connect(
            lambda: self.Delete_Hospital()
        )
        self.btn_add_imgHospital.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsHospital, self.images)
        )
        self.btn_remove_imgHospital.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsHospital, self.images)
        )
        self.btn_show_imgsHospital.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images) if len(self.images) != 0 else None
            )
        )
        self.btnSearchHospital.clicked.connect(
            lambda: self.Search_Hospital()
        )

        #   School
        self.btn_add_School.clicked.connect(
            lambda: self.Add_School()
        )
        self.btn_edit_School.clicked.connect(
            lambda: self.Edit_School()
        )
        self.btn_remove_School.clicked.connect(
            lambda: self.Delete_School()
        )
        self.btn_add_imgSchool.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsSchool, self.images1)
        )
        self.btn_remove_imgSchool.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsSchool, self.images1)
        )
        self.btn_show_imgsSchool.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images1) if len(self.images1) != 0 else None
            )
        )
        self.btnSearchSchool.clicked.connect(
            lambda: self.Search_School()
        )

        # Build
        self.btn_add_Build.clicked.connect(
            lambda: self.Add_Build()
        )
        self.btn_edit_Build.clicked.connect(
            lambda: self.Edit_Build()
        )
        self.btn_remove_Build.clicked.connect(
            lambda: self.Delete_Build()
        )
        self.btn_add_imgBuild.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsBuild, self.images2)
        )
        self.btn_remove_imgBuild.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsBuild, self.images2)
        )
        self.btn_show_imgsBuild.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images2) if len(self.images2) != 0 else None
            )
        )
        self.btnSearchBuild.clicked.connect(
            lambda: self.Search_Build()
        )

        #  Unit
        self.btn_add_Unit.clicked.connect(
            lambda: self.Add_Unit()
        )
        self.btn_edit_Unit.clicked.connect(
            lambda: self.Edit_Unit()
        )
        self.btn_remove_Unit.clicked.connect(
            lambda: self.Delete_Unit()
        )
        self.btn_add_imgUnit.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsUnit, self.images3)
        )
        self.btn_remove_imgUnit.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsUnit, self.images3)
        )
        self.btn_show_imgsUnit.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images3) if len(self.images3) != 0 else None
            )
        )
        self.btnSearchUnit.clicked.connect(
            lambda: self.Search_Unit()
        )

    def Handle_Function(self):
        self.Fill_CbxCities()
        self.Get_Owners_Info()

        ###  Fill CBX __________________________

    def Fill_CbxStreet(self, target=None, sender=None):
        try:
            if sender == None:
                sender = self.cbxCityHospital
            self.namespace.cur.execute(f'''
                select street_id, name from streets
                where city = '{self.citiesInfo[sender.currentIndex()][0]}'
            ''')
            self.streetsInfo = self.namespace.cur.fetchall()
            if target == None:
                self.cbxStreetHospital.clear()
                self.cbxStreetSchool.clear()
                self.cbxStreetBuild.clear()
                self.cbxStreetUnit.clear()
                for street in self.streetsInfo:
                    self.cbxStreetHospital.addItem(street[1])
                    self.cbxStreetSchool.addItem(street[1])
                    self.cbxStreetBuild.addItem(street[1])
                    self.cbxStreetunit.addItem(street[1])
            else:
                target.clear()
                for street in self.streetsInfo:
                    target.addItem(street[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxBlock(self, target=None, sender=None):
        try:
            if sender == None:
                sender = self.cbxStreetHospital
            self.namespace.cur.execute(f'''
                select block_id, name from blocks
                where street= '{self.streetsInfo[sender.currentIndex()][0]}'
            ''')
            self.blocksInfo = self.namespace.cur.fetchall()
            if target == None:
                self.cbxBlockHospital.clear()
                self.cbxBlockSchool.clear()
                self.cbxBlockBuild.clear()
                self.cbxBlockUint.clear()
                for block in self.blocksInfo:
                    self.cbxBlock.addItem(block[1])
                    self.cbxBlockSchool.addItem(block[1])
                    self.cbxBlockBuild.addItem(block[1])
                    self.cbxBlockUnit.addItem(block[1])
            else:
                target.clear()
                for block in self.blocksInfo:
                    target.addItem(block[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxCities(self):
        try:
            self.namespace.cur.execute('''
                select city_id, name from cities
            ''')
            self.citiesInfo = self.namespace.cur.fetchall()
            for city in self.citiesInfo:
                self.cbxCityHospital.addItem(city[1])
                self.cbxCitySchool.addItem(city[1])
                self.cbxCityBuild.addItem(city[1])
                self.cbxCityUnit.addItem(city[1])
        # except AttributeError:
        #     self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
        #     self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Get_Owners_Info(self):
        try:
            self.namespace.cur.execute('''
                select phone1, name from persons where is_owner = 'نعم'
            ''')
            self.ownerInfo = self.namespace.cur.fetchall()
            self.ownerPhonesList = []
            self.ownerNamesList = []
            for owner in self.ownerInfo:
                self.ownerPhonesList.append(owner[0])
                self.ownerNamesList.append(owner[1])
            ownerCompleter = QCompleter(self.ownerPhonesList)
            self.txtPhoneHospital.setCompleter(ownerCompleter)
            self.txtPhoneSchool.setCompleter(ownerCompleter)
            self.txtPhoneBuild.setCompleter(ownerCompleter)
            self.txtPhoneUnit.setCompleter(ownerCompleter)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Check_Owner(self, target, sender):
        if sender.text().strip().replace("'", "") in self.ownerPhonesList:
            name = self.ownerPhonesList.index(sender.text().strip().replace("'", ""))
            target.setText(self.ownerNamesList[name])
        else:
            target.setText('')

    ###Hospital_________________________
    def Add_Hospital(self):
        try:
            piece_id =self.txtPieceHospital.text().strip().replace("'", '')
            cityName = self.cbxCityHospital.currentIndex()
            streetName = self.cbxStreetHospital.currentIndex()
            blockName = self.cbxBlockHospital.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerHospital.text().strip().replace("'", '') == '':
                                self.txtPhoneHospital.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            pieceType = 'Hospital'
                            phone= self.txtPhoneHospital.text().strip().replace("'", '')
                            price = self.txtPriceHospital.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaHospital.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusHospital.currentText()
                            premium = '0'
                            if self.cbxStatusHospital.currentIndex() == 1:
                                premium = self.txtRestHospital.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsHospital.toPlainText().strip().replace("'", '')
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{ pieceType }' ,'{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')

                            # Convert Images to Byte and Insert them into Database
                            for img in self.images:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','Hospital')
                            ''')
                            self.namespace.db.commit()
                            self.images.clear()
                            self.tblImgsHospital.setRowCount(0)
                            self.Clear_Widgets(self.Services_Hospital_Propreties)
                            self.txtPieceHospital.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة مبني صحي ', 1)
                        else:
                            self.cbxBlockHospital.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetHospital.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityHospital.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceHispital.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Hospital(self):
        try:
            piece_id =self.txtPieceHospital.text().strip().replace("'", '')
            cityName = self.cbxCityHospital.currentIndex()
            streetName = self.cbxStreetHospital.currentIndex()
            blockName = self.cbxBlockHospital.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerHospital.text().strip().replace("'", '') == '':
                                    self.txtPhoneHospital.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                pieceType = 'Hospital'
                                phone = self.txtPhoneHospital.text().strip().replace("'", '')
                                price = self.txtPriceHospital.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaHospital.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusHospital.currentText()
                                premium = '0'
                                if self.cbxStatusHospital.currentIndex() == 1:
                                    premium = self.txtRestHospital.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsHospital.toPlainText().strip().replace("'", '')

                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}'
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'Hospital'
                                ''')
                                for img in self.images:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','Hospital')
                                ''')
                                self.namespace.db.commit()
                                self.images.clear()
                                self.tblImgsHospital.setRowCount(0)
                                self.Clear_Widgets(self.Services_Hospital_Propreties)
                                self.txtPieceHospital.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل المبني الصحي', 1)
                        else:
                            self.cbxBlockHospital.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetHospital.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityHospital.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceHospital.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Hospital(self):
        piece_id =self.txtPieceHospital.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                                            update propreties set working = 'no'
                                             where
                                            proprety ='{piece_id}' and type = 'Hospital'
                                        ''')
                    self.namespace.cur.execute(f'''
                                            delete from images where piece = '{piece_id}' and piece_type = 'Hospital'
                                        ''')
                    self.namespace.db.commit()
                    self.images.clear()
                    self.tblImgsHospital.setRowCount(0)
                    self.Clear_Widgets(self.Services_Hospital_Propreties)
                    self.txtPieceHospital.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف مبني صحي ', 1)
            else:
                self.txtPieceHospital.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_Hospital(self):
        try:
            piece_id = self.txtPieceHospital.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'Hospital' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'Hospital'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaHospital.setText(str(mainData[0][0]))
                self.txtPriceHospital.setText(str(mainData[0][1]))
                self.txtDetailsHospital.setText(mainData[0][2])
                self.txtPhoneHospital.setText(mainData[0][3])
                self.txtOwnerHospital.setText(mainData[0][4])
                self.cbxCityHospital.setCurrentText(mainData[0][5])
                self.cbxStreetHospital.setCurrentText(mainData[0][6])
                self.cbxBlockHospital.setCurrentText(mainData[0][7])
                self.cbxStatusHospital.setCurrentText(mainData[0][8])
                self.txtRestHospital.setText(str(mainData[0][9]))
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images.clear()
                self.tblImgsHospital.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsHospital.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsHospital.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsHospital.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsHospital.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceHospital.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود المبني الصحي غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    ###School___________________________
    def Add_School(self):
        try:
            piece_id =self.txtPieceSchool.text().strip().replace("'", '')
            cityName = self.cbxCitySchool.currentIndex()
            streetName = self.cbxStreetSchool.currentIndex()
            blockName = self.cbxBlockSchool.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerSchool.text().strip().replace("'", '') == '':
                                self.txtPhoneSchool.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'School'
                            phone= self.txtPhoneSchool.text().strip().replace("'", '')
                            price = self.txtPriceSchool.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaSchool.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusSchool.currentText()
                            premium = '0'
                            if self.cbxStatusSchool.currentIndex() == 1:
                                premium = self.txtRestSchool.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsSchool.toPlainText().strip().replace("'", '')

                            SchoolType = self.cbxTypeSchool.currentText()
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into eductional values
                                ('{SchoolType}','{piece_id}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images1:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','School')
                            ''')
                            self.namespace.db.commit()
                            self.images1.clear()
                            self.tblImgsSchool.setRowCount(0)
                            self.Clear_Widgets(self.Services_Eductional_Propreties)
                            self.txtPieceSchool.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة المدرسة ', 1)
                        else:
                            self.cbxBlockSchool.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetSchool.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCitySchool.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceSchool.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_School(self):
        try:
            piece_id =self.txtPieceSchool.text().strip().replace("'", '')
            cityName = self.cbxCitySchool.currentIndex()
            streetName = self.cbxStreetSchool.currentIndex()
            blockName = self.cbxBlockSchool.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerSchool.text().strip().replace("'", '') == '':
                                    self.txtPhoneSchool.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                pieceType = 'School'
                                phone= self.txtPhoneSchool.text().strip().replace("'", '')
                                price = self.txtPriceSchool.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaSchool.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusSchool.currentText()
                                premium = '0'
                                if self.cbxStatusSchool.currentIndex() == 1:
                                    premium = self.txtRestSchool.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsSchool.toPlainText().strip().replace("'", '')
                                SchoolType = self.cbxTypeSchool.currentText()
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'School'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update eductional set 
                                    type ='{SchoolType}'
                                    where piece='{piece_id}' 
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'School'
                                ''')
                                for img in self.images1:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','School')
                                ''')
                                self.namespace.db.commit()
                                self.images1.clear()
                                self.tblImgsSchool.setRowCount(0)
                                self.Clear_Widgets(self.Services_Eductional_Propreties)
                                self.txtPieceSchool.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم تعديل المدرسة ', 1)
                        else:
                            self.cbxBlockSchool.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetSchool.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCitySchool.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceSchool.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_School(self):
        piece_id =self.txtPieceSchool.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where proprety='{piece_id}' and type = 'School'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'School'
                    ''')
                    self.namespace.db.commit()
                    self.images1.clear()
                    self.tblImgsSchool.setRowCount(0)
                    self.Clear_Widgets(self.Services_Eductional_Propreties)
                    self.txtPieceSchool.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف المدرسة ', 1)
            else:
                self.txtPieceSchool.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_School(self):
        try:
            piece_id = self.txtPieceSchool.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'School' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from eductional
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'School'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaSchool.setText(str(mainData[0][0]))
                self.txtPriceSchool.setText(str(mainData[0][1]))
                self.txtDetailsSchool.setText(mainData[0][2])
                self.txtPhoneSchool.setText(mainData[0][3])
                self.txtOwnerSchool.setText(mainData[0][4])
                self.cbxCitySchool.setCurrentText(mainData[0][5])
                self.cbxStreetSchool.setCurrentText(mainData[0][6])
                self.cbxBlockSchool.setCurrentText(mainData[0][7])
                self.cbxStatusSchool.setCurrentText(mainData[0][8])
                self.txtRestSchool.setText(str(mainData[0][9]))
                # fill second data
                self.cbxTypeSchool.setCurrentText(secondData[0][0])
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images1.clear()
                self.tblImgsSchool.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsSchool.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images1.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsSchool.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsSchool.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsSchool.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceSchool.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود المبني التعليمي غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    ### Build______________________________
    def Add_Build(self):
        try:
            piece_id = self.txtPieceBuild.text().strip().replace("'", '')
            cityName = self.cbxCityBuild.currentIndex()
            streetName = self.cbxStreetBuild.currentIndex()
            blockName = self.cbxBlockBuild.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerBuild.text().strip().replace("'", '') == '':
                                self.txtPhoneBuild.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'Build'
                            NameBuild= self.txtNameBuild.text().strip().replace("'", '')
                            if NameBuild == '':
                                NameBuild= 'لم يحدد'
                            phone = self.txtPhoneBuild.text().strip().replace("'", '')
                            price = self.txtPriceBuild.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaBuild.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusBuild.currentText()
                            premium = '0'
                            if self.cbxStatusBuild.currentIndex() == 1:
                                premium = self.txtRestBuild.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsBuild.toPlainText().strip().replace("'", '')

                            # secondary info
                            UnitNum = self.txtNumUnits.text().strip().replace("'", "")
                            if UnitNum == '':
                                UnitNum = 'لم يحدد'
                            floorNum = self.txtNumFloors.text().strip().replace("'", "")
                            if floorNum == '':
                                floorNum = 'لم يحدد'
                            manage = 'لا'
                            trad = 'لا'
                            skani = 'لا'
                            if self.chxManageBuild.isChecked():
                                manage = 'نعم'
                            if self.chxTradBuild.isChecked():
                                trad = 'نعم'
                            if self.chxSkaniBuild.isChecked():
                                skani = 'نعم'
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                   insert into propreties values
                                   ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                   '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                   '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                               ''')
                            # name num_of_floors num_of_units trading managing apartment piece
                            self.namespace.cur.execute(f'''
                                   insert into service_building values
                                   ('{NameBuild}','{floorNum}','{UnitNum}','{trad}','{manage}','{skani}','{piece_id}')
                               ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images2:
                                self.namespace.cur.execute(f'''
                                   insert into images values
                                   (LOAD_FILE('{img}'), '{img}','{piece_id}','Build')
                               ''')
                            self.namespace.db.commit()
                            self.images2.clear()
                            self.tblImgsBuild.setRowCount(0)
                            self.Clear_Widgets(self.Services_Trading_Building)
                            self.txtPieceBuild.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة مبني تجاري', 1)
                        else:
                            self.cbxBlockBuild.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetBuild.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityBuild.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceBuild.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Build(self):
        try:
            piece_id = self.txtPieceBuild.text().strip().replace("'", '')
            cityName = self.cbxCityBuild.currentIndex()
            streetName = self.cbxStreetBuild.currentIndex()
            blockName = self.cbxBlockBuild.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                                self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerBuild.text().strip().replace("'", '') == '':
                                    self.txtPhoneBuild.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'Build'
                                phone = self.txtPhoneBuild.text().strip().replace("'", '')
                                NameBuild= self.txtNameBuild.text().strip().replace("'", '')
                                if NameBuild == '':
                                    NameBuild= 'لم يحدد'
                                price = self.txtPriceBuild.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaBuild.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusBuild.currentText()
                                premium = '0'
                                if self.cbxStatusBuild.currentIndex() == 1:
                                    premium = self.txtRestBuild.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsBuild.toPlainText().strip().replace("'", '')

                                # secondary info
                                UnitNum = self.txtNumUnits.text().strip().replace("'", "")
                                floorNum = self.txtNumFloors.text().strip().replace("'", "")
                                manage ='لا '
                                trad = 'لا '
                                skani = 'لا '
                                if self.chxManageBuild.isChecked():
                                    manage = 'نعم'
                                if self.chxTradBuild.isChecked():
                                    trad = 'نعم'
                                if self.chxSkaniBuild.isChecked():
                                    skani = 'نعم'

                                # insert into Database
                                self.namespace.cur.execute(f'''
                                       update propreties set area='{area}', price='{price}',details='{details}',
                                       owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                       block='{self.blocksInfo[blockName][0]}',
                                       city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                       where proprety = '{piece_id}' and type = 'Build'
                                   ''')
                                # name num_of_floors num_of_units trading managing apartment piece
                                self.namespace.cur.execute(f'''
                                       update service_building set num_of_units='{UnitNum}',
                                       num_of_floors='{floorNum}',
                                       name ='{NameBuild}',
                                       trading ='{trad}',
                                       managing ='{manage}',
                                       apartment='{skani}'
                                       where piece='{piece_id}' 
                                   ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                   delete from images where piece = '{piece_id}' and piece_type = 'Build'
                                   ''')
                                for img in self.images2:
                                    self.namespace.cur.execute(f'''
                                       insert into images values
                                       (LOAD_FILE('{img}'), '{img}','{piece_id}','Build')
                                   ''')
                                self.namespace.db.commit()
                                self.images2.clear()
                                self.tblImgsBuild.setRowCount(0)
                                self.Clear_Widgets(self.Services_Trading_Building)
                                self.txtPieceBuild.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل مبني تجاري', 1)
                        else:
                            self.cbxBlockBuild.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetBuild.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityBuild.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceBuild.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Delete_Build(self):
        piece_id = self.txtPieceBuild.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                    self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                           update propreties set working = 'no'
                           where proprety='{piece_id}' and type = 'Build'
                       ''')
                    self.namespace.cur.execute(f'''
                           delete from images where piece = '{piece_id}' and piece_type = 'Build'
                       ''')
                    self.namespace.db.commit()
                    self.images2.clear()
                    self.tblImgsBuild.setRowCount(0)
                    self.Clear_Widgets(self.Services_Trading_Building)
                    self.txtPieceBuild.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف المبني التجاري', 1)
            else:
                self.txtPieceBuild.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_Build(self):
        try:
            piece_id = self.txtPieceBuild.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                       select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                       streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                       from propreties
                       inner JOIN persons on propreties.owner = persons.phone1
                       inner JOIN streets on propreties.street = streets.street_id
                       inner join blocks on propreties.block = blocks.block_id
                       inner JOIN cities on propreties.city = cities.city_id
                       where propreties.proprety = '{piece_id}' and type = 'Build' and working = 'yes'
                   ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                       select * from service_building
                       where piece = '{piece_id}'
                   ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                       select * from images
                       where piece = '{piece_id}' and piece_type = 'Build'
                   ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                 # name num_of_floors num_of_units trading managing apartment piece
                self.txtAreaBuild.setText(str(mainData[0][0]))
                self.txtPriceBuild.setText(str(mainData[0][1]))
                self.txtDetailsBuild.setText(mainData[0][2])
                self.txtPhoneBuild.setText(mainData[0][3])
                self.txtOwnerBuild.setText(mainData[0][4])
                self.cbxCityBuild.setCurrentText(mainData[0][5])
                self.cbxStreetBuild.setCurrentText(mainData[0][6])
                self.cbxBlockBuild.setCurrentText(mainData[0][7])
                self.cbxStatusBuild.setCurrentText(mainData[0][8])
                self.txtRestBuild.setText(str(mainData[0][9]))
                # fill second data
                self.txtNumFloors.setText(str(secondData[0][1]))
                self.txtNameBuild.setText(str(secondData[0][0]))
                self.txtNumUnits.setText(str(secondData[0][2]))
                if secondData[0][4] == 'نعم':
                    self.chxManageBuild.setChecked(True)
                if secondData[0][3] == 'نعم':
                    self.chxTradBuild.setChecked(True)
                if secondData[0][5] == 'نعم':
                    self.chxSkaniBuild.setChecked(True)
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images2.clear()
                self.tblImgsBuild.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsBuild.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images2.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsBuild.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsBuild.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsBuild.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceBuild.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
            self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    ###Unit_____________________________

    def Add_Unit(self):
        try:
            piece_Unit =self.txtPieceUnit.text().strip().replace("'", '')
            piece_Build = self.txtpiecebuid.text().strip().replace("'", '')
            cityName = self.cbxCityUnit.currentIndex()
            streetName = self.cbxStreetUnit.currentIndex()
            blockName = self.cbxBlockUnit.currentIndex()
            if piece_Unit != '':
                if piece_Build != '':
                    if cityName >= 0:
                        if streetName >= 0:
                            if blockName >= 0:
                                if self.txtOwnerUnit.text().strip().replace("'", '') == '':
                                    self.txtPhoneUnit.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'Unit'
                                phone= self.txtPhoneUnit.text().strip().replace("'", '')
                                price = self.txtPriceUnit.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaUnit.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusUnit.currentText()
                                premium = '0'
                                if self.cbxStatusUnit.currentIndex() == 1:
                                    premium = self.txtRestUnit.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsUnit.toPlainText().strip().replace("'", '')

                                # secondary info
                                name = self.txtNameUnit.text().strip().replace("'", "")
                                trad='لا'
                                manage ='لا'
                                skani='لا'
                                if self.chxTrad.isChecked():
                                    trad = 'نعم'
                                if self.chxManage.isChecked():
                                    manage = 'نعم'
                                if self.chxSkani.isChecked():
                                    skani = 'نعم'
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    insert into propreties values
                                    ('{piece_Unit}', '{pieceType}','{area}','{price}','{details}',
                                    '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                    '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                                ''')
                                #unit_name trading managing apartment building piece
                                self.namespace.cur.execute(f'''
                                    insert into service_unit values
                                    ('{name}','{trad}','{manage}','{skani}','{piece_Build}','{piece_Unit}')
                                ''')
                                # Convert Images to Byte and Insert them into Database

                                for img in self.images3:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_Unit}','Unit')
                                ''')
                                self.namespace.db.commit()
                                self.images3.clear()
                                self.tblImgsUnit.setRowCount(0)
                                self.Clear_Widgets(self.Services_Trading_Units)
                                self.txtPieceUnit.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم اضافة وحدة تجارية', 1)
                            else:
                                self.cbxBlockUnit.setFocus()
                                self.namespace.Handle_Status('أدخل البلوك', 3)
                        else:
                            self.cbxStreetUnit.setFocus()
                            self.namespace.Handle_Status('أدخل الحي', 3)
                    else:
                        self.cbxCityUnit.setFocus()
                        self.namespace.Handle_Status('أدخل المدينة', 3)
                else:
                    self.txtpiecebuid.setFocus()
                    self.namespace.Handle_Status('أدخل رقم المبني', 3)
            else:
                self.txtPieceUnit.setFocus()
                self.namespace.Handle_Status('أدخل رقم  الوحدة ', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
           QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Unit(self):
        try:
            piece_Unit = self.txtPieceUnit.text().strip().replace("'", '')
            piece_Build = self.txtPieceBuild.text().strip().replace("'", '')
            cityName = self.cbxCityFlat.currentIndex()
            streetName = self.cbxStreetFlat.currentIndex()
            blockName = self.cbxBlockFlat.currentIndex()
            if piece_Unit != '':
                if piece_Build != '':
                    if cityName >= 0:
                        if streetName >= 0:
                            if blockName >= 0:
                                if self.txtOwnerUnit.text().strip().replace("'", '') == '':
                                    self.txtPhoneUnit.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'Unit'
                                phone= self.txtPhoneUnit.text().strip().replace("'", '')
                                price = self.txtPriceUnit.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaUnit.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusUnit.currentText()
                                premium = '0'
                                if self.cbxStatusUnit.currentIndex() == 1:
                                    premium = self.txtRestUnit.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsUnit.toPlainText().strip().replace("'", '')

                                # secondary info
                                name = self.txtNameUnit.text().strip().replace("'", "")
                                trad = 'لا'
                                manage = 'لا'
                                if self.chxTrad.isChecked():
                                    trad = 'نعم'
                                if self.chxManage.isChecked():
                                    manage = 'نعم'
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_Unit}' and type = 'Unit'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update Unit set 
                                    where piece='{piece_Unit}' 
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_Unit}' and piece_type = 'Unit'
                                ''')
                                for img in self.images3:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','Unit')
                                ''')
                                self.namespace.db.commit()
                                self.images3.clear()
                                self.tblImgsUnit.setRowCount(0)
                                self.Clear_Widgets(self.Services_Trading_Units)
                                self.txtPieceUnit.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل وحدة التجارية', 1)
                            else:
                                self.cbxBlockUnit.setFocus()
                                self.namespace.Handle_Status('أدخل البلوك', 3)
                        else:
                            self.cbxStreetUnit.setFocus()
                            self.namespace.Handle_Status('أدخل الحي', 3)
                    else:
                        self.cbxCityUnit.setFocus()
                        self.namespace.Handle_Status('أدخل المدينة', 3)
                else:
                    self.txtPieceBuild.setFocus()
                    self.namespace.Handle_Status('أدخل رقم القطعه', 3)
            else:
                self.txtPieceUnit.setFocus()
                self.namespace.Handle_Status('أدخل رقم الوحدة', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Unit(self):
        piece_id =self.txtPieceUnit.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where proprety='{piece_id}' and type = 'Unit'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'Unit'
                    ''')
                    self.namespace.db.commit()
                    self.images3.clear()
                    self.tblImgsUnit.setRowCount(0)
                    self.Clear_Widgets(self.Services_Trading_Units)
                    self.txtPieceUnit.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف الوحدة ', 1)
            else:
                self.txtPieceunit.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_Unit(self):
        try:
            piece_id = self.txtPieceUnit.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'Unit' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from Unit
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'Unit'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaUnit.setText(str(mainData[0][0]))
                self.txtPriceUnit.setText(str(mainData[0][1]))
                self.txtDetailsUnit.setText(mainData[0][2])
                self.txtPhoneUnit.setText(mainData[0][3])
                self.txtOwnerUnit.setText(mainData[0][4])
                self.cbxCityUnit.setCurrentText(mainData[0][7])
                self.cbxStreetUnit.setCurrentText(mainData[0][5])
                self.cbxBlockUnit.setCurrentText(mainData[0][6])
                self.cbxStatusUnit.setCurrentText(mainData[0][8])
                self.txtRestUnit.setText(str(mainData[0][9]))
                # fill second data
                self.txtNameUnit.setText(str(secondData[0][1]))
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images3.clear()
                self.tblImgsUnit.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsUnit.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.Unit.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsUnit.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsUnit.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsUnit.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceUnit.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

   #__________________________________________________________________________
    def Clear_Widgets(self, target):
        for child in target.children():
            if isinstance(child, QLineEdit):
                child.setText('')
            if isinstance(child, QTextEdit):
                child.setText('')
            if isinstance(child, QComboBox):
                try:
                    child.setCurrentIndex(0)
                except:
                    child.clear()
            if isinstance(child, QCheckBox):
                child.setChecked(False)

    def Get_Imgs(self, sender, imglist):
        try:

            supportedImageFormats = {'.bmp', '.eps', '.gif', '.icns', '.ico', '.im', '.jpg', '.jpeg', '.jpeg2000',
                                     '.msp', '.pcx', \
                                     '.png', '.ppm', '.sgi', '.tiff', '.tif', '.xbm', '.BMP', '.EPS', '.GIF', '.ICNS',
                                     '.ICO', '.IM', '.JPG', '.JPEG', '.JPEG2000', '.MSP', '.PCX', \
                                     '.PNG', '.PPM', '.SGI', '.TIFF', '.TIF', '.XBM'}
            fileDlg = QFileDialog(self)
            fileDlg.setDirectory('./')
            paths = fileDlg.getOpenFileNames(
                filter="All Files (*.*);; JPEG (*.jpg;*.jpeg;*.jpeg2000);;GIF (*.gif);;PNG (*.png);;TIF (*.tif;*.tiff);;BMP (*.bmp);; Nikon (*.nef;*.nrw);;Sony (*.arw;*.srf;*.sr2);;Canon (*.crw;*.cr2;*.cr3)")[
                0]
            if len(paths) != 0:
                rowIndex = sender.rowCount()
                if rowIndex == 0:
                    sender.insertRow(0)
                else:
                    sender.insertRow(rowIndex)

                for row, path in enumerate(paths):
                    if not path == '':
                        if not (os.path.splitext(path)[1] in supportedImageFormats):
                            self.namespace.Handle_Status("Not supported image type!", 2)
                            return
                    else:
                        return
                    imglist.append(path)
                    imgName = str(path).split('/')
                    sender.setItem(rowIndex + row, 0, QTableWidgetItem(str(imgName[-1])))
                    rowPosition = sender.rowCount()
                    if rowPosition == len(paths) + rowIndex:
                        break
                    sender.insertRow(rowPosition)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Remove_Selected_Imgs(self, sender, imglist):

        try:
            if sender.rowCount() != 0:
                selectedImgs = sender.selectionModel().selectedRows()
                for img in selectedImgs:
                    del imglist[img.row()]
                sender.setRowCount(0)
                if len(imglist) != 0:
                    sender.insertRow(0)
                    for row, path in enumerate(imglist):

                        imgName = str(path).split('/')
                        sender.setItem(row, 0, QTableWidgetItem(str(imgName[-1])))
                        rowPosition = sender.rowCount()
                        if rowPosition == len(imglist):
                            break
                        sender.insertRow(rowPosition)

        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)
