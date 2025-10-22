# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(887, 710)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 688, 520))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 20, 851, 671))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
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

        self.label = QLabel(self.CameraTab)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(10000, 30))

        self.verticalLayout_2.addWidget(self.label)

        self.SerialComboBox = QComboBox(self.CameraTab)
        self.SerialComboBox.setObjectName(u"SerialComboBox")
        self.SerialComboBox.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_2.addWidget(self.SerialComboBox)

        self.label_2 = QLabel(self.CameraTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(10000, 30))

        self.verticalLayout_2.addWidget(self.label_2)

        self.CameraComboBox = QComboBox(self.CameraTab)
        self.CameraComboBox.setObjectName(u"CameraComboBox")
        self.CameraComboBox.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_2.addWidget(self.CameraComboBox)

        self.tabWidget.addTab(self.CameraTab, "")
        self.MapTab = QWidget()
        self.MapTab.setObjectName(u"MapTab")
        self.verticalLayoutWidget = QWidget(self.MapTab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 831, 611))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.captureDisplayWidget = QLabel(self.verticalLayoutWidget)
        self.captureDisplayWidget.setObjectName(u"captureDisplayWidget")

        self.verticalLayout.addWidget(self.captureDisplayWidget)

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

        self.saveDatabase = QPushButton(self.verticalLayoutWidget)
        self.saveDatabase.setObjectName(u"saveDatabase")

        self.verticalLayout.addWidget(self.saveDatabase)

        self.tabWidget.addTab(self.MapTab, "")
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose Drone Serial", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Choose Camera Input", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CameraTab), QCoreApplication.translate("MainWindow", u"Camera", None))
        self.captureDisplayWidget.setText(QCoreApplication.translate("MainWindow", u"Detection Image", None))
        self.latitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Latitude", None))
        self.altitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Altitude", None))
        self.longitudeLbl.setText(QCoreApplication.translate("MainWindow", u"Longitude", None))
        self.saveDatabase.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MapTab), QCoreApplication.translate("MainWindow", u"Map", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

