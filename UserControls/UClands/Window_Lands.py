from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import mysql.connector
import os

landsUI,_ = loadUiType('./UserControls/UClands/UC_Lands.ui')

class window_lands(QFrame, landsUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.InitUi()
        self.Init_Events()
        self.Handle_Btn()
        self.Handle_Function()
        self.images = []
        self.lands_list.setCurrentRow(0)

    def InitUi(self):
        self.lands_panels = [
            self.Lands,
            self.Lands_archieve,
        ]


    def View_Target_Frame(self, parent, child):
        for frame in parent:
            if frame == parent[child]:
                frame.setVisible(True)
            else:
                frame.setVisible(False)

    def Init_Events(self):
        self.lands_list.currentRowChanged.connect(
            lambda: (
                self.View_Target_Frame(self.lands_panels, self.lands_list.currentRow()),
                self.Lands_Info.setFocus()
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


    def Handle_Function(self):
        self.Fill_CbxCities()

    def Handle_Btn(self):
        self.btn_add_land.clicked.connect(
            lambda: self.Add_land()
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
            print(type(er))
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
            print(type(er))
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
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Fill_CbxOwner(self):
        try:
            self.cur.execute('''
                select owner_id, name from owners
            ''')
            self.ownersInfo = self.cur.fetchall()
            for owner in self.ownersInfo:
                self.cbxStreetName.addItem(owner[1])
        except AttributeError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء5 الاتصال بمطور البرنامج', QMessageBox.Ok)


    def Add_land(self):
        try:
            piece_id =self.txtpiece.text().strip().replace("'", '')
            cityName = self.cbxCity.currentIndex()
            streetName = self.cbxStreet.currentIndex()
            blockName = self.cbxBlock.currentIndex()
            if piece_id != '':
                if cityName >= 0:
                    if streetName >= 0:
                        if blockName >= 0:
                            owner = self.cbxowner.currentIndex()
                            phone= self.txtphone.text().strip().replace("'", '')
                            mahgoz="لا"
                            if mahgoz == "لم يحدد" :
                                if self.chxmahgoz.isChecked():
                                    mahgoz="ارض محجوز"
                                    self.chxonther.setChecked(False)
                                if self.chxonther.isChecked():
                                    mahgoz="اماكن اخري "
                                    self.chxmahgoz.setChecked(False)
                            type_land = self.cbxtypeland.currentIndex()
                            price = self.txtprice.text().strip().replace("'", '')
                            if price == '':
                                price = 'لم يحدد'
                            area = self.txtarea.text().strip().replace("'", '')
                            if area == '':
                                area = 'لم يحدد'
                            status =self.cbxstatus.currentIndex()
                            premium = self.txtpremium.text().strip().replace("'", '')
                            if price == '':
                                premium = 'لم يحدد'
                            if self.chxover.isChecked():
                                self.txtoffer.setEnabled(True)
                            # details = self.txtdetails.text().strip().replace("'", '')
                            # if details == '':
                            #     details = 'لم يحدد تفاصيل للارض'


                            #self.cur.execute(f'''
                            #insert into lands(name, num_of_pieces ,street ,city )
                            #values
                            #('{blockName}', '{numPieces}','{self.streetsInfo[streetName][0]}','{self.citiesInfo[cityName][0]}')
                            #''')

                            # self.namespace.db.commit()
                            self.Clear_Widgets()
                            ##foucsAgain
                            self.txtpiece.setFocus()
                            self.btn_edit_land.setEnabled(False)
                            self.btn_remove_land.setEnabled(False)

                            self.namespace.Handle_Status('تم اضافة ارض', 1)

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
                self.txtpiece.setFocus()
                self.namespace.Handle_Status('أدخل رقم القطعه', 3)

        except mysql.connector.errors.OperationalError:
            self.namespace.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.namespace.MainFrame.setEnabled(False)
        except Exception as er:
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Edit_land(self):
        pass
    def Delete_land(self):
        pass
    def Fill_Text_Lands(self):
        pass

    def Clear_Widgets(self):
        for child in self.Lands.children():
            if isinstance(child, QLineEdit):
                child.setText('')
            if isinstance(child, QComboBox):
                child.setCurrentIndex(-1)
            if isinstance(child, QCheckBox):
                child.setChecked(False)


    @property
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
                header = self.tblImgs.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.Stretch)
        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)

    def Remove_Selected_Imgs(self):

        try:
            if self.tblImgs.rowCount() != 0:
                selectedImgs = self.tblImgs.selectionModel().selectedRows()
                for img in selectedImgs:
                    print(img.row())
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
                    header = self.tblImgs.horizontalHeader()
                    header.setSectionResizeMode(0, QHeaderView.Stretch)

        except Exception as er:
            print(type(er))
            QMessageBox.critical(self, 'خطأ تقنى', f'{er}\n الرجاء الاتصال بمطور البرنامج', QMessageBox.Ok)
