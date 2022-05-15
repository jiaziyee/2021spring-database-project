import psycopg2

import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Construct import *
from Function import *

global conn
conn = psycopg2.connect(database="Project", user="postgres", password="010504", host="127.0.0.1", port="5432")


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(400, 150)
        self.setWindowTitle("System")

        self.user_label = QLabel('User ID:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('Log in', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.mainwindow = Mainwindow()

    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 1, 1)
        self.h_layout.addWidget(self.login_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your ID')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.check_login_func)

    def check_login_func(self):

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM my_User WHERE user_id LIKE %s", (self.user_line.text(),))
        number = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("SELECT user_password FROM my_User WHERE user_id LIKE %s", (self.user_line.text(),))
        results = cursor.fetchall()

        if number[0][0] == 0:
            QMessageBox.critical(self, 'Wrong', 'User ID not exist!')
        elif results[0][0] == self.pwd_line.text():
            QMessageBox.information(self, 'Information', 'Success!')
            global ID
            ID = self.user_line.text()
            self.mainwindow.tab1.id_lab.setText(self.user_line.text())
            self.mainwindow.show()
            self.hide()
        else:
            QMessageBox.critical(self, 'Information', 'Password wrong!')

        self.user_line.clear()
        self.pwd_line.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
