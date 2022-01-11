from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap
import sys
import client
import os


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(680, 300, 500, 500)
        self.setWindowTitle("GUI")
        self.client = client.Client()
        self.q_pixmap = QPixmap('Starcraft.jpg')
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #89CFF0")
        self.pixmap = QPixmap('Starcraft.png')

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.resize(400, 120)
        self.label.move(59, 0)

        self.app_label = QLabel("Team Viewer - Python", self)
        self.app_label.move(65, 120)
        self.app_label.setFont(QtGui.QFont("Bauhaus 93", 30))
        self.app_label.adjustSize()

        self.connection_label = QLabel('Enter Server IP:', self)
        self.connection_label.setFont(QtGui.QFont("Bauhaus 93", 10))
        self.connection_label.move(150, 225)

        self.textbox = QLineEdit(self)
        self.textbox.move(145, 250)
        self.textbox.resize(200, 40)

        self.start_stream = QtWidgets.QPushButton(self)
        self.start_stream.setText("Start")
        self.start_stream.setFont(QtGui.QFont("Baskerville Old Face", 10))
        self.start_stream.move(130, 400)
        self.start_stream.clicked.connect(self.connect_server)

        self.stop_stream = QtWidgets.QPushButton(self)
        self.stop_stream.setText("Stop")
        self.stop_stream.setFont(QtGui.QFont("Baskerville Old Face", 10))
        self.stop_stream.move(270, 400)
        self.stop_stream.clicked.connect(self.disconnect_server)

        self.show()

    def connect_server(self):
        """Convert the textbox to IP and ping to check if alive, then start the server"""
        self.server_IP = self.textbox.text()
        response = os.system("ping " + self.server_IP + " -n 1")
        if response == 0:
            self.client.start_server(self.server_IP)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error connecting")
            msg.setText("Please enter valid IP")
            msg.exec_()

    def disconnect_server(self):
        """Convert the textbox to IP and ping to check if alive, then stops the server"""
        self.server_IP = self.textbox.text()
        response = os.system("ping " + self.server_IP + " -n 1")
        if response == 0:
            self.client.stop_server(self.server_IP)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error connecting")
            msg.setText("Please enter valid IP")
            msg.exec_()


def main():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())


main()
