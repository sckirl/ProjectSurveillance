# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTabWidget, QTableView,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 720)
        MainWindow.setMaximumSize(QSize(900, 720))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(4, -1, 871, 701))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabBarAutoHide(False)
        self.CameraTab = QWidget()
        self.CameraTab.setObjectName(u"CameraTab")
        self.verticalLayout_2 = QVBoxLayout(self.CameraTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.videoDisplayWidget = QLabel(self.CameraTab)
        self.videoDisplayWidget.setObjectName(u"videoDisplayWidget")
        self.videoDisplayWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.videoDisplayWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.videoDisplayWidget)

        self.readButton = QPushButton(self.CameraTab)
        self.readButton.setObjectName(u"readButton")
        self.readButton.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_2.addWidget(self.readButton)

        self.databaseLbl = QLabel(self.CameraTab)
        self.databaseLbl.setObjectName(u"databaseLbl")
        self.databaseLbl.setMaximumSize(QSize(10000, 30))

        self.verticalLayout_2.addWidget(self.databaseLbl)

        self.databaseEdit = QLineEdit(self.CameraTab)
        self.databaseEdit.setObjectName(u"databaseEdit")

        self.verticalLayout_2.addWidget(self.databaseEdit)

        self.cameraLbl = QLabel(self.CameraTab)
        self.cameraLbl.setObjectName(u"cameraLbl")
        self.cameraLbl.setMaximumSize(QSize(10000, 30))

        self.verticalLayout_2.addWidget(self.cameraLbl)

        self.CameraComboBox = QComboBox(self.CameraTab)
        self.CameraComboBox.setObjectName(u"CameraComboBox")
        self.CameraComboBox.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_2.addWidget(self.CameraComboBox)

        self.tabWidget.addTab(self.CameraTab, "")
        self.TableTab = QWidget()
        self.TableTab.setObjectName(u"TableTab")
        self.tableView = QTableView(self.TableTab)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(15, 21, 851, 561))
        self.loadBtn = QPushButton(self.TableTab)
        self.loadBtn.setObjectName(u"loadBtn")
        self.loadBtn.setGeometry(QRect(400, 620, 100, 32))
        self.tabWidget.addTab(self.TableTab, "")
        self.DetailsTab = QWidget()
        self.DetailsTab.setObjectName(u"DetailsTab")
        self.DetailsTab.setEnabled(True)
        self.verticalLayoutWidget = QWidget(self.DetailsTab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 831, 611))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.captureDisplayWidget = QLabel(self.verticalLayoutWidget)
        self.captureDisplayWidget.setObjectName(u"captureDisplayWidget")

        self.verticalLayout.addWidget(self.captureDisplayWidget)

        self.MapWebView = QLabel(self.verticalLayoutWidget)
        self.MapWebView.setObjectName(u"MapWebView")

        self.verticalLayout.addWidget(self.MapWebView)

        self.latitudeLbl = QLabel(self.verticalLayoutWidget)
        self.latitudeLbl.setObjectName(u"latitudeLbl")
        self.latitudeLbl.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.latitudeLbl)

        self.latitudeEdit = QLineEdit(self.verticalLayoutWidget)
        self.latitudeEdit.setObjectName(u"latitudeEdit")

        self.verticalLayout.addWidget(self.latitudeEdit)

        self.altitudeLbl = QLabel(self.verticalLayoutWidget)
        self.altitudeLbl.setObjectName(u"altitudeLbl")
        self.altitudeLbl.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.altitudeLbl)

        self.altitudeEdit = QLineEdit(self.verticalLayoutWidget)
        self.altitudeEdit.setObjectName(u"altitudeEdit")

        self.verticalLayout.addWidget(self.altitudeEdit)

        self.longitudeLbl = QLabel(self.verticalLayoutWidget)
        self.longitudeLbl.setObjectName(u"longitudeLbl")
        self.longitudeLbl.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.longitudeLbl)

        self.longitudeEdit = QLineEdit(self.verticalLayoutWidget)
        self.longitudeEdit.setObjectName(u"longitudeEdit")

        self.verticalLayout.addWidget(self.longitudeEdit)

        self.updateBtn = QPushButton(self.verticalLayoutWidget)
        self.updateBtn.setObjectName(u"updateBtn")

        self.verticalLayout.addWidget(self.updateBtn)

        self.tabWidget.addTab(self.DetailsTab, "")
        self.formLayout = QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(u"formLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.formLayout.setLayout(0, QFormLayout.ItemRole.LabelRole, self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.videoDisplayWidget.setText(QCoreApplication.translate("MainWindow", u"Choose the camera input below!", None))
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"Start Connection", None))
        self.databaseLbl.setText(QCoreApplication.translate("MainWindow", u"Choose Database and Port", None))
        self.cameraLbl.setText(QCoreApplication.translate("MainWindow", u"Choose Camera Input", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CameraTab), QCoreApplication.translate("MainWindow", u"Camera", None))
        self.loadBtn.setText(QCoreApplication.translate("MainWindow", u"Load Details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TableTab), QCoreApplication.translate("MainWindow", u"Database", None))
        self.captureDisplayWidget.setText(QCoreApplication.translate("MainWindow", u"Detection Image", None))
        self.MapWebView.setText(QCoreApplication.translate("MainWindow", u"MapWebView", None))
        self.latitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Latitude", None))
        self.altitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Altitude", None))
        self.longitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Longitude", None))
        self.updateBtn.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DetailsTab), QCoreApplication.translate("MainWindow", u"Details", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

