from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import mysql.connector
import os
import shutil

factoriesUI,_ = loadUiType('./UserControls/UCfactories/UC_Factories.ui')

class widnow_factory(QFrame, factoriesUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.InitUi()
        self.Handle_Events()
        self.Handle_Btn()
        self.Handle_Function()
        self.factory_list.setCurrentRow(0)
        self.images = []

    def InitUi(self):
        self.sena3i_panels = [
            self.Factory_Properties,
            self.Factory_Archiev,
        ]
        header = self.tblImgs.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)


    def View_Target_Frame(self, parent, child):
        for frame in parent:
            if frame == parent[child]:
                frame.setVisible(True)
            else:
                frame.setVisible(False)

    def Handle_Events(self):
        self.factory_list.currentRowChanged.connect(
            lambda: (
                self.View_Target_Frame(self.sena3i_panels, self.factory_list.currentRow()),
                self.Factory_Info.setFocus()
            )
        )
        self.cbxCity.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxStreet()
        )
        self.cbxStreet.currentIndexChanged.connect(
            lambda:
                self.Fill_CbxBlock()
        )
        self.cbxStatus.currentIndexChanged.connect(
            lambda: (
                self.txtRest.setEnabled(True) if self.cbxStatus.currentIndex() == 1
                else self.txtRest.setEnabled(False), self.txtRest.setText('')
            )
        )
        self.cbxFactoryType.currentIndexChanged.connect(
            lambda: (
                self.txtGamalonDetails.setEnabled(True) if self.cbxFactoryType.currentIndex() == 1
                else self.txtGamalonDetails.setEnabled(False), self.txtGamalonDetails.setText('')
            )
        )
    def Handle_Btn(self):
        self.btn_add_msn3.clicked.connect(
            lambda: self.Add_Factory()
        )
        self.btn_edit_msn3.clicked.connect(
            lambda: self.Edit_Factory()
        )
        self.btn_remove_msn3.clicked.connect(
            lambda: self.Delete_Factory()
        )
        self.btn_add_img.clicked.connect(
            lambda: self.Get_Imgs
        )

        self.btn_remove_img.clicked.connect(
            lambda: self.Remove_Selected_Imgs()
        )
        self.btn_show_imgs.clicked.connect(
            lambda: (
                self.namespace.Open_Galary(self.images) if len(self.images) != 0 else None
            )
        )

        self.btnSearch.clicked.connect(
            lambda: self.Search()
        )
        self.txtOwnerPhone.textChanged.connect(
            lambda: self.Check_Owner()
        )
    def Handle_Function(self):
        self.Fill_CbxCities()
        self.Get_Owners_Info()
    # ----------------------------
    # Factories Info Events

    def Fill_CbxStreet(self):
        try:
            self.cbxStreet.setEnabled(True)
            self.namespace.cur.execute(f'''
                select street_id, name from streets
                where city = '{self.citiesInfo[self.cbxCity.currentIndex()][0]}'
            ''')
            self.streetsInfo = self.namespace.cur.fetchall()
            self.cbxStreet.clear()
            for street in self.streetsInfo:
                self.cbxStreet.addItem(street[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Fill_CbxBlock(self):
        try:
            self.cbxBlock.setEnabled(True)
            self.namespace.cur.execute(f'''
                select block_id, name from blocks
                where street= '{ self.streetsInfo[self.cbxStreet.currentIndex()][0]}'
            ''')
            self.blocksInfo = self.namespace.cur.fetchall()
            self.cbxBlock.clear()
            for block in self.blocksInfo:
                self.cbxBlock.addItem(block[1])
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
                self.cbxCity.addItem(city[1])
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
            ownerCompleter = QCompleter( self.ownerPhonesList)
            self.txtOwnerPhone.setCompleter(ownerCompleter)
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Check_Owner(self):
        if self.txtOwnerPhone.text().strip().replace("'","") in self.ownerPhonesList:
            name = self.ownerPhonesList.index(self.txtOwnerPhone.text().strip().replace("'",""))
            self.txtOwnerName.setText(self.ownerNamesList[name])
        else:
            self.txtOwnerName.setText('')

    def Add_Factory(self):
        try:
            piece_id =self.txtPieceID.text().strip().replace("'", '')
            cityName = self.cbxCity.currentIndex()
            streetName = self.cbxStreet.currentIndex()
            blockName = self.cbxBlock.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            if self.txtOwnerName.text().strip().replace("'", '') == '':
                                self.txtOwnerPhone.setFocus()
                                self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                return
                            # main Info
                            pieceType = 'factory'
                            phone= self.txtOwnerPhone.text().strip().replace("'", '')
                            price = self.txtPrice.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtArea.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status = self.cbxStatus.currentText()
                            premium = '0'
                            if self.cbxStatus.currentIndex() == 1:
                                premium = self.txtRest.text().strip().replace("'", '')
                            if premium == '':
                                premium = 'لم يحدد'
                            details = self.txtDetails.toPlainText().strip().replace("'", '')

                            # secondary info
                            factoryType = self.cbxFactoryType.currentText()
                            gamalonDetails = ''
                            if self.cbxFactoryType.currentIndex() == 1:
                                gamalonDetails = self.txtGamalonDetails.toPlainText().strip().replace("'", '')
                            # insert into Database
                            self.namespace.cur.execute(f'''
                                insert into propreties values
                                ('{piece_id}', '{pieceType}','{area}','{price}','{details}',
                                '{phone}','{self.streetsInfo[streetName][0]}','{self.blocksInfo[blockName][0]}',
                                '{self.citiesInfo[cityName][0]}','{status}','{premium}','yes')
                            ''')
                            self.namespace.cur.execute(f'''
                                insert into factories values
                                ('{factoryType}', '{piece_id}','{gamalonDetails}')
                            ''')
                            # Convert Images to Byte and Insert them into Database

                            for img in self.images:
                                self.namespace.cur.execute(f'''
                                insert into images values
                                (LOAD_FILE('{img}'), '{img}','{piece_id}','factory')
                            ''')
                            self.namespace.db.commit()
                            self.images.clear()
                            self.tblImgs.setRowCount(0)
                            self.Clear_Widgets()
                            self.txtPieceID.setFocus()
                            try:
                                shutil.rmtree('tempImg')
                            except:
                                pass
                            self.namespace.Handle_Status('تم اضافة مصنع', 1)
                        else:
                            self.cbxBlock.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreet.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCity.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceID.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.IntegrityError:
            self.namespace.Handle_Status('الكود مسجل بالفعل!', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_Factory(self):
        try:
            piece_id =self.txtPieceID.text().strip().replace("'", '')
            cityName = self.cbxCity.currentIndex()
            streetName = self.cbxStreet.currentIndex()
            blockName = self.cbxBlock.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            msgbx = QMessageBox.warning(
                            self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msgbx == QMessageBox.Yes:
                                if self.txtOwnerName.text().strip().replace("'", '') == '':
                                    self.txtOwnerPhone.setFocus()
                                    self.namespace.Handle_Status('تأكد من رقم المالك', 3)
                                    return
                                # main Info
                                phone= self.txtOwnerPhone.text().strip().replace("'", '')
                                price = self.txtPrice.text().strip().replace("'", '')
                                if price == '':
                                    price = 'لم يحدد'
                                area = self.txtArea.text().strip().replace("'", '')
                                if area == '':
                                    area = 'لم يحدد'
                                status = self.cbxStatus.currentText()
                                premium = '0'
                                if self.cbxStatus.currentIndex() == 1:
                                    premium = self.txtRest.text().strip().replace("'", '')
                                if premium == '':
                                    premium = 'لم يحدد'
                                details = self.txtDetails.toPlainText().strip().replace("'", '')

                                # secondary info
                                factoryType = self.cbxFactoryType.currentText()
                                gamalonDetails = ''
                                if self.cbxFactoryType.currentIndex() == 1:
                                    gamalonDetails = self.txtGamalonDetails.toPlainText().strip().replace("'", '')
                                # insert into Database
                                self.namespace.cur.execute(f'''
                                    update propreties set area='{area}', price='{price}',details='{details}',
                                    owner='{phone}',street='{self.streetsInfo[streetName][0]}',
                                    block='{self.blocksInfo[blockName][0]}',
                                    city='{self.citiesInfo[cityName][0]}',status='{status}',rest_debt='{premium}'
                                    where proprety = '{piece_id}' and type = 'factory'
                                ''')
                                self.namespace.cur.execute(f'''
                                    update factories set type='{factoryType}',gamalon_details='{gamalonDetails}'
                                    where piece='{piece_id}'
                                ''')
                                # Convert Images to Byte and Insert them into Database
                                self.namespace.cur.execute(f'''
                                delete from images where piece = '{piece_id}' and piece_type = 'factory'
                                ''')
                                for img in self.images:
                                    self.namespace.cur.execute(f'''
                                    insert into images values
                                    (LOAD_FILE('{img}'), '{img}','{piece_id}','factory')
                                ''')
                                self.namespace.db.commit()
                                self.images.clear()
                                self.tblImgs.setRowCount(0)
                                self.Clear_Widgets()
                                self.txtPieceID.setFocus()
                                try:
                                    shutil.rmtree('tempImg')
                                except:
                                    pass
                                self.namespace.Handle_Status('تم تعديل مصنع', 1)
                        else:
                            self.cbxBlock.setFocus()
                            self.namespace.Handle_Status('أدخل البلوك', 3)
                    else:
                        self.cbxStreet.setFocus()
                        self.namespace.Handle_Status('أدخل الحي', 3)
                else:
                    self.cbxCity.setFocus()
                    self.namespace.Handle_Status('أدخل المدينة', 3)
            else:
                self.txtPieceID.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Delete_Factory(self):
        piece_id =self.txtPieceID.text().strip().replace("'", '')
        try:
            if piece_id != '':
                msgbx = QMessageBox.warning(
                self, 'تحذير', 'تأكيد التعديل !', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msgbx == QMessageBox.Yes:
                    self.namespace.cur.execute(f'''
                        update propreties set working = 'no'
                        where piece='{piece_id}' and type = 'factory'
                    ''')
                    self.namespace.db.commit()
                    self.images.clear()
                    self.tblImgs.setRowCount(0)
                    self.Clear_Widgets()
                    self.txtPieceID.setFocus()
                    try:
                        shutil.rmtree('tempImg')
                    except:
                        pass
                    self.namespace.Handle_Status('تم حذف مصنع', 1)
            else:
                self.txtPieceID.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except mysql.connector.errors.IntegrityError:

            self.namespace.Handle_Status('لا يمكن مسح البيانات', 2)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Search(self):
        try:
            piece_id = self.txtPieceID.text().strip().replace("'", '')
            if piece_id != '':
                self.namespace.cur.execute(f'''
                    select propreties.area,propreties.price,propreties.details,propreties.owner,persons.name,
                    streets.name,blocks.name,cities.name,propreties.status,propreties.rest_debt
                    from propreties
                    inner JOIN persons on propreties.owner = persons.phone1
                    inner JOIN streets on propreties.street = streets.street_id
                    inner join blocks on propreties.block = blocks.block_id
                    inner JOIN cities on propreties.city = cities.city_id
                    where propreties.proprety = '{piece_id}' and type = 'factory' and working = 'yes'
                ''')
                mainData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from factories
                    where piece = '{piece_id}'
                ''')
                secondData = self.namespace.cur.fetchall()
                self.namespace.cur.execute(f'''
                    select * from images
                    where piece = '{piece_id}' and piece_type = 'factory'
                ''')
                imgData = self.namespace.cur.fetchall()
                # fill main data
                self.txtArea.setText(str(mainData[0][0]))
                self.txtPrice.setText(str(mainData[0][1]))
                self.txtDetails.setText(mainData[0][2])
                self.txtOwnerPhone.setText(mainData[0][3])
                self.txtOwnerName.setText(mainData[0][4])
                self.cbxStreet.setCurrentText(mainData[0][5])
                self.cbxBlock.setCurrentText(mainData[0][6])
                self.cbxCity.setCurrentText(mainData[0][7])
                self.cbxStatus.setCurrentText(mainData[0][8])
                self.txtRest.setText(str(mainData[0][9]))
                # fill second data
                self.cbxFactoryType.setCurrentText(secondData[0][0])
                self.txtGamalonDetails.setText(str(secondData[0][2]))
                tempImg = 'tempimg'
                try:
                    shutil.rmtree(tempImg)
                except:
                    pass
                os.mkdir(tempImg)
                self.images.clear()
                if len(imgData) > 0:
                    self.tblImgs.setRowCount(0)
                    self.tblImgs.insertRow(0)
                    for round, img in enumerate(imgData):
                        path = f'E:/my_pc/Wehdaaaan/{tempImg}/{img[1].split("/")[-1]}'
                        self.images.append(path)
                        with open(path, 'wb') as file:
                            file.write(img[0])
                        self.tblImgs.setItem(round, 0, QTableWidgetItem(f'{img[1].split("/")[-1]}'))
                        row = self.tblImgs.rowCount()
                        if row == len(imgData):
                            break
                        self.tblImgs.insertRow(row)
            else:
                self.txtPieceID.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)
        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except IndexError:
             self.namespace.Handle_Status('كود المصنع غير مسجل', 2)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Clear_Widgets(self):
        for child in self.Factory_Properties.children():
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

    def Get_Imgs(self):
        try:
            supportedImageFormats = {'.bmp','.eps','.gif','.icns','.ico','.im','.jpg','.jpeg','.jpeg2000','.msp','.pcx', \
                                          '.png','.ppm','.sgi','.tiff','.tif','.xbm','.BMP','.EPS','.GIF','.ICNS','.ICO','.IM','.JPG','.JPEG','.JPEG2000','.MSP','.PCX', \
                                          '.PNG','.PPM','.SGI','.TIFF','.TIF','.XBM'}
            fileDlg = QFileDialog(self)
            fileDlg.setDirectory('./')
            paths = fileDlg.getOpenFileNames(filter="All Files (*.*);; JPEG (*.jpg;*.jpeg;*.jpeg2000);;GIF (*.gif);;PNG (*.png);;TIF (*.tif;*.tiff);;BMP (*.bmp);; Nikon (*.nef;*.nrw);;Sony (*.arw;*.srf;*.sr2);;Canon (*.crw;*.cr2;*.cr3)")[0]
            if len(paths) != 0:
                rowIndex = self.tblImgs.rowCount()
                if rowIndex == 0:
                    self.tblImgs.insertRow(0)
                else:
                    self.tblImgs.insertRow(rowIndex)

                for row, path in enumerate(paths):
                    if not path == '':
                        if not (os.path.splitext(path)[1] in supportedImageFormats):
                            self.namespace.Handle_Status("Not supported image type!", 2)
                            return
                    else:
                        return
                    self.images.append(path)
                    imgName = str(path).split('/')
                    self.tblImgs.setItem(rowIndex + row, 0, QTableWidgetItem(str(imgName[-1])))
                    rowPosition = self.tblImgs.rowCount()
                    if rowPosition == len(paths) + rowIndex:
                        break
                    self.tblImgs.insertRow(rowPosition)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Remove_Selected_Imgs(self):

        try:
            if self.tblImgs.rowCount() != 0:
                selectedImgs = self.tblImgs.selectionModel().selectedRows()
                for img in selectedImgs:
                    del self.images[img.row()]
                self.tblImgs.setRowCount(0)
                if len(self.images) != 0:
                    self.tblImgs.insertRow(0)
                    for row, path in enumerate(self.images):

                        imgName = str(path).split('/')
                        self.tblImgs.setItem(row, 0, QTableWidgetItem(str(imgName[-1])))
                        rowPosition = self.tblImgs.rowCount()
                        if rowPosition == len(self.images):
                            break
                        self.tblImgs.insertRow(rowPosition)

        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

