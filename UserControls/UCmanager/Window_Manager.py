from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import mysql.connector
managerUI,_ = loadUiType('./UserControls/UCmanager/UC_Manager.ui')

class window_manager(QFrame, managerUI ):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.db = namespace.db
        try:
            self.cur = self.db.cursor()
        except:
            pass
        self.manager_frames = [
            self.Frame_Manager_Cities,
            self.Frame_Manager_Blocks,
            self.Frame_Manager_Streets,

        ]
        self.Swipe_Manager_Frames(self.Frame_Manager_Cities)
        self.InitUi()
        self.Fill_Table_Cities()
        self.Fill_CbxCities()

        self.Fill_Table_Streets()
        self.Fill_Table_Blocks()
    def Swipe_Manager_Frames(self, frame):
        for frm in self.manager_frames:
            if frm == frame:
                frame.setVisible(True)
            else:
                frm.setVisible(False)

    def InitUi(self):
        # frames btns controls
        self.btn_cities_frame.clicked.connect(
            lambda: self.Swipe_Manager_Frames(self.Frame_Manager_Cities)
        )
        self.btn_streets_frame.clicked.connect(
            lambda: self.Swipe_Manager_Frames(self.Frame_Manager_Streets)
        )
        self.btn_blocks_frame.clicked.connect(
            lambda: self.Swipe_Manager_Frames(self.Frame_Manager_Blocks)
        )

        # cities btns controls
        self.btn_add_city.clicked.connect(
            lambda: self.Add_City()
        )
        self.btn_edit_city.clicked.connect(
            lambda: self.Edit_City()
        )
        self.btn_remove_city.clicked.connect(
            lambda: self.Delete_City()
        )
        self.tbl_cities.cellClicked.connect(
            lambda: (
                self.btn_edit_city.setEnabled(True),
                self.btn_remove_city.setEnabled(True),
                self.Fill_Text_Cities()
            )
        )

        #streets btns controls
        self.btn_add_street.clicked.connect(
            lambda: self.Add_Street()
        )
        self.btn_edit_street.clicked.connect(
            lambda: self.Edit_Streets()
        )
        self.btn_remove_street.clicked.connect(
            lambda: self.Delete_Streets()
        )

        self.tbl_streets.cellClicked.connect(
            lambda: (
                self.btn_edit_street.setEnabled(True),
                self.btn_remove_street.setEnabled(True),
                self.Fill_Text_Streets()
            )
        )
        #blocks btns controls
        self.btn_add_blok.clicked.connect(
            lambda: self.Add_block()
        )
        self.btn_edit_blok.clicked.connect(
            lambda: self.Edit_Blocks()
        )
        self.btn_remove_blok.clicked.connect(
            lambda: self.Delete_Blocks()
        )
        self.tbl_blocks.cellClicked.connect(
            lambda: (
                self.btn_edit_blok.setEnabled(True),
                self.btn_remove_blok.setEnabled(True),
                self.Fill_Text_Blocks()
            )
        )
        self.cbxCityName2.currentIndexChanged.connect(
            lambda: self.Fill_CbxStreet()
        )

    # cities Functions
    def Add_City(self):
        try:
            cityName = self.txtCityName.text().strip().replace("'", '')
            govName = self.txtGovName.text().strip().replace("'", '')
            if cityName != '':
                if govName != '':
                    streetsNum = self.txtStreetsNumber.text().strip().replace("'", '')
                    if streetsNum == '':
                        streetsNum = '0'
                    self.cur.execute(f'''
                        insert into cities(name, mohafza ,num_of_streets)
                         values ('{cityName}', '{govName}', '{streetsNum}')
                    ''')
                    self.db.commit()
                    self.txtCityName.setText('')
                    self.txtGovName.setText('')
                    self.txtStreetsNumber.setText('')
                    self.txtCityName.setFocus()
                    self.Fill_Table_Cities()
                    self.btn_edit_city.setEnabled(False)
                    self.btn_remove_city.setEnabled(False)
                    self.namespace.Handle_Status('تم اضافة مدينه', 1)
                else:
                    self.txtGovName.setFocus()
                    self.namespace.Handle_Status('أدخل المحافظه', 3)
            else:
                self.txtCityName.setFocus()
                self.namespace.Handle_Status('أدخل ألمدينه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Edit_City(self):
        try:
            cityID = self.tbl_cities.selectedIndexes()[0].data()
            print(cityID)
            cityName = self.txtCityName.text().strip().replace("'", '')
            govName = self.txtGovName.text().strip().replace("'", '')
            if cityName != '':
                if govName != '':
                    streetsNum = self.txtStreetsNumber.text().strip().replace("'", '')
                    if streetsNum == '':
                        streetsNum = '0'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                            update cities set name='{cityName}', mohafza='{govName}' ,num_of_streets='{streetsNum}'
                            where city_id='{cityID}'
                        ''')
                        self.db.commit()
                        self.txtCityName.setText('')
                        self.txtGovName.setText('')
                        self.txtStreetsNumber.setText('')
                        self.txtCityName.setFocus()
                        self.Fill_Table_Cities()
                        self.btn_edit_city.setEnabled(False)
                        self.btn_remove_city.setEnabled(False)
                        self.namespace.Handle_Status('تم تعديل مدينه', 1)
                else:
                    self.txtGovName.setFocus()
                    self.namespace.Handle_Status('أدخل المحافظه', 3)
            else:
                self.txtCityName.setFocus()
                self.namespace.Handle_Status('أدخل ألمدينه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Delete_City(self):
        try:
            cityID = self.tbl_cities.selectedIndexes()[0].data()
            print(cityID)
            cityName = self.txtCityName.text().strip().replace("'", '')
            govName = self.txtGovName.text().strip().replace("'", '')
            if cityName != '':
                if govName != '':
                    streetsNum = self.txtStreetsNumber.text().strip().replace("'", '')
                    if streetsNum == '':
                        streetsNum = '0'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                            delete from cities where city_id='{cityID}'
                        ''')
                        self.db.commit()
                        self.txtCityName.setText('')
                        self.txtGovName.setText('')
                        self.txtStreetsNumber.setText('')
                        self.txtCityName.setFocus()
                        self.Fill_Table_Cities()
                        self.btn_edit_city.setEnabled(False)
                        self.btn_remove_city.setEnabled(False)
                        self.namespace.Handle_Status('تم حذف مدينه', 1)
                else:
                    self.txtGovName.setFocus()
                    self.namespace.Handle_Status('أدخل المحافظه', 3)
            else:
                self.txtCityName.setFocus()
                self.namespace.Handle_Status('أدخل ألمدينه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_Table_Cities(self):
        try:
            self.cur.execute('''
            select * from cities
            ''')
            tblCities = self.cur.fetchall()
            self.tbl_cities.setRowCount(0)
            if len(tblCities) != 0:
                self.tbl_cities.insertRow(0)
                for rownum, row in enumerate(tblCities):
                    for colnum, col in enumerate(row):
                        self.tbl_cities.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_cities.rowCount()
                    if rowPosition == len(tblCities):
                        break
                    self.tbl_cities.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Text_Cities(self):
        rowData = self.tbl_cities.selectedIndexes()
        self.txtCityName.setText(str(rowData[1].data()))
        self.txtGovName.setText(rowData[2].data())
        self.txtStreetsNumber.setText(str(rowData[3].data()))

    # -----------------------------------------------
    # streets Finctions
    def Add_Street(self):
        try:
            streetName = self.txtStreetName.text().strip().replace("'", '')
            cityName = self.cbxCityName.currentIndex()
            if streetName != '':
                if cityName >= 0:
                    blocksNum = self.txtBlockNumber.text().strip().replace("'", '')
                    if blocksNum == '':
                        blocksNum = '0'
                    self.cur.execute(f'''
                        insert into streets(name, city  ,num_of_blocks)
                         values ('{streetName}', '{self.citiesInfo[cityName][0]}', '{blocksNum}')
                    ''')
                    self.db.commit()
                    self.txtStreetName.setText('')
                    self.cbxCityName.setCurrentIndex(-1)
                    self.txtBlockNumber.setText('')
                    self.txtStreetName.setFocus()
                    self.Fill_Table_Streets()
                    self.btn_edit_street.setEnabled(False)
                    self.btn_remove_street.setEnabled(False)
                    self.Fill_CbxStreet()
                    self.namespace.Handle_Status('تم اضافة حى', 1)
                else:
                    self.cbxCityName.setFocus()
                    self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtStreetName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Edit_Streets(self):
        try:
            streetID = self.tbl_streets.selectedIndexes()[0].data()
            streetName = self.txtStreetName.text().strip().replace("'", '')
            cityName = self.cbxCityName.currentIndex()
            if streetName != '':
                if cityName >= 0:
                    blocksNum = self.txtBlockNumber.text().strip().replace("'", '')
                    if blocksNum == '':
                        blocksNum = '0'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                            update streets set
                            name='{streetName}', city='{self.citiesInfo[cityName][0]}'  ,num_of_blocks='{blocksNum}'
                            where street_id='{streetID}'
                        ''')
                        self.db.commit()
                        self.txtStreetName.setText('')
                        self.cbxCityName.setCurrentIndex(-1)
                        self.txtBlockNumber.setText('')
                        self.txtStreetName.setFocus()
                        self.Fill_Table_Streets()
                        self.btn_edit_street.setEnabled(False)
                        self.btn_remove_street.setEnabled(False)
                        self.Fill_CbxStreet()
                        self.namespace.Handle_Status('تم تعديل حى', 1)
                else:
                    self.cbxCityName.setFocus()
                    self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtStreetName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Delete_Streets(self):
        try:
            streetID = self.tbl_streets.selectedIndexes()[0].data()
            streetName = self.txtStreetName.text().strip().replace("'", '')
            cityName = self.cbxCityName.currentIndex()
            if streetName != '':
                if cityName >= 0:
                    blocksNum = self.txtBlockNumber.text().strip().replace("'", '')
                    if blocksNum == '':
                        blocksNum = '0'
                    msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )
                    if msgbx == QMessageBox.Yes:
                        self.cur.execute(f'''
                            delete from streets 
                            where street_id='{streetID}'
                        ''')
                        self.db.commit()
                        self.txtStreetName.setText('')
                        self.cbxCityName.setCurrentIndex(-1)
                        self.txtBlockNumber.setText('')
                        self.txtStreetName.setFocus()
                        self.Fill_Table_Blocks()
                        self.btn_edit_blok.setEnabled(False)
                        self.btn_remove_blok.setEnabled(False)
                        self.Fill_CbxStreet()
                        self.namespace.Handle_Status('تم حذف حى', 1)
                else:
                    self.cbxCityName.setFocus()
                    self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtStreetName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_Table_Streets(self):
        try:
            self.cur.execute('''
            select streets.street_id, streets.name, cities.name, streets.num_of_blocks from streets
            join cities on cities.city_id = streets.city
            ''')
            tblٍStreets = self.cur.fetchall()
            self.tbl_streets.setRowCount(0)
            if len(tblٍStreets) != 0:
                self.tbl_streets.insertRow(0)
                for rownum, row in enumerate(tblٍStreets):
                    for colnum, col in enumerate(row):
                        self.tbl_streets.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_streets.rowCount()
                    if rowPosition == len(tblٍStreets):
                        break
                    self.tbl_streets.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Text_Streets(self):
        rowData = self.tbl_streets.selectedIndexes()
        self.txtStreetName.setText(str(rowData[1].data()))
        self.cbxCityName.setCurrentText(rowData[2].data())
        self.txtBlockNumber.setText(str(rowData[3].data()))

    def Fill_CbxCities(self):
        try:
            self.cur.execute('''
                select city_id, name from cities
            ''')
            self.citiesInfo = self.cur.fetchall()
            for city in self.citiesInfo:
                self.cbxCityName.addItem(city[1])
                self.cbxCityName2.addItem(city[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    #------------------------------------------------------------------
    #Blocks Function
    def Add_block(self):
        try:
            blockName = self.txtBlockName.text().strip().replace("'", '')
            cityName = self.cbxCityName2.currentIndex()
            streetName = self.cbxStreetName.currentIndex()
            if blockName != '':
                if cityName >= 0:
                    if streetName >= 0:
                        numPieces = self.txtNumPieces.text().strip().replace("'", '')
                        if numPieces == '':
                            numPieces = '0'
                        self.cur.execute(f'''
                        insert into blocks(name, num_of_pieces ,street ,city )
                        values 
                        ('{blockName}', '{numPieces}','{self.streetsInfo[streetName][0]}','{self.citiesInfo[cityName][0]}')
                        ''')
                        self.db.commit()
                        self.txtStreetName.setText('')
                        self.cbxCityName.setCurrentIndex(-1)
                        self.txtBlockNumber.setText('')
                        self.txtStreetName.setFocus()
                        self.Fill_Table_Blocks()
                        self.btn_edit_blok.setEnabled(False)
                        self.btn_remove_blok.setEnabled(False)
                        self.namespace.Handle_Status('تم اضافة بلوك', 1)
                    else:
                        self.cbxCityName.setFocus()
                        self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtStreetName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_CbxStreet(self):
        try:
            cityName = self.cbxCityName2.currentText()
            self.cur.execute(f'''
                select streets.street_id, streets.name from streets
                join cities on cities.city_id = streets.city
                and cities.name='{cityName}'
            ''')
            self.streetsInfo = self.cur.fetchall()
            self.cbxStreetName.clear()
            for city in self.streetsInfo:
                self.cbxStreetName.addItem(city[1])
            print('hi')
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Table_Blocks(self):
        try:
            #block_id name num_of_pieces street city
            self.cur.execute('''
            select blocks.block_id, blocks.name, cities.name,streets.name, blocks.num_of_pieces from blocks
            join cities on cities.city_id = blocks.city 
            join streets on streets.street_id=blocks.street
            ''')
            tblٍblocks = self.cur.fetchall()
            self.tbl_blocks.setRowCount(0)
            if len(tblٍblocks) != 0:
                self.tbl_blocks.insertRow(0)
                for rownum, row in enumerate(tblٍblocks):
                    for colnum, col in enumerate(row):
                        self.tbl_blocks.setItem(rownum, colnum, QTableWidgetItem(str(col)))
                    rowPosition = self.tbl_blocks.rowCount()
                    if rowPosition == len(tblٍblocks):
                        break
                    self.tbl_blocks.insertRow(rowPosition)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Edit_Blocks(self):
        try:
            # block_id name num_of_pieces street city tbl_blocks
            block_id = self.tbl_blocks.selectedIndexes()[0].data()
            name = self.txtBlockName.text().strip().replace("'", '')
            cityName2 = self.cbxCityName2.currentIndex()
            StreetName = self.cbxStreetName.currentIndex()
            if name != '':
                if cityName2 >= 0:
                    if StreetName >= 0:
                        numPieces = self.txtNumPieces.text().strip().replace("'", '')
                        if numPieces == '':
                           numPieces = '0'
                        msgbx = QMessageBox.warning(
                        self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )
                        if msgbx == QMessageBox.Yes:
                            self.cur.execute(f'''
                                   update blocks set
                                   name='{name}',
                                   city='{self.citiesInfo[cityName2][0]}',
                                   street='{self.streetsInfo[StreetName][0]}'
                                   ,num_of_pieces='{numPieces}'
                                   where block_id='{block_id}'
                            ''')
                            self.db.commit()
                            self.db.commit()
                            self.txtBlockName.setText('')
                            self.cbxCityName2.setCurrentIndex(-1)
                            self.txtNumPieces.setText('')
                            self.txtBlockName.setFocus()
                            self.Fill_Table_Blocks()
                            self.btn_edit_street.setEnabled(False)
                            self.btn_remove_street.setEnabled(False)
                            self.namespace.Handle_Status('تم تعديل بلوك', 1)
                    else:
                        self.cbxCityName.setFocus()
                        self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtBlockName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Delete_Blocks(self):
        try:
            blockID = self.tbl_blocks.selectedIndexes()[0].data()
            name = self.txtBlockName.text().strip().replace("'", '')
            cityName = self.cbxCityName2.currentIndex()
            StreetName = self.cbxStreetName.currentIndex()
            if name != '':
                if cityName >= 0:
                    if StreetName >= 0:
                        Numpieces = self.txtNumPieces.text().strip().replace("'", '')
                        if Numpieces == '':
                            Numpieces = '0'
                        msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد الحذف !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                        )
                        if msgbx == QMessageBox.Yes:
                            self.cur.execute(f'''
                                   delete from blocks 
                                   where block_id='{blockID}'
                               ''')
                            self.db.commit()
                            self.txtBlockName.setText('')
                            self.cbxCityName2.setCurrentIndex(-1)
                            self.cbxStreetName.setCurrentIndex(-1)
                            self.txtNumPieces.setText('')
                            self.txtBlockName.setFocus()
                            self.Fill_Table_Blocks()
                            self.btn_edit_blok.setEnabled(False)
                            self.btn_remove_blok.setEnabled(False)
                            self.namespace.Handle_Status('تم حذف بلوك', 1)
                    else:
                        self.cbxCityName.setFocus()
                        self.namespace.Handle_Status('أدخل المدينه', 3)
            else:
                self.txtBlockName.setFocus()
                self.namespace.Handle_Status('أدخل الحى', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:
            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_Text_Blocks(self):
        rowData = self.tbl_blocks.selectedIndexes()
        self.txtBlockName.setText(str(rowData[1].data()))
        self.cbxCityName2.setCurrentText(rowData[2].data())
        self.cbxStreetName.setCurrentText(rowData[3].data())
        self.txtNumPieces.setText(str(rowData[4].data()))
