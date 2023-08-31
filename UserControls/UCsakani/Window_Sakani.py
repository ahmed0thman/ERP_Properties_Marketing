from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from win32api import GetSystemMetrics
from PyQt5.uic import loadUiType
import os
import mysql.connector
import shutil
sakaniUI,_ = loadUiType('./UserControls/UCsakani/UC_Sakani.ui')

class window_sakani(QFrame, sakaniUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.InitUi()
        self.Init_Events()
        self.Handle_Function()
        self.Handle_Btn()
        self.sakani_list.setCurrentRow(0)
        self.images = []    # Pictures of resident
        self.images1 = []   # Pictures of villa
        self.images2 = []   # Pictures of flat
        self.images3 = []   # Pictures of double

    def InitUi(self):
        self.sakani_panels = [
            self.frame_emarah,
            self.frame_villa,
            self.frame_flat
        ]

        self.sakani_btns = [
            self.btn_emarah_frame,
            self.btn_villa_frame,
            self.btn_flat_frame
        ]

        self.emarah_panels = [
            self.Emara_Properties,
            self.Emara_Archiev
        ]

        self.villa_panels = [
            self.Vila_Properties,
            self.Vila_Archiev
        ]

        self.flat_panels = [
            self.Flat_Normal_propeties,
            self.Flat_Normal_Archiev,
            self.Doublex_Properties,
            self.Doublex_Archiev,
        ]


    def View_Target_Frame(self, parent, child):
        for frame in parent:
            if frame == parent[child]:
                frame.setVisible(True)
            else:
                frame.setVisible(False)

    def Init_Events(self):
        self.sakani_list.currentRowChanged.connect(
            lambda: (
                self.View_Target_Frame(self.sakani_panels, self.sakani_list.currentRow()),
                self.sakani_btns[self.sakani_list.currentRow()].click(),
                self.sakani_btns[self.sakani_list.currentRow()].setFocus(),
            )
        )

        self.btn_emarah_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.emarah_panels, 0),
            )
        )
        self.btn_emarah_archieve_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.emarah_panels, 1),
            )
        )
        self.btn_flat_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.flat_panels, 0),
            )
        )
        self.btn_flat_archieve_frame.clicked.connect(
            lambda: (self.View_Target_Frame(self.flat_panels, 1),
             )
        )
        self.btn_doblex_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.flat_panels, 2),
            )
        )
        self.btn_doplex_arechieve_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.flat_panels, 3),
            )
        )
        self.btn_villa_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.villa_panels, 0),
            )
        )
        self.btn_villa_archieve_frame.clicked.connect(
            lambda: (
                self.View_Target_Frame(self.villa_panels, 1),
            )
        )
        # EMARAH Events
        self.cbxCityEmarah.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxStreet(self.cbxStreetEmarah, self.cbxCityEmarah)
        )
        self.cbxStreetEmarah.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxBlock(self.cbxBlockEmarah, self.cbxStreetEmarah)
        )
        self.cbxStatusEmarah.currentIndexChanged.connect(
            lambda: (
                self.txtRestEmarah.setEnabled(True) if self.cbxStatusEmarah.currentIndex() == 1
                else self.txtRestEmarah.setEnabled(False), self.txtRestEmarah.setText('')
            )
        )
        self.txtOwnerPhoneEmarah.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerNameEmarah, self.txtOwnerPhoneEmarah)
        )
        # Villa Events
        self.cbxCityVilla.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxStreet(self.cbxStreetVilla, self.cbxCityVilla)
        )
        self.cbxStreetVilla.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxBlock(self.cbxBlockVilla, self.cbxStreetVilla)
        )
        self.cbxStatusVilla.currentIndexChanged.connect(
            lambda: (
                self.txtRestVilla.setEnabled(True) if self.cbxStatusVilla.currentIndex() == 1
                else self.txtRestVilla.setEnabled(False), self.txtRestVilla.setText('')
            )
        )
        self.txtOwnerPhoneVilla.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerNameVilla, self.txtOwnerPhoneVilla)
        )
        # FLAT Events
        self.cbxCityFlat.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxStreet(self.cbxStreetFlat, self.cbxCityFlat)
        )
        self.cbxStreetFlat.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxBlock(self.cbxBlockFlat, self.cbxStreetFlat)
        )
        self.cbxStatusFlat.currentIndexChanged.connect(
            lambda: (
                self.txtRestFlat.setEnabled(True) if self.cbxStatusFlat.currentIndex() == 1
                else self.txtRestFlat.setEnabled(False), self.txtRestFlat.setText('')
            )
        )
        self.txtOwnerPhoneFlat.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerNameFlat, self.txtOwnerPhoneFlat)
        )

        # DOBLEX Events
        self.cbxCityFlat_2.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxStreet(self.cbxStreetFlat_2, self.cbxCityFlat_2)
        )
        self.cbxStreetFlat_2.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxBlock(self.cbxBlockFlat_2, self.cbxStreetFlat_2)
        )
        self.cbxStatusFlat_2.currentIndexChanged.connect(
            lambda: (
                self.txtRestFlat_2.setEnabled(True) if self.cbxStatusFlat_2.currentIndex() == 1
                else self.txtRestFlat_2.setEnabled(False), self.txtRestFlat_2.setText('')
            )
        )
        self.txtOwnerPhoneFlat_2.textChanged.connect(
            lambda: self.Check_Owner(self.txtOwnerNameFlat_2, self.txtOwnerPhoneFlat_2)
        )

    def Handle_Btn(self):
        # EMARAH Buttons
        self.btn_add_3emara.clicked.connect(
            lambda: self.Add_Emarah()
        )
        self.btn_edit_3emara.clicked.connect(
            lambda: self.Edit_Emarah()
        )
        self.btn_remove_3emara.clicked.connect(
            lambda: self.Delete_Emarah()
        )
        self.btn_add_imgEmarah.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsEmarah, self.images)
        )

        self.btn_remove_imgEmarah.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsEmarah, self.images)
        )
        self.btn_show_imgsEmarah.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images) if len(self.images) != 0 else None
            )
        )
        self.btn_emarah_archieve_frame.clicked.connect(
            lambda: self.Get_All_Emarah()
        )
        self.btnSearchEmarah.clicked.connect(
            lambda: self.Search_Emarah()
        )

        # VILLA Buttons
        self.btn_add_vella.clicked.connect(
            lambda: self.Add_Villa()
        )
        self.btn_edit_vella.clicked.connect(
            lambda: self.Edit_Villa()
        )
        self.btn_remove_vella.clicked.connect(
            lambda: self.Delete_Villa()
        )
        self.btn_add_imgVilla.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsVilla, self.images1)
        )

        self.btn_remove_imgVilla.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsVilla, self.images1)
        )
        self.btn_show_imgsVilla.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images1) if len(self.images1) != 0 else None
            )
        )
        self.btn_villa_archieve_frame.clicked.connect(
            lambda: self.Get_All_Villa()
        )
        self.btnSearchVilla.clicked.connect(
            lambda: self.Search_Villa()
        )

        # FLAT Buttons
        self.btn_add_42a.clicked.connect(
            lambda: self.Add_Flat()
        )
        self.btn_edit_42a.clicked.connect(
            lambda: self.Edit_Flat()
        )
        self.btn_remove_42a.clicked.connect(
            lambda: self.Delete_Flat()
        )
        self.btn_add_imgFlat.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsFlat, self.images2)
        )

        self.btn_remove_imgFlat.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsFlat, self.images2)
        )
        self.btn_show_imgsFlat.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images2) if len(self.images2) != 0 else None
            )
        )
        self.btn_flat_archieve_frame.clicked.connect(
            lambda: self.Get_All_Flat()
        )
        self.btnSearchFlat.clicked.connect(
            lambda: self.Search_Flat()
        )
        # DOBLEX Buttons
        self.btn_add_dobleks.clicked.connect(
            lambda: self.Add_Doblex()
        )
        self.btn_edit_dobleks.clicked.connect(
            lambda: self.Edit_Doblex()
        )
        self.btn_remove_dobleks.clicked.connect(
            lambda: self.Delete_Doblex()
        )
        self.btn_add_imgFlat_2.clicked.connect(
            lambda: self.Get_Imgs(self.tblImgsFlat_2, self.images3)
        )

        self.btn_remove_imgFlat.clicked.connect(
            lambda: self.Remove_Selected_Imgs(self.tblImgsFlat_2, self.images3)
        )
        self.btn_show_imgsFlat_2.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images3) if len(self.images3) != 0 else None
            )
        )
        self.btn_doplex_arechieve_frame.clicked.connect(
            lambda: self.Get_All_Doblex()
        )
        self.btnSearchFlat_2.clicked.connect(
            lambda: self.Search_Doblex()
        )

    def Handle_Function(self):
        self.Fill_CbxCities()
        self.Get_Owners_Info()
    # ----------------------------
    # General Info Events

    def Fill_CbxStreet(self, target=None, sender=None):
        try:
            if sender == None:
                sender = self.cbxCityEmarah
            self.namespace.cur.execute(f'''
                select street_id, name from streets
                where city = '{self.citiesInfo[sender.currentIndex()][0]}'
            ''')
            self.streetsInfo = self.namespace.cur.fetchall()
            if target == None:
                self.cbxStreetEmarah.clear()
                self.cbxStreetVilla.clear()
                self.cbxStreetFlat.clear()
                self.cbxStreetFlat_2.clear()
                for street in self.streetsInfo:
                    self.cbxStreetEmarah.addItem(street[1])
                    self.cbxStreetVilla.addItem(street[1])
                    self.cbxStreetFlat.addItem(street[1])
                    self.cbxStreetFlat_2.addItem(street[1])
            else:
                target.clear()
                for street in self.streetsInfo:
                    target.addItem(street[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxBlock(self, target=None, sender=None):
        try:
            if sender == None:
                sender = self.cbxStreetEmarah
            self.namespace.cur.execute(f'''
                select block_id, name from blocks
                where street= '{ self.streetsInfo[sender.currentIndex()][0]}'
            ''')
            self.blocksInfo = self.namespace.cur.fetchall()
            if target == None:
                self.cbxBlockEmarah.clear()
                self.cbxBlockVilla.clear()
                self.cbxBlockFlat.clear()
                self.cbxBlockFlat_2.clear()
                for block in self.blocksInfo:
                    self.cbxBlockEmarah.addItem(block[1])
                    self.cbxBlockVilla.addItem(block[1])
                    self.cbxBlockFlat.addItem(block[1])
                    self.cbxBlockFlat_2.addItem(block[1])
            else:
                target.clear()
                for block in self.blocksInfo:
                    target.addItem(block[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxCities(self):
        try:
            self.namespace.cur.execute('''
                select city_id, name from cities
            ''')
            self.citiesInfo = self.namespace.cur.fetchall()
            for city in self.citiesInfo:
                self.cbxCityEmarah.addItem(city[1])
                self.cbxCityVilla.addItem(city[1])
                self.cbxCityFlat.addItem(city[1])
                self.cbxCityFlat_2.addItem(city[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

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
            self.txtOwnerPhoneEmarah.setCompleter(ownerCompleter)
            self.txtOwnerPhoneVilla.setCompleter(ownerCompleter)
            self.txtOwnerPhoneFlat.setCompleter(ownerCompleter)
            self.txtOwnerPhoneFlat_2.setCompleter(ownerCompleter)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Check_Owner(self, target, sender):
        if sender.text().strip().replace("'","") in self.ownerPhonesList:
            name = self.ownerPhonesList.index(sender.text().strip().replace("'",""))
            target.setText(self.ownerNamesList[name])
        else:
            target.setText('')

    # Special Info For Flat and Doblex

    # -------------------------------
    # Add | Edit | Delete 3emarah Functions
    def Add_Emarah(self):
        try:
            piece_id =self.txtPieceIDEmarah.text().strip().replace("'", '')
            cityName = self.cbxCityEmarah.currentIndex()
            streetName = self.cbxStreetEmarah.currentIndex()
            blockName = self.cbxBlockEmarah.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerNameEmarah.text().strip().replace("'", '') == '':
                                self.txtOwnerPhoneEmarah.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'emarah'
                            phone= self.txtOwnerPhoneEmarah.text().strip().replace("'", '')
                            price = self.txtPriceEmarah.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaEmarah.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusEmarah.currentText()
                            premium = '0'
                            if self.cbxStatusEmarah.currentIndex() == 1:
                                premium = self.txtRestEmarah.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsEmarah.toPlainText().strip().replace("'", '')

                            # secondary info
                            ta4teb = self.cbxTa4tebEmarah.currentText()
                            floorNum = self.txtFloorNumEmarah.text().strip().replace("'", "")
                            electricity = 'لا'
                            water = 'لا'
                            gaz = 'لا'
                            if self.ckbxElecEmarah.isChecked():
                                electricity = 'نعم'
                            if self.ckbxWaterEmarah.isChecked():
                                water = 'نعم'
                            if self.ckbxGazEmarah.isChecked():
                                gaz = 'نعم'
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into emara values
                                ('{floorNum}','{ta4teb}','{gaz}','{water}', '{electricity}','{piece_id}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','emarah')
                            ''')
                            self.namespace.db.commit()
                            self.images.clear()
                            self.tblImgsEmarah.setRowCount(0)
                            self.Clear_Widgets(self.Emara_Properties)
                            self.txtPieceIDEmarah.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة عماره', 1)
                        else:
                            self.cbxBlockEmarah.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetEmarah.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityEmarah.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDEmarah.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Emarah(self):
        try:
            piece_id =self.txtPieceIDEmarah.text().strip().replace("'", '')
            cityName = self.cbxCityEmarah.currentIndex()
            streetName = self.cbxStreetEmarah.currentIndex()
            blockName = self.cbxBlockEmarah.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerNameEmarah.text().strip().replace("'", '') == '':
                                    self.txtOwnerPhoneEmarah.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                phone = self.txtOwnerPhoneEmarah.text().strip().replace("'", '')
                                price = self.txtPriceEmarah.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaEmarah.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusEmarah.currentText()
                                premium = '0'
                                if self.cbxStatusEmarah.currentIndex() == 1:
                                    premium = self.txtRestEmarah.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsEmarah.toPlainText().strip().replace("'", '')

                                # secondary info
                                ta4teb = self.cbxTa4tebEmarah.currentText()
                                floorNum = self.txtFloorNum.Emarahtext().strip().replace("'", "")
                                electricity = 'لا'
                                water = 'لا'
                                gaz = 'لا'
                                if self.ckbxElecEmarah.isChecked():
                                    electricity = 'نعم'
                                if self.ckbxWaterEmarah.isChecked():
                                    water = 'نعم'
                                if self.ckbxGazEmarah.isChecked():
                                    gaz = 'نعم'

                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'emarah'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update emara set num_of_floors='{floorNum}',ta4teb_type='{ta4teb}',
                                    gaz = '{gaz}', water = '{water}', electricity = '{electricity}'
                                    where piece='{piece_id}' 
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'emarah'
                                ''')
                                for img in self.images:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','emarah')
                                ''')
                                self.namespace.db.commit()
                                self.images.clear()
                                self.tblImgsEmarah.setRowCount(0)
                                self.Clear_Widgets(self.Emara_Properties)
                                self.txtPieceIDEmarah.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل عماره', 1)
                        else:
                            self.cbxBlockEmarah.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetEmarah.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityEmarah.setFocus()
                    self.namespaceEmarah.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDEmarah.setFocus()
                self.namespaceEmarah.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Emarah(self):
        piece_id =self.txtPieceIDEmarah.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        proprety piece='{piece_id}' and type = 'emarah'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'emarah'
                    ''')
                    self.namespace.db.commit()
                    self.images.clear()
                    self.tblImgsEmarah.setRowCount(0)
                    self.Clear_Widgets(self.Emara_Properties)
                    self.txtPieceIDEmarah.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف عماره', 1)
            else:
                self.txtPieceIDEmarah.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Get_All_Emarah(self):
        try:
            self.namespace.cur.execute(f'''
                    select propreties.proprety,persons.name,cities.name,streets.name,blocks.name,
                    emara.ta4teb_type,emara.num_of_floors,
                    propreties.area,propreties.price,emara.electricity,emara.gaz,emara.water,
                    propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    inner JOIN emara on propreties.proprety = emara.piece
                    where propreties.type = 'emarah' and working = 'yes'
                ''')
            doblexData = self.namespace.cur.fetchall()
            print(doblexData)
            self.tblEmarahArchieve.setRowCount(0)
            if len(doblexData) != 0:
                self.tblEmarahArchieve.insertRow(0)
                for rowNum, row in enumerate(doblexData):
                    for colNum, item in enumerate(row):
                        self.tblEmarahArchieve.setItem(rowNum, colNum, QTableWidgetItem(str(item)))
                    rowIndex = self.tblEmarahArchieve.rowCount()
                    if rowIndex == len(doblexData):
                        break
                    self.tblEmarahArchieve.insertRow(rowIndex)
            self.namespace.Handle_Status('تم البحث', 1)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_Emarah(self):
        try:
            piece_id = self.txtPieceIDEmarah.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'emarah' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from emara
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'emarah'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaEmarah.setText(str(mainData[0][0]))
                self.txtPriceEmarah.setText(str(mainData[0][1]))
                self.txtDetailsEmarah.setText(mainData[0][2])
                self.txtOwnerPhoneEmarah.setText(mainData[0][3])
                self.txtOwnerNameEmarah.setText(mainData[0][4])
                self.cbxCityEmarah.setCurrentText(mainData[0][7])
                self.cbxStreetEmarah.setCurrentText(mainData[0][5])
                self.cbxBlockEmarah.setCurrentText(mainData[0][6])
                self.cbxStatusEmarah.setCurrentText(mainData[0][8])
                self.txtRestEmarah.setText(str(mainData[0][9]))
                # fill second data
                self.txtFloorNumEmarah.setText(str(secondData[0][0]))
                self.cbxTa4tebEmarah.setCurrentText(secondData[0][1])
                if secondData[0][2] == 'نعم':
                    self.ckbxGazEmarah.setChecked(True)
                if secondData[0][3] == 'نعم':
                    self.ckbxWaterEmarah.setChecked(True)
                if secondData[0][4] == 'نعم':
                    self.ckbxElecEmarah.setChecked(True)
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images.clear()
                self.tblImgsEmarah.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsEmarah.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsEmarah.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsEmarah.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsEmarah.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceIDEmarah.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود العماره غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    # -------------------------------
    # Add | Edit | Delete VILLA Functions
    def Add_Villa(self):
        try:
            piece_id =self.txtPieceIDVilla.text().strip().replace("'", '')
            cityName = self.cbxCityVilla.currentIndex()
            streetName = self.cbxStreetVilla.currentIndex()
            blockName = self.cbxBlockVilla.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerNameVilla.text().strip().replace("'", '') == '':
                                self.txtOwnerPhoneVilla.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'villa'
                            phone= self.txtOwnerPhoneVilla.text().strip().replace("'", '')
                            price = self.txtPriceVilla.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaVilla.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusVilla.currentText()
                            premium = '0'
                            if self.cbxStatusVilla.currentIndex() == 1:
                                premium = self.txtRestVilla.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsVilla.toPlainText().strip().replace("'", '')

                            # secondary info
                            ta4teb = self.cbxTa4tebVilla.currentText()
                            floorNum = self.txtFloorNumVilla.text().strip().replace("'", "")
                            electricity = 'لا'
                            water = 'لا'
                            gaz = 'لا'
                            if self.ckbxElecVilla.isChecked():
                                electricity = 'نعم'
                            if self.ckbxWaterVilla.isChecked():
                                water = 'نعم'
                            if self.ckbxGazVilla.isChecked():
                                gaz = 'نعم'
                            villaType = self.cbxVillaType.currentText()
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into villa values
                                ('{floorNum}','{ta4teb}','{villaType}','{gaz}','{water}', '{electricity}','{piece_id}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images1:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','villa')
                            ''')
                            self.namespace.db.commit()
                            self.images1.clear()
                            self.tblImgsVilla.setRowCount(0)
                            self.Clear_Widgets(self.Vila_Properties)
                            self.txtPieceIDVilla.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة فيلا', 1)
                        else:
                            self.cbxBlockVilla.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetVilla.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityVilla.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDVilla.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Villa(self):
        try:
            piece_id =self.txtPieceIDVilla.text().strip().replace("'", '')
            cityName = self.cbxCityVilla.currentIndex()
            streetName = self.cbxStreetVilla.currentIndex()
            blockName = self.cbxBlockVilla.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerNameVilla.text().strip().replace("'", '') == '':
                                    self.txtOwnerPhoneVilla.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'villa'
                                phone= self.txtOwnerPhoneVilla.text().strip().replace("'", '')
                                price = self.txtPriceVilla.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaVilla.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusVilla.currentText()
                                premium = '0'
                                if self.cbxStatusVilla.currentIndex() == 1:
                                    premium = self.txtRestVilla.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsVilla.toPlainText().strip().replace("'", '')

                                # secondary info
                                ta4teb = self.cbxTa4tebVilla.currentText()
                                floorNum = self.txtFloorNumVilla.text().strip().replace("'", "")
                                electricity = 'لا'
                                water = 'لا'
                                gaz = 'لا'
                                if self.ckbxElecVilla.isChecked():
                                    electricity = 'نعم'
                                if self.ckbxWaterVilla.isChecked():
                                    water = 'نعم'
                                if self.ckbxGazVilla.isChecked():
                                    gaz = 'نعم'
                                villaType = self.cbxVillaType.currentText()
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'villa'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update villa set num_of_floors='{floorNum}',ta4teb_type='{ta4teb}',
                                    gaz = '{gaz}', water = '{water}', electricity = '{electricity}', villa_type ='{villaType}'
                                    where piece='{piece_id}' 
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'villa'
                                ''')
                                for img in self.images1:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','villa')
                                ''')
                                self.namespace.db.commit()
                                self.images1.clear()
                                self.tblImgsVilla.setRowCount(0)
                                self.Clear_Widgets(self.Vila_Properties)
                                self.txtPieceIDEmarah.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم تعديل فيلا', 1)
                        else:
                            self.cbxBlockVilla.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetVilla.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityVilla.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDVilla.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Villa(self):
        piece_id =self.txtPieceIDVilla.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where proprety='{piece_id}' and type = 'villa'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'villa'
                    ''')
                    self.namespace.db.commit()
                    self.images1.clear()
                    self.tblImgsVilla.setRowCount(0)
                    self.Clear_Widgets(self.Vila_Properties)
                    self.txtPieceIDVilla.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف فيلا', 1)
            else:
                self.txtPieceIDVilla.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Get_All_Villa(self):
        try:
            self.namespace.cur.execute(f'''
                    select propreties.proprety,persons.name,cities.name,streets.name,blocks.name,villa.villa_type,
                    villa.ta4teb_type,villa.num_of_floors,
                    propreties.area,propreties.price,villa.electricity,villa.gaz,villa.water,
                    propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    inner JOIN villa on propreties.proprety = villa.piece
                    where propreties.type = 'villa' and working = 'yes'
                ''')
            doblexData = self.namespace.cur.fetchall()
            print(doblexData)
            self.tblVillaArchieve.setRowCount(0)
            if len(doblexData) != 0:
                self.tblVillaArchieve.insertRow(0)
                for rowNum, row in enumerate(doblexData):
                    for colNum, item in enumerate(row):
                        self.tblVillaArchieve.setItem(rowNum, colNum, QTableWidgetItem(str(item)))
                    rowIndex = self.tblVillaArchieve.rowCount()
                    if rowIndex == len(doblexData):
                        break
                    self.tblVillaArchieve.insertRow(rowIndex)
            self.namespace.Handle_Status('تم البحث', 1)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Search_Villa(self):
        try:
            piece_id = self.txtPieceIDVilla.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'villa' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from villa
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'villa'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaVilla.setText(str(mainData[0][0]))
                self.txtPriceVilla.setText(str(mainData[0][1]))
                self.txtDetailsVilla.setText(mainData[0][2])
                self.txtOwnerPhoneVilla.setText(mainData[0][3])
                self.txtOwnerNameVilla.setText(mainData[0][4])
                self.cbxCityVilla.setCurrentText(mainData[0][7])
                self.cbxStreetVilla.setCurrentText(mainData[0][5])
                self.cbxBlockVilla.setCurrentText(mainData[0][6])
                self.cbxStatusVilla.setCurrentText(mainData[0][8])
                self.txtRestVilla.setText(str(mainData[0][9]))
                # fill second data
                self.txtFloorNumVilla.setText(str(secondData[0][0]))
                self.cbxTa4tebVilla.setCurrentText(secondData[0][1])
                self.cbxVillaType.setCurrentText(secondData[0][2])
                if secondData[0][3] == 'نعم':
                    self.ckbxGazVilla.setChecked(True)
                if secondData[0][4] == 'نعم':
                    self.ckbxWaterVilla.setChecked(True)
                if secondData[0][5] == 'نعم':
                    self.ckbxElecVilla.setChecked(True)
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images1.clear()
                self.tblImgsVilla.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsVilla.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images1.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsVilla.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsVilla.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsVilla.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceIDVilla.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    # -------------------------------
    # Add | Edit | Delete Flat Functions
    def Add_Flat(self):
        try:
            piece_id =self.txtPieceIDFlat.text().strip().replace("'", '')
            cityName = self.cbxCityFlat.currentIndex()
            streetName = self.cbxStreetFlat.currentIndex()
            blockName = self.cbxBlockFlat.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerNameFlat.text().strip().replace("'", '') == '':
                                self.txtOwnerPhoneFlat.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'flat'
                            phone= self.txtOwnerPhoneFlat.text().strip().replace("'", '')
                            price = self.txtPriceFlat.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaFlat.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusFlat.currentText()
                            premium = '0'
                            if self.cbxStatusFlat.currentIndex() == 1:
                                premium = self.txtRestFlat.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsFlat.toPlainText().strip().replace("'", '')

                            # secondary info
                            container = self.txtParentFlatID.text().strip().replace("'", "")
                            roomNum = self.txtRoomFlat.text().strip().replace("'", "")
                            wcNum = self.txtWCFlat.text().strip().replace("'", "")
                            flatType = 'normal'
                            ta4teb = self.cbxTa4tebFlat.currentText()
                            floorNum = self.txtFloorNumFlat.text().strip().replace("'", "")
                            electricity = 'لا'
                            water = 'لا'
                            gaz = 'لا'
                            if self.ckbxElecFlat.isChecked():
                                electricity = 'نعم'
                            if self.ckbxWaterFlat.isChecked():
                                water = 'نعم'
                            if self.ckbxGazFlat.isChecked():
                                gaz = 'نعم'
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into flat values
                                ('{piece_id}','{roomNum}','{wcNum}','{floorNum}','{flatType}','{ta4teb}','{gaz}',
                                '{water}','{electricity}','{container}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images2:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','flat')
                            ''')
                            self.namespace.db.commit()
                            self.images2.clear()
                            self.tblImgsFlat.setRowCount(0)
                            self.Clear_Widgets(self.Flat_Normal_propeties)
                            self.txtPieceIDFlat.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة شقه', 1)
                        else:
                            self.cbxBlockFlat.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetFlat.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityFlat.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDFlat.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Flat(self):
        try:
            piece_id =self.txtPieceIDFlat.text().strip().replace("'", '')
            cityName = self.cbxCityFlat.currentIndex()
            streetName = self.cbxStreetFlat.currentIndex()
            blockName = self.cbxBlockFlat.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerNameFlat.text().strip().replace("'", '') == '':
                                    self.txtOwnerPhoneFlat.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'flat'
                                phone= self.txtOwnerPhoneFlat.text().strip().replace("'", '')
                                price = self.txtPriceFlat.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaFlat.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusFlat.currentText()
                                premium = '0'
                                if self.cbxStatusFlat.currentIndex() == 1:
                                    premium = self.txtRestFlat.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsFlat.toPlainText().strip().replace("'", '')

                                # secondary info
                                container = self.txtParentFlatID.text().strip().replace("'", "")
                                roomNum = self.txtRoomFlat.text().strip().replace("'", "")
                                wcNum = self.txtWCFlat.text().strip().replace("'", "")
                                flatType = 'normal'
                                ta4teb = self.cbxTa4tebFlat.currentText()
                                floorNum = self.txtFloorNumFlat.text().strip().replace("'", "")
                                electricity = 'لا'
                                water = 'لا'
                                gaz = 'لا'
                                if self.ckbxElecFlat.isChecked():
                                    electricity = 'نعم'
                                if self.ckbxWaterFlat.isChecked():
                                    water = 'نعم'
                                if self.ckbxGazFlat.isChecked():
                                    gaz = 'نعم'
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'flat'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update flat set num_of_rooms='{roomNum}',num_of_bathrooms='{wcNum}',
                                    floor_number='{floorNum}',ta4teb_type='{ta4teb}',
                                    gaz = '{gaz}', water = '{water}', electricity = '{electricity}',
                                    container ='{container}'
                                    where piece='{piece_id}' 
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'flat'
                                ''')
                                for img in self.images2:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','flat')
                                ''')
                                self.namespace.db.commit()
                                self.images2.clear()
                                self.tblImgsFlat.setRowCount(0)
                                self.Clear_Widgets(self.Flat_Normal_propeties)
                                self.txtPieceIDFlat.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل شقه', 1)
                        else:
                            self.cbxBlockFlat.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetFlat.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityFlat.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDFlat.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Flat(self):
        piece_id =self.txtPieceIDFlat.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where proprety='{piece_id}' and type = 'flat'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'flat'
                    ''')
                    self.namespace.db.commit()
                    self.images2.clear()
                    self.tblImgsFlat.setRowCount(0)
                    self.Clear_Widgets(self.Flat_Normal_propeties)
                    self.txtPieceIDFlat.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف شقه', 1)
            else:
                self.txtPieceIDFlat.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Get_All_Flat(self):
        try:
            self.namespace.cur.execute(f'''
                    select propreties.proprety,persons.name,cities.name,streets.name,blocks.name,flat.container,
                    flat.ta4teb_type,propreties.price,propreties.area,flat.floor_number,flat.num_of_rooms,
                    flat.num_of_bathrooms,flat.electricity,flat.gaz,flat.water,
                    propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    inner JOIN flat on propreties.proprety = flat.piece
                    where propreties.type = 'flat' and working = 'yes'
                ''')
            doblexData = self.namespace.cur.fetchall()
            self.tblFlatArchieve.setRowCount(0)
            if len(doblexData) != 0:
                self.tblFlatArchieve.insertRow(0)
                for rowNum, row in enumerate(doblexData):
                    for colNum, item in enumerate(row):
                        self.tblFlatArchieve.setItem(rowNum, colNum, QTableWidgetItem(str(item)))
                    rowIndex = self.tblFlatArchieve.rowCount()
                    if rowIndex == len(doblexData):
                        break
                    self.tblFlatArchieve.insertRow(rowIndex)
            self.namespace.Handle_Status('تم البحث', 1)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search_Flat(self):
        try:
            piece_id = self.txtPieceIDFlat.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'flat' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from flat
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'flat'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaFlat.setText(str(mainData[0][0]))
                self.txtPriceFlat.setText(str(mainData[0][1]))
                self.txtDetailsFlat.setText(mainData[0][2])
                self.txtOwnerPhoneFlat.setText(mainData[0][3])
                self.txtOwnerNameFlat.setText(mainData[0][4])
                self.cbxCityFlat.setCurrentText(mainData[0][7])
                self.cbxStreetFlat.setCurrentText(mainData[0][5])
                self.cbxBlockFlat.setCurrentText(mainData[0][6])
                self.cbxStatusFlat.setCurrentText(mainData[0][8])
                self.txtRestFlat.setText(str(mainData[0][9]))
                # fill second data
                self.txtRoomFlat.setText(str(secondData[0][1]))
                self.txtWCFlat.setText(str(secondData[0][2]))
                self.txtFloorNumFlat.setText(str(secondData[0][3]))
                self.cbxTa4tebFlat.setCurrentText(secondData[0][5])
                if secondData[0][6] == 'نعم':
                    self.ckbxGazFlat.setChecked(True)
                if secondData[0][7] == 'نعم':
                    self.ckbxWaterFlat.setChecked(True)
                if secondData[0][8] == 'نعم':
                    self.ckbxElecFlat.setChecked(True)
                self.txtParentFlatID.setText(str(secondData[0][9]))
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images2.clear()
                self.tblImgsFlat.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsFlat.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images2.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsFlat.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsFlat.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsFlat.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceIDFlat.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    # -------------------------------
    # Add | Edit | Delete Doblex Functions
    def Add_Doblex(self):
        try:
            piece_id =self.txtPieceIDFlat_2.text().strip().replace("'", '')
            cityName = self.cbxCityFlat_2.currentIndex()
            streetName = self.cbxStreetFlat_2.currentIndex()
            blockName = self.cbxBlockFlat_2.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerNameFlat_2.text().strip().replace("'", '') == '':
                                self.txtOwnerPhoneFlat_2.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'doblex'
                            phone= self.txtOwnerPhoneFlat_2.text().strip().replace("'", '')
                            price = self.txtPriceFlat_2.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtAreaFlat_2.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatusFlat_2.currentText()
                            premium = '0'
                            if self.cbxStatusFlat_2.currentIndex() == 1:
                                premium = self.txtRestFlat_2.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetailsFlat_2.toPlainText().strip().replace("'", '')

                            # secondary info
                            container = self.txtParentFlatID_2.text().strip().replace("'", "")
                            roomNum = self.txtRoomFlat_2.text().strip().replace("'", "")
                            wcNum = self.txtWCFlat_2.text().strip().replace("'", "")
                            flatType = 'doplex'
                            ta4teb = self.cbxTa4tebFlat_2.currentText()
                            electricity = 'لا'
                            water = 'لا'
                            gaz = 'لا'
                            if self.ckbxElecFlat_2.isChecked():
                                electricity = 'نعم'
                            if self.ckbxWaterFlat_2.isChecked():
                                water = 'نعم'
                            if self.ckbxGazFlat_2.isChecked():
                                gaz = 'نعم'
                            # doplex Info
                            doplexType = self.cbxDoplexType.currentText()
                            pool = 'لا'
                            apecialEnter = 'لا'
                            innerStairs = 'لا'
                            garden = 'لا'
                            if self.ckbxPool.isChecked():
                                pool = 'نعم'
                            if self.chbxSpecialEnter.isChecked():
                                apecialEnter = 'نعم'
                            if self.chbxInnerStairs.isChecked():
                                innerStairs = 'نعم'
                            if self.ckbxGarden.isChecked():
                                garden = 'نعم'
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into flat values
                                ('{piece_id}','{roomNum}','{wcNum}','0','{flatType}','{ta4teb}','{gaz}',
                                '{water}','{electricity}','{container}')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into doplex values
                                ('{doplexType}','{pool}','{apecialEnter}','{innerStairs}','{garden}','{piece_id}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images3:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','doblex')
                            ''')
                            self.namespace.db.commit()
                            self.images3.clear()
                            self.tblImgsFlat_2.setRowCount(0)
                            self.Clear_Widgets(self.Doublex_Properties)
                            self.txtPieceIDFlat_2.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة شقه(دوبلكس)', 1)
                        else:
                            self.cbxBlockFlat_2.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetFlat_2.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityFlat_2.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDFlat_2.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Doblex(self):
        try:
            piece_id =self.txtPieceIDFlat_2.text().strip().replace("'", '')
            cityName = self.cbxCityFlat_2.currentIndex()
            streetName = self.cbxStreetFlat_2.currentIndex()
            blockName = self.cbxBlockFlat_2.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerNameFlat_2.text().strip().replace("'", '') == '':
                                    self.txtOwnerPhoneFlat_2.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                pieceType = 'doblex'
                                phone = self.txtOwnerPhoneFlat_2.text().strip().replace("'", '')
                                price = self.txtPriceFlat_2.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtAreaFlat_2.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatusFlat_2.currentText()
                                premium = '0'
                                if self.cbxStatusFlat_2.currentIndex() == 1:
                                    premium = self.txtRestFlat_2.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetailsFlat_2.toPlainText().strip().replace("'", '')

                                # secondary info
                                container = self.txtParentFlatID_2.text().strip().replace("'", "")
                                roomNum = self.txtRoomFlat_2.text().strip().replace("'", "")
                                wcNum = self.txtWCFlat_2.text().strip().replace("'", "")
                                flatType = 'doplex'
                                ta4teb = self.cbxTa4tebFlat_2.currentText()
                                electricity = 'لا'
                                water = 'لا'
                                gaz = 'لا'
                                if self.ckbxElecFlat_2.isChecked():
                                    electricity = 'نعم'
                                if self.ckbxWaterFlat_2.isChecked():
                                    water = 'نعم'
                                if self.ckbxGazFlat_2.isChecked():
                                    gaz = 'نعم'
                                # doplex Info
                                doplexType = self.cbxDoplexType.currentText()
                                pool = 'لا'
                                apecialEnter = 'لا'
                                innerStairs = 'لا'
                                garden = 'لا'
                                if self.ckbxPool.isChecked():
                                    pool = 'نعم'
                                if self.chbxSpecialEnter.isChecked():
                                    apecialEnter = 'نعم'
                                if self.chbxInnerStairs.isChecked():
                                    innerStairs = 'نعم'
                                if self.ckbxGarden.isChecked():
                                    garden = 'نعم'
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'doblex'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update flat set num_of_rooms='{roomNum}',num_of_bathrooms='{wcNum}',
                                    ta4teb_type='{ta4teb}',gaz = '{gaz}', water = '{water}', electricity = '{electricity}',
                                     container ='{container}'
                                    where piece='{piece_id}' 
                                ''')
                                self.namespace.cur.execute(f'''
                                update doplex set doplex_type='{doplexType}',pool='{pool}',special_enter='{apecialEnter}',
                                inner_stairs='{innerStairs}',garden='{garden}'
                                where piece='{piece_id}'
                            ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'doblex'
                                ''')
                                for img in self.images3:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','doblex')
                                ''')
                                self.namespace.db.commit()
                                self.images3.clear()
                                self.tblImgsFlat_2.setRowCount(0)
                                self.Clear_Widgets(self.Doublex_Properties)
                                self.txtPieceIDFlat_2.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم تعديل شقه(دوبلكس)', 1)
                        else:
                            self.cbxBlockFlat_2.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreetFlat_2.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCityFlat_2.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceIDFlat_2.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Doblex(self):
        piece_id =self.txtPieceIDFlat_2.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where proprety='{piece_id}' and type = 'doblex'
                    ''')
                    self.namespace.cur.execute(f'''
                        delete from images where piece = '{piece_id}' and piece_type = 'doblex'
                    ''')
                    self.namespace.db.commit()
                    self.images3.clear()
                    self.tblImgsFlat_2.setRowCount(0)
                    self.Clear_Widgets(self.Doublex_Properties)
                    self.txtPieceIDFlat_2.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف شقه(دوبلكس)', 1)
            else:
                self.txtPieceIDFlat_2.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Get_All_Doblex(self):
        try:
            self.namespace.cur.execute(f'''
                    select propreties.proprety,persons.name,cities.name,streets.name,blocks.name,flat.container,
                    flat.ta4teb_type,propreties.price,propreties.area,doplex.doplex_type,flat.num_of_rooms,
                    flat.num_of_bathrooms,flat.electricity,flat.gaz,flat.water,
                    doplex.pool,doplex.special_enter,doplex.inner_stairs,
                    doplex.garden,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    inner JOIN flat on propreties.proprety = flat.piece
                    inner JOIN doplex on propreties.proprety = doplex.piece
                    where propreties.type = 'doblex' and working = 'yes'
                ''')
            doblexData = self.namespace.cur.fetchall()
            self.tblDoblexArchieve.setRowCount(0)
            if len(doblexData) != 0:
                self.tblDoblexArchieve.insertRow(0)
                for rowNum, row in enumerate(doblexData):
                    for colNum, item in enumerate(row):
                        self.tblDoblexArchieve.setItem(rowNum, colNum, QTableWidgetItem(str(item)))
                    rowIndex = self.tblDoblexArchieve.rowCount()
                    if rowIndex == len(doblexData):
                        break
                    self.tblDoblexArchieve.insertRow(rowIndex)
            self.namespace.Handle_Status('تم البحث', 1)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Search_Doblex(self):
        try:
            piece_id = self.txtPieceIDFlat_2.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'doblex' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from flat
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from doplex
                    where piece = '{piece_id}'
                ''')
                doblexData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'doblex'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtAreaFlat_2.setText(str(mainData[0][0]))
                self.txtPriceFlat_2.setText(str(mainData[0][1]))
                self.txtDetailsFlat_2.setText(mainData[0][2])
                self.txtOwnerPhoneFlat_2.setText(mainData[0][3])
                self.txtOwnerNameFlat_2.setText(mainData[0][4])
                self.cbxCityFlat_2.setCurrentText(mainData[0][7])
                self.cbxStreetFlat_2.setCurrentText(mainData[0][5])
                self.cbxBlockFlat_2.setCurrentText(mainData[0][6])
                self.cbxStatusFlat_2.setCurrentText(mainData[0][8])
                self.txtRestFlat_2.setText(str(mainData[0][9]))
                # fill second data
                self.txtRoomFlat_2.setText(str(secondData[0][1]))
                self.txtWCFlat_2.setText(str(secondData[0][2]))
                self.cbxTa4tebFlat_2.setCurrentText(secondData[0][5])
                if secondData[0][6] == 'نعم':
                    self.ckbxGazFlat_2.setChecked(True)
                if secondData[0][7] == 'نعم':
                    self.ckbxWaterFlat_2.setChecked(True)
                if secondData[0][8] == 'نعم':
                    self.ckbxElecFlat_2.setChecked(True)
                self.txtParentFlatID_2.setText(str(secondData[0][9]))
                # fill doblex Info
                self.cbxDoplexType.setCurrentText(doblexData[0][0])
                if doblexData[0][1] == 'نعم':
                    self.ckbxPool.setChecked(True)
                if doblexData[0][2] == 'نعم':
                    self.chbxSpecialEnter.setChecked(True)
                if doblexData[0][3] == 'نعم':
                    self.chbxInnerStairs.setChecked(True)
                if doblexData[0][4] == 'نعم':
                    self.ckbxGarden.setChecked(True)
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images3.clear()
                self.tblImgsFlat_2.setRowCount(0)
                if len(imgData) > 0:
                    self.tblImgsFlat_2.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images3.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgsFlat_2.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgsFlat_2.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgsFlat_2.insertRow(row)
                self.namespace.Handle_Status('تم البحث', 1)
            else:
                self.txtPieceIDFlat_2.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود الفيلا غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


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

            supportedImageFormats = {'.bmp','.eps','.gif','.icns','.ico','.im','.jpg','.jpeg','.jpeg2000','.msp','.pcx', \
                                          '.png','.ppm','.sgi','.tiff','.tif','.xbm','.BMP','.EPS','.GIF','.ICNS','.ICO','.IM','.JPG','.JPEG','.JPEG2000','.MSP','.PCX', \
                                          '.PNG','.PPM','.SGI','.TIFF','.TIF','.XBM'}
            fileDlg = QFileDialog(self)
            fileDlg.setDirectory('./')
            paths = fileDlg.getOpenFileNames(filter="All Files (*.*);; JPEG (*.jpg;*.jpeg;*.jpeg2000);;GIF (*.gif);;PNG (*.png);;TIF (*.tif;*.tiff);;BMP (*.bmp);; Nikon (*.nef;*.nrw);;Sony (*.arw;*.srf;*.sr2);;Canon (*.crw;*.cr2;*.cr3)")[0]
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
