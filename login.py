from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from verification_code import *
from pymysql import *

import sys
import time
import os
import re
import sent_email
import requests
import util


class Login(QWidget):
    to_customer = pyqtSignal()
    to_rider = pyqtSignal()
    to_merchant = pyqtSignal()

    def __init__(self):
        super(Login, self).__init__()
        self.connect = util.sql_connect()
        self.cwd = os.getcwd()
        self.cursor = self.connect.cursor()
        self.setFixedSize(1000, 1300)
        self.setWindowIcon(QIcon("./image/icon.jpg"))
        self.setWindowTitle("饱了没")
        self.INDEX = 0
        self.LOGIN = 0
        self.REGISTER = 1
        self.REGISTER_2 = 2
        self.all_items = []
        self.pass_code = ""
        self.login_palette = QPalette()
        self.login_palette.setColor(self.backgroundRole(), QColor(255, 255, 255))  # 设置背景颜色
        self.setPalette(self.login_palette)

        self.logo = QLabel(self)
        # url = "http://kuroko.info/wp-content/uploads/2020/11/2.jpg"
        # self.logo.setPixmap(QPixmap.fromImage(QImage.fromData(requests.get(url).content)))
        '''
        fin = open("./image/logo.PNG", 'rb')  # 'rb'加上才能将图片读取为二进制
        img = fin.read()  # 将二进制数据读取到img中
        fin.close()
        x = QPixmap()
        x.loadFromData(img)
        self.logo.setPixmap(x)
        '''
        self.logo.setPixmap(QPixmap("./image/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.resize(500, 200)
        self.logo.move(250, 150)

        self.username = QLineEdit(self)
        self.username.resize(470, 60)
        self.username.setFont(QFont('宋体', 12))
        self.username.setPlaceholderText("用户名")
        self.username.move(270, 400)
        self.username.setMaxLength(50)
        self.username.editingFinished.connect(self.focus_to_password)

        self.password = QLineEdit(self)
        self.password.resize(470, 60)
        self.password.setFont(QFont('宋体', 12))
        self.password.setPlaceholderText("密码")
        self.password.move(270, 520)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMaxLength(18)
        self.password.editingFinished.connect(self.focus_to_verification)

        self.verification_code = QLineEdit(self)
        self.verification_code.resize(200, 60)
        self.verification_code.setFont(QFont('宋体', 12))
        self.verification_code.setPlaceholderText("验证码")
        self.verification_code.move(270, 650)
        self.verification_code.setMaxLength(4)

        self.showpd = QCheckBox("显示密码", self)
        self.showpd.move(615, 590)
        self.showpd.stateChanged.connect(self.show_password)

        self.verification_code_list = []
        for i in range(4):
            self.verification_code_list.append(QLabel(self))
            self.verification_code_list[i].setScaledContents(True)
            self.verification_code_list[i].resize(40, 60)
            self.verification_code_list[i].move(550 + i * 40, 650)

        self.ans = ""
        self.change_code()

        self.login = QPushButton("登录", self)
        self.login.move(590, 850)
        self.login.resize(200, 60)
        self.login.setFont(QFont('幼圆', 14))
        self.login.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.login.clicked.connect(self.login_button)

        self.register = QPushButton("注册", self)
        self.register.move(200, 850)
        self.register.resize(200, 60)
        self.register.setFont(QFont('幼圆', 14))
        self.register.clicked.connect(self.register_button)

        self.forget_password = QLabel(self)
        self.forget_password.setText("<a href='#'>忘记密码?</a>")
        self.forget_password.move(600, 730)

        self.more = QLabel(self)
        self.more.setText("开发日志  |  项目开源  |  关于我们")
        self.more.setFont(QFont("幼圆", 15))
        self.more.move(150, 1100)

        self.login_items = []
        self.login_items.append(self.logo)
        self.login_items.append(self.username)
        self.login_items.append(self.password)
        self.login_items.append(self.verification_code)
        self.login_items.append(self.showpd)
        self.login_items += self.verification_code_list
        self.login_items.append(self.login)
        self.login_items.append(self.register)
        self.login_items.append(self.forget_password)
        self.login_items.append(self.more)
        self.all_items.append(self.login_items)

        self.register_logo = QLabel(self)
        self.register_logo.setPixmap(QPixmap("./image/register_logo.jpg"))
        self.register_logo.setScaledContents(True)
        self.register_logo.resize(550, 220)
        self.register_logo.move(250, 20)

        self.register_username = QLineEdit(self)
        self.register_username.resize(600, 60)
        self.register_username.setFont(QFont('宋体', 12))
        self.register_username.setPlaceholderText("不可全为空格,最大长度为50位")
        self.register_username.move(270, 280)
        self.register_username.setMaxLength(50)
        self.register_username.editingFinished.connect(self.focus_to_register_password)

        self.register_password = QLineEdit(self)
        self.register_password.resize(600, 60)
        self.register_password.setFont(QFont('宋体', 12))
        self.register_password.setPlaceholderText("任意字符,长度为6-18位")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.move(270, 400)
        self.register_password.setMaxLength(18)
        self.register_password.editingFinished.connect(self.focus_to_confirm_password)

        self.confirm_password = QLineEdit(self)
        self.confirm_password.resize(600, 60)
        self.confirm_password.setFont(QFont('宋体', 12))
        self.confirm_password.setPlaceholderText("请再次输入密码")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.move(270, 520)
        self.confirm_password.setMaxLength(18)
        self.confirm_password.editingFinished.connect(self.focus_to_register_email)

        self.register_email = QLineEdit(self)
        self.register_email.resize(600, 60)
        self.register_email.setFont(QFont('宋体', 12))
        self.register_email.setPlaceholderText("请输入正确的邮箱格式")
        self.register_email.move(270, 640)
        self.register_email.setMaxLength(50)
        self.register_email.editingFinished.connect(self.focus_to_register_phone)

        self.register_phone = QLineEdit(self)
        self.register_phone.resize(600, 60)
        self.register_phone.setFont(QFont('宋体', 12))
        self.register_phone.setPlaceholderText("请输入正确的电话号码,支持区号格式")
        self.register_phone.move(270, 760)
        self.register_phone.setMaxLength(20)
        self.register_phone.editingFinished.connect(self.focus_to_email_code)

        self.back_to_login = QPushButton("返回", self)
        self.back_to_login.move(200, 950)
        self.back_to_login.resize(200, 60)
        self.back_to_login.setFont(QFont('幼圆', 14))
        self.back_to_login.clicked.connect(self.back_to_login_button)

        self.confirm_register = QPushButton("注册", self)
        self.confirm_register.move(600, 950)
        self.confirm_register.resize(200, 60)
        self.confirm_register.setFont(QFont('幼圆', 14))
        self.confirm_register.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.confirm_register.clicked.connect(self.confirm_register_button)

        self.register_showpd = QCheckBox("显示密码", self)
        self.register_showpd.move(737, 478)
        self.register_showpd.stateChanged.connect(self.register_show_password)

        self.register_error = [0 for i in range(8)]

        self.register_items = []
        self.register_items.append(self.register_logo)
        self.register_items.append(self.register_username)
        self.register_items.append(self.register_password)
        self.register_items.append(self.confirm_password)
        self.register_items.append(self.register_email)
        self.register_items.append(self.register_phone)
        self.register_items.append(self.back_to_login)
        self.register_items.append(self.confirm_register)
        self.register_items.append(self.register_showpd)
        self.all_items.append(self.register_items)

        self.email_code = QLineEdit(self)
        self.email_code.resize(150, 50)
        self.email_code.setFont(QFont('宋体', 12))
        self.email_code.move(340, 905)
        self.email_code.setMaxLength(6)

        self.sent_code = QPushButton("发送验证码", self)
        self.sent_code.move(550, 905)
        self.sent_code.resize(220, 50)
        self.sent_code.setFont(QFont('幼圆', 12))
        self.sent_code.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.sent_code.clicked.connect(self.email_action)
        self.count = 60
        self.email_timer = QTimer(self)
        self.email_timer.setInterval(1000)
        self.email_timer.timeout.connect(self.email_refresh)

        self.choose_index = 0
        self.choose_customer = QPushButton("我是顾客", self)
        self.choose_customer.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.choose_customer.resize(180, 60)
        self.choose_customer.setFont(QFont('宋体', 12))
        self.choose_customer.move(160, 250)
        self.choose_customer.clicked.connect(lambda: self.choose_button(0))

        self.choose_rider = QPushButton("我是骑手", self)
        self.choose_rider.setStyleSheet("background-color: rgb(232, 232, 232)")
        self.choose_rider.resize(180, 60)
        self.choose_rider.setFont(QFont('宋体', 12))
        self.choose_rider.move(410, 250)
        self.choose_rider.clicked.connect(lambda: self.choose_button(1))

        self.choose_merchant = QPushButton("我是商家", self)
        self.choose_merchant.setStyleSheet("background-color: rgb(232, 232, 232)")
        self.choose_merchant.resize(180, 60)
        self.choose_merchant.setFont(QFont('宋体', 12))
        self.choose_merchant.move(660, 250)
        self.choose_merchant.clicked.connect(lambda: self.choose_button(2))

        self.choose_portrait = QPushButton("选取图片", self)
        self.choose_portrait.resize(180, 55)
        self.choose_portrait.setFont(QFont('宋体', 12))
        self.choose_portrait.move(530, 495)
        self.choose_portrait.clicked.connect(self.portrait_file_dialog)

        self.register_portrait = QLabel(self)
        self.register_portrait.setPixmap(QPixmap("./image/default_customer.jpg"))
        self.register_portrait.setScaledContents(True)
        self.register_portrait.resize(149, 149)
        self.register_portrait.move(341, 401)

        self.portrait_name = "./image/default_customer.jpg"

        self.pos_x = QComboBox(self)
        self.pos_x.addItems([str(i) for i in range(1, 1000)])
        self.pos_x.setFont(QFont('宋体', 12))
        self.pos_x.resize(100, 50)
        self.pos_x.move(340, 605)

        self.pos_y = QComboBox(self)
        self.pos_y.addItems([str(i) for i in range(1, 1000)])
        self.pos_y.setFont(QFont('宋体', 12))
        self.pos_y.resize(100, 50)
        self.pos_y.move(570, 605)

        self.time_1 = QComboBox(self)
        for i in range(24):
            if i < 10: self.time_1.addItem("0"+str(i))
            else: self.time_1.addItem(str(i))
        self.time_1.setFont(QFont('宋体', 12))
        self.time_1.resize(80, 50)
        self.time_1.move(340, 705)

        self.time_2 = QComboBox(self)
        for i in range(60):
            if i < 10: self.time_2.addItem("0"+str(i))
            else: self.time_2.addItem(str(i))
        self.time_2.setFont(QFont('宋体', 12))
        self.time_2.resize(80, 50)
        self.time_2.move(450, 705)

        self.time_3 = QComboBox(self)
        for i in range(24):
            if i < 10: self.time_3.addItem("0" + str(i))
            else: self.time_3.addItem(str(i))
        self.time_3.setFont(QFont('宋体', 12))
        self.time_3.resize(80, 50)
        self.time_3.move(605, 705)

        self.time_4 = QComboBox(self)
        for i in range(60):
            if i < 10: self.time_4.addItem("0" + str(i))
            else: self.time_4.addItem(str(i))
        self.time_4.setFont(QFont('宋体', 12))
        self.time_4.resize(80, 50)
        self.time_4.move(715, 705)

        self.date_1 = QComboBox(self)
        self.date_1.addItems([str(i) for i in range(1900, 2021)])
        self.date_1.setFont(QFont('宋体', 12))
        self.date_1.resize(110, 50)
        self.date_1.move(340, 705)

        self.date_2 = QComboBox(self)
        self.date_2.addItems([str(i) for i in range(1, 13)])
        self.date_2.setFont(QFont('宋体', 12))
        self.date_2.resize(100, 50)
        self.date_2.move(500, 705)

        self.date_3 = QComboBox(self)
        self.date_3.addItems([str(i) for i in range(1, 32)])
        self.date_3.setFont(QFont('宋体', 12))
        self.date_3.resize(100, 50)
        self.date_3.move(650, 705)

        self.back_to_register = QPushButton("返回", self)
        self.back_to_register.move(200, 1050)
        self.back_to_register.resize(200, 60)
        self.back_to_register.setFont(QFont('幼圆', 14))
        self.back_to_register.clicked.connect(self.back_to_register_button)

        self.finish_register = QPushButton("完成", self)
        self.finish_register.move(600, 1050)
        self.finish_register.resize(200, 60)
        self.finish_register.setFont(QFont('幼圆', 14))
        self.finish_register.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.finish_register.clicked.connect(self.finish_register_button)

        self.register2_error = [0, 0]

        self.register2_items = []
        self.register2_items.append(self.register_logo)
        self.register2_items.append(self.email_code)
        self.register2_items.append(self.sent_code)
        self.register2_items.append(self.choose_customer)
        self.register2_items.append(self.choose_rider)
        self.register2_items.append(self.choose_merchant)
        self.register2_items.append(self.choose_portrait)
        self.register2_items.append(self.register_portrait)
        self.register2_items.append(self.pos_x)
        self.register2_items.append(self.pos_y)
        self.register2_items.append(self.time_1)
        self.register2_items.append(self.time_2)
        self.register2_items.append(self.time_3)
        self.register2_items.append(self.time_4)
        self.register2_items.append(self.date_1)
        self.register2_items.append(self.date_2)
        self.register2_items.append(self.date_3)
        self.register2_items.append(self.back_to_register)
        self.register2_items.append(self.finish_register)

        self.all_items.append(self.register2_items)
        self.show_interface(self.LOGIN)


    def show_interface(self, index):
        for i in range(len(self.all_items)):
            for j in range(len(self.all_items[i])):
                self.all_items[i][j].setVisible(False)

        for j in range(len(self.all_items[index])):
            self.all_items[index][j].setVisible(True)

        tmp = [self.username, self.password, self.verification_code, self.email_code]
        for i in range(len(tmp)):
            tmp[i].setText("")

    def show_password(self):
        if self.showpd.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def register_show_password(self):
        if self.register_showpd.isChecked():
            self.register_password.setEchoMode(QLineEdit.Normal)
            self.confirm_password.setEchoMode(QLineEdit.Normal)
        else:
            self.register_password.setEchoMode(QLineEdit.Password)
            self.confirm_password.setEchoMode(QLineEdit.Password)

    def focus_to_password(self):
        self.password.setFocus()

    def focus_to_verification(self):
        self.verification_code.setFocus()

    def focus_to_register_password(self):
        self.register_password.setFocus()

    def focus_to_confirm_password(self):
        self.confirm_password.setFocus()

    def focus_to_register_email(self):
        self.register_email.setFocus()

    def focus_to_register_phone(self):
        self.register_phone.setFocus()

    def focus_to_email_code(self):
        self.email_code.setFocus()

    def change_code(self):
        self.ans, photos = random_verification_code()
        for i in range(4):
            self.verification_code_list[i].setPixmap(QPixmap(photos[i]))

    def login_button(self):
        if self.verification_code.text().lower() != self.ans.lower():
            QMessageBox.critical(self, "错误", "验证码错误！")
        else:
            if self.username.text() == "":
                QMessageBox.critical(self, "错误", "用户名不能为空！")
            elif self.password.text() == "":
                QMessageBox.critical(self, "错误", "密码不能为空！")
            else:
                sql = "select count(*) from users where `username` = '%s'" % self.username.text()
                self.cursor.execute(sql)
                if self.cursor.fetchone()[0] == 0:
                    QMessageBox.critical(self, "错误", "用户名不存在！")
                else:
                    sql = "select password from users where `username` = '%s'" % self.username.text()
                    self.cursor.execute(sql)
                    if self.cursor.fetchone()[0] != self.password.text():
                        QMessageBox.critical(self, "错误", "用户名或密码错误！")
                    else:
                        sql = "select user_type from users where `username` = '%s'" % self.username.text()
                        self.cursor.execute(sql)
                        login_type = self.cursor.fetchone()[0]
                        if login_type == "customer": self.to_customer.emit()
                        elif login_type == "rider": self.to_rider.emit()
                        else: self.to_merchant.emit()
        self.change_code()

    def register_button(self):
        tmp = [self.register_username, self.register_password, self.confirm_password, self.register_email, self.register_phone]
        for i in range(len(tmp)):
            tmp[i].setText("")
        self.INDEX = self.REGISTER
        self.update()
        self.show_interface(self.REGISTER)

    def email_action(self):
        if self.sent_code.isEnabled():
            self.register2_error[0] = 0
            email_text = self.register_email.text()
            email_type = sent_email.email_type(email_text)
            if email_type == 0: self.pass_code = "all-right-mode"
            else:
                self.pass_code = sent_email.sent_email([email_text])
                if self.pass_code != "all-right-mode" and self.pass_code.isdigit() == False:
                    self.register2_error[0] = 1
                    self.update()
                    return
                else:
                    self.email_timer.start()
                    self.sent_code.setEnabled(False)

    def email_refresh(self):
        if self.count > 0:
            self.sent_code.setText("重新发送(" + str(self.count) + ")")
            self.count -= 1
        else:
            self.email_timer.stop()
            self.sent_code.setEnabled(True)
            self.sent_code.setText('重新发送')
            self.count = 60

    def back_to_login_button(self):
        self.INDEX = self.LOGIN
        self.update()
        self.show_interface(self.LOGIN)

    def back_to_register_button(self):
        self.INDEX = self.REGISTER
        self.update()
        self.show_interface(self.REGISTER)

    def confirm_register_button(self):
        self.register_error = [0 for i in range(8)]
        if len(self.register_username.text()) == 0:
            self.register_error[1] = 1
        elif self.register_username.text().isspace():
            self.register_error[1] = 1
        else:
            sql = "select count(*) from users where `username` = '%s'" % self.register_username.text()
            self.cursor.execute(sql)
            if self.cursor.fetchone()[0] > 0:
                self.register_error[0] = 1

        if 0 <= len(self.register_password.text()) < 6:
            self.register_error[2] = 1
        elif 0 <= len(self.confirm_password.text()) < 6:
            self.register_error[3] = 1
        elif self.confirm_password.text() != self.register_password.text():
            self.register_error[3] = 1

        if len(self.register_email.text()) == 0:
            self.register_error[5] = 1
        elif sent_email.email_type(self.register_email.text()) == -1:
            self.register_error[5] = 1
        else:
            sql = "select count(*) from users where `email` = '%s'" % self.register_email.text()
            self.cursor.execute(sql)
            if self.cursor.fetchone()[0] > 0:
                self.register_error[4] = 1

        if len(self.register_phone.text()) == 0:
            self.register_error[7] = 1
        else:
            pattern = re.compile(r"^\+?\d+(-\d+)*$")
            if pattern.match(self.register_phone.text()):
                sql = "select count(*) from users where `telephone` = '%s'" % self.register_phone.text()
                self.cursor.execute(sql)
                if self.cursor.fetchone()[0] > 0:
                    self.register_error[6] = 1
            else:
                self.register_error[7] = 1
        if sum(self.register_error) == 0:
            self.INDEX = self.REGISTER_2
            self.show_interface(self.REGISTER_2)
            self.register2_error = [0, 0]
            self.choose_button(0)
        self.update()

    def finish_register_button(self):
        self.register2_error[1] = [0]
        if self.email_code.text() == "": self.register2_error[1] = 1
        elif self.email_code.text() != self.pass_code: self.register2_error[1] = 1
        if self.pass_code == "all-right-mode": self.register2_error[1] = 0
        if self.register2_error[1] == 1:
            self.update()
        else:
            tmp = ["customer", "rider", "merchant"]
            sql = "insert into users (`username`,`password`,`user_type`,`email`,`telephone`)values('%s','%s','%s','%s','%s')" %\
                  (self.register_username.text(), self.register_password.text(), tmp[self.choose_index], self.register_email.text(), self.register_phone.text())
            print(sql)
            try:
                self.cursor.execute(sql)
                # self.connect.commit()
                # print("users插入成功")
            except:
                pass
                # print("users插入失败")
            if self.choose_index == 0:
                sql = "insert into customer (`username`,`portrait`,`longitude`, `latitude`, `register_date`)values('%s','%s',%d,%d,'%s');" % \
                      (self.register_username.text(), self.portrait_name, int(self.pos_x.currentText()), int(self.pos_y.currentText()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split()[0])
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                    QMessageBox.about(self, "饱了没", "注册成功!")
                except:
                    self.connect.rollback()
                    QMessageBox.critical(self, "饱了没", "注册失败!")

            elif self.choose_index == 1:
                sql = "insert into rider (`username`,`portrait`,`longitude`, `latitude`, `register_date`)values('%s','%s',%d,%d,'%s');" % \
                      (self.register_username.text(), self.portrait_name, int(self.pos_x.currentText()),
                       int(self.pos_y.currentText()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split()[0])
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                    QMessageBox.about(self, "饱了没", "注册成功!")
                except:
                    self.connect.rollback()
                    QMessageBox.critical(self, "饱了没", "注册失败!")

            elif self.choose_index == 2:
                begin = self.time_1.currentText()+":"+self.time_2.currentText()
                end = self.time_3.currentText()+":"+self.time_4.currentText()
                sql = "insert into merchant (`username`,`portrait`,`longitude`, `latitude`, `register_date`, `begin_time`, `end_time`)values('%s','%s',%d,%d,'%s','%s','%s');" % \
                      (self.register_username.text(), self.portrait_name, int(self.pos_x.currentText()), int(self.pos_y.currentText()),
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split()[0], begin, end)
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                    QMessageBox.about(self, "饱了没", "注册成功!")
                except:
                    self.connect.rollback()
                    QMessageBox.critical(self, "饱了没", "注册失败!")
            self.INDEX = self.LOGIN
            self.update()
            self.show_interface(self.LOGIN)

    def choose_button(self, mode):
        self.choose_index = mode
        tmp1 = [self.choose_customer, self.choose_rider, self.choose_merchant]
        tmp2 = ["customer", "rider", "merchant"]
        tmp3 = [self.time_1, self.time_2, self.time_3, self.time_4]
        tmp4 = [self.date_1, self.date_2, self.date_3]
        self.portrait_name = "./image/default_%s.jpg" % tmp2[mode]
        self.register_portrait.setPixmap(QPixmap("./image/default_%s.jpg" % tmp2[mode]))

        for i in range(3):
            if i == mode: tmp1[i].setStyleSheet("background-color: rgb(51, 153, 255)")
            else: tmp1[i].setStyleSheet("background-color: rgb(232, 232, 232)")

        for i in range(4): tmp3[i].setVisible(bool(self.choose_index == 1) | bool(self.choose_index == 2))
        for i in range(3): tmp4[i].setVisible(bool(self.choose_index == 0))

        self.update()

    def portrait_file_dialog(self):
        file_name, file_type = QFileDialog.getOpenFileName(self,
                                                           "选取文件",
                                                           self.cwd,  # 起始路径
                                                           "图像文件 (*.bmp *.jpg *.jpeg *.png)")  # 设置文件扩展名过滤,用双分号间隔
        if file_name != "":
            self.register_portrait.setPixmap(QPixmap(file_name))
            self.portrait_name = file_name

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if self.INDEX == self.LOGIN:
            if 690 > x > 530 and 710 > y > 650:
                self.change_code()
            elif 150 < x < 330 and 1100 < y < 1145:
                QDesktopServices.openUrl(QUrl('http://kuroko.info/areyourfull-diary/'))
            elif 400 < x < 580 and 1100 < y < 1145:
                QDesktopServices.openUrl(QUrl('https://github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project'))
            elif 660 < x < 840 and 1100 < y < 1145:
                QMessageBox.about(self, "关于我们", "2021 ECNU MySQL Final Project")

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.INDEX == self.LOGIN:
            self.paint_login(event, qp)
        elif self.INDEX == self.REGISTER:
            self.paint_register(event, qp)
        elif self.INDEX == self.REGISTER_2:
            self.paint_register2(event, qp)
        qp.end()

    def paint_login(self, event, qp):
        return

    def paint_register(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("楷体", 16))
        qp.drawText(80, 320, "用户名:")
        qp.drawText(125, 440, "密码:")
        qp.drawText(38, 560, "确认密码:")
        qp.drawText(38, 680, "电子邮箱:")
        qp.drawText(38, 800, "电话号码:")
        register_errors = [(270, 370, "用户名已被注册!"),
                           (270, 370, "用户名不能为空!"),
                           (270, 490, "密码长度过短!"),
                           (270, 610, "两次输入的密码不一致!"),
                           (270, 730, "邮箱已被注册!"),
                           (270, 730, "邮箱格式错误!"),
                           (270, 850, "手机号已被注册!"),
                           (270, 850, "手机号格式错误!")]
        qp.setPen(QColor(255, 0, 0))
        qp.setFont(QFont("宋体", 9))
        for i in range(len(register_errors)):
            if self.register_error[i]:
                qp.drawText(register_errors[i][0], register_errors[i][1], register_errors[i][2])

    def paint_register2(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("宋体", 13))
        qp.drawText(455, 642, "经度         纬度")
        if self.choose_index == 0:
            qp.drawText(455, 742, "年")
            qp.drawText(605, 742, "月")
            qp.drawText(750, 742, "日")
        else:
            qp.drawText(425, 742, ":      —")
            qp.drawText(690, 742, ":")
        qp.drawRect(340, 400, 150, 150)
        tmp1 = ["用户头像:", "骑手头像:", "商家图标:"]
        tmp2 = ["居住地址:", "工作地址:", "店铺地址:"]
        tmp3 = ["出生日期:", "工作时间:", "营业时间:"]
        qp.drawText(160, 430, tmp1[self.choose_index])
        qp.drawText(160, 640, tmp2[self.choose_index])
        qp.drawText(160, 740, tmp3[self.choose_index])
        qp.drawText(160, 840, "注册邮箱: " + self.register_email.text())
        qp.drawText(160, 940, "  验证码:")
        qp.setPen(QColor(255, 0, 0))
        qp.setFont(QFont("宋体", 9))
        if self.register2_error[0]: qp.drawText(340, 990, "发送邮件失败,请检查邮箱!")
        #if self.register2_error[1]: qp.drawText(340, 990, "验证码错误!")


if __name__ == '__main__':
    pass
