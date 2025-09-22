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
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTabWidget,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 688, 520))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.gridLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.CameraTab = QWidget()
        self.CameraTab.setObjectName(u"CameraTab")
        self.verticalLayout_2 = QVBoxLayout(self.CameraTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.videoDisplayWidget = QVideoWidget(self.CameraTab)
        self.videoDisplayWidget.setObjectName(u"videoDisplayWidget")
        self.videoDisplayWidget.setMinimumSize(QSize(640, 300))
        self.videoDisplayWidget.setMaximumSize(QSize(640, 400))

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
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 671, 491))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.MapWebView = QWebEngineView(self.verticalLayoutWidget)
        self.MapWebView.setObjectName(u"MapWebView")
        self.MapWebView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.MapWebView)

        self.MapRestart = QPushButton(self.verticalLayoutWidget)
        self.MapRestart.setObjectName(u"MapRestart")

        self.verticalLayout.addWidget(self.MapRestart)

        self.tabWidget.addTab(self.MapTab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

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
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"Start Connection", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose Drone Serial", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Choose Camera Input", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CameraTab), QCoreApplication.translate("MainWindow", u"Camera", None))
        self.MapRestart.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MapTab), QCoreApplication.translate("MainWindow", u"Map", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

