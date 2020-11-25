from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget,QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import zwavePubSub


class UiMainWindow(object):
    def __init__(self):
        self.timerflip = 0
        self.btnflip = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.toggle_time)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(260, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(260, 300))
        MainWindow.setMaximumSize(QtCore.QSize(260, 300))
        qr = MainWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry(-1).center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Add device button
        self.addbutton = QtWidgets.QPushButton(self.centralwidget)
        self.addbutton.setGeometry(QtCore.QRect(50, 30, 160, 30))
        self.addbutton.clicked.connect(self.add_button_click)
        self.addbutton.setObjectName("addbutton")
        # Remove device button
        self.removebtn = QtWidgets.QPushButton(self.centralwidget)
        self.removebtn.setGeometry(QtCore.QRect(50, 70, 160, 30))
        self.removebtn.clicked.connect(self.remove_button_click)
        self.removebtn.setObjectName("removebutton")
        # turn on switch button
        self.onbtn = QtWidgets.QPushButton(self.centralwidget)
        self.onbtn.setGeometry(QtCore.QRect(50, 110, 160, 30))
        self.onbtn.clicked.connect(self.on_button_click)
        self.onbtn.setObjectName("onbutton")
        # turn off switch button
        self.offbtn = QtWidgets.QPushButton(self.centralwidget)
        self.offbtn.setGeometry(QtCore.QRect(50, 150, 160, 30))
        self.offbtn.clicked.connect(self.off_button_click)
        self.offbtn.setObjectName("offbutton")
        # toggle switch button
        self.togglebtn = QtWidgets.QPushButton(self.centralwidget)
        self.togglebtn.setGeometry(QtCore.QRect(50, 190, 160, 30))
        self.togglebtn.clicked.connect(self.toggle_button_click)
        self.togglebtn.setObjectName("togglebutton")
        # exit button
        self.exitbtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitbtn.setGeometry(QtCore.QRect(50, 230, 160, 30))
        self.exitbtn.clicked.connect(self.exit_button_click)
        self.exitbtn.setObjectName("exitbutton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def add_button_click(self):
        zwavePubSub.add_device()

    def remove_button_click(self):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setText("Are you sure to remove device?")
        msgbox.setWindowTitle("Zwave Console Message")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        button_reply = msgbox.exec_()
        if button_reply == QMessageBox.Yes:
            zwavePubSub.remove_device()

    def on_button_click(self):
        zwavePubSub.turn_on_dimmer()

    def off_button_click(self):
        zwavePubSub.turn_off_dimmer()

    def toggle_button_click(self):
        self.btnflip ^= 1
        if self.btnflip == 1:
            self.togglebtn.setText("Stop Toggle Switch")
            self.timer.start()
            zwavePubSub.turn_on_dimmer()
        elif self.btnflip == 0:
            self.togglebtn.setText("Start Toggle Switch")
            self.timer.stop()
            zwavePubSub.turn_off_dimmer()

    def toggle_time(self):
        self.timerflip ^= 1
        if self.timerflip == 1:
            zwavePubSub.turn_off_dimmer()
        elif self.timerflip == 0:
            zwavePubSub.turn_on_dimmer()

    def exit_button_click(self):
        sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CHIP Gateway Console"))
        self.addbutton.setText(_translate("MainWindow", "Form OT Network"))
        self.removebtn.setText(_translate("MainWindow", "Commission Device"))
        self.onbtn.setText(_translate("MainWindow", "Turn On Light"))
        self.offbtn.setText(_translate("MainWindow", "Turn Off Light"))
        self.togglebtn.setText(_translate("MainWindow", "Start Toggle Light"))
        self.exitbtn.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    zwavePubSub.configure_aws_connection()
    MainWindow.show()
    sys.exit(app.exec_())
