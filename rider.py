from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pymysql import *
import sys
import os
import util
import re
import sent_email


class Rider(QWidget):
    to_login = pyqtSignal()

    def __init__(self, username):
        super(Rider, self).__init__()
        self.connect = Connect(
            host="124.71.228.59",
            port=3306,
            user="DB_USER066",
            passwd="DB_USER066@123",
            db="user066db",
            charset="utf8"
        )
        self.cwd = os.getcwd()
        self.cursor = self.connect.cursor()
        self.setFixedSize(900, 1400)
        self.setWindowIcon(QIcon("./image/icon.jpg"))
        self.setWindowTitle("饱了没-骑手版")
        self.username = username
        self.login_palette = QPalette()
        self.login_palette.setColor(self.backgroundRole(), QColor(255, 255, 255))  # 设置背景颜色
        self.setPalette(self.login_palette)
        self.info = None
        self.all_orders = []
        self.info_refresh()
        print(self.info)
        self.dialog = None
        self.all_items = []
        self.INDEX = 0
        self.MAIN = 0
        self.ORDER = 1
        self.PERSONAL = 2

        self.main_button = QPushButton("主菜单", self)
        self.main_button.move(0, 1342)
        self.main_button.resize(300, 60)
        self.main_button.setFont(QFont('幼圆', 13))
        self.main_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.main_button.clicked.connect(lambda: self.menu_choose(self.MAIN))

        self.order_button = QPushButton("订单中心", self)
        self.order_button.move(300, 1342)
        self.order_button.resize(300, 60)
        self.order_button.setFont(QFont('幼圆', 13))
        self.order_button.setStyleSheet("background-color: rgb(232, 232, 232)")
        self.order_button.clicked.connect(lambda: self.menu_choose(self.ORDER))

        self.personal_button = QPushButton("个人中心", self)
        self.personal_button.move(600, 1342)
        self.personal_button.resize(302, 60)
        self.personal_button.setFont(QFont('幼圆', 13))
        self.personal_button.setStyleSheet("background-color: rgb(232, 232, 232)")
        self.personal_button.clicked.connect(lambda: self.menu_choose(self.PERSONAL))

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("./image/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.resize(500, 200)
        self.logo.move(200, 50)

        self.request = QLabel(self)
        self.request.setPixmap(QPixmap("./image/request_abstract.jpg"))
        self.request.setScaledContents(True)
        self.request.resize(430, 430)
        self.request.move(10, 280)

        self.request_button = QPushButton("接单中心", self)
        self.request_button.move(10, 710)
        self.request_button.resize(430, 60)
        self.request_button.setFont(QFont('幼圆', 13))
        self.request_button.clicked.connect(self.func_request_button)

        self.rank = QLabel(self)
        self.rank.setPixmap(QPixmap("./image/rank_abstract.jpg"))
        self.rank.setScaledContents(True)
        self.rank.resize(430, 430)
        self.rank.move(460, 280)

        self.rank_button = QPushButton("骑手排行", self)
        self.rank_button.move(460, 710)
        self.rank_button.resize(430, 60)
        self.rank_button.setFont(QFont('幼圆', 13))
        self.rank_button.clicked.connect(self.func_rank_button)

        self.evaluate = QLabel(self)
        self.evaluate.setPixmap(QPixmap("./image/evaluate_abstract.jpg"))
        self.evaluate.setScaledContents(True)
        self.evaluate.resize(430, 430)
        self.evaluate.move(10, 810)

        self.evaluate_button = QPushButton("我的评价", self)
        self.evaluate_button.move(10, 1240)
        self.evaluate_button.resize(430, 60)
        self.evaluate_button.setFont(QFont('幼圆', 13))
        self.evaluate_button.clicked.connect(self.func_evaluate_button)

        self.contract = QLabel(self)
        self.contract.setPixmap(QPixmap("./image/merchant_abstract.jpg"))
        self.contract.setScaledContents(True)
        self.contract.resize(430, 430)
        self.contract.move(460, 810)

        self.contract_button = QPushButton("签约商家", self)
        self.contract_button.move(460, 1240)
        self.contract_button.resize(430, 60)
        self.contract_button.setFont(QFont('幼圆', 13))
        self.contract_button.clicked.connect(self.func_contract_button)

        self.main_items = []
        self.main_items.append(self.logo)
        self.main_items += [self.request, self.request_button]
        self.main_items += [self.rank, self.rank_button]
        self.main_items += [self.evaluate, self.evaluate_button]
        self.main_items += [self.contract, self.contract_button]
        self.all_items.append(self.main_items)

        self.order_logo = QLabel(self)
        self.order_logo.setPixmap(QPixmap("./image/order_logo.png"))
        self.order_logo.setScaledContents(True)
        self.order_logo.resize(550, 200)
        self.order_logo.move(175, 0)

        self.order_index = 0
        self.sum_order = len(self.all_orders)
        self.pre_order = QPushButton("上一页", self)
        self.pre_order.resize(160, 50)
        self.pre_order.setFont(QFont('幼圆', 10))
        self.pre_order.move(210, 1287)
        self.pre_order.clicked.connect(lambda: self.change_order(-1))

        self.next_order = QPushButton("下一页", self)
        self.next_order.resize(160, 50)
        self.next_order.setFont(QFont('幼圆', 10))
        self.next_order.move(530, 1287)
        self.next_order.clicked.connect(lambda: self.change_order(1))

        self.show_order = QPushButton(str(self.order_index + 1), self)
        self.show_order.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.show_order.resize(60, 50)
        self.show_order.setFont(QFont('幼圆', 12))
        self.show_order.move(420, 1287)

        self.products = QScrollArea(self)
        self.products.move(0, 530)
        self.products.resize(900, 750)

        self.all_product = None
        self.order_items = []
        self.order_items.append(self.pre_order)
        self.order_items.append(self.next_order)
        self.order_items.append(self.show_order)
        self.order_items.append(self.order_logo)
        self.order_items.append(self.products)
        self.all_items.append(self.order_items)

        self.plogo = QLabel(self)
        self.plogo.setPixmap(QPixmap("./image/logo.png"))
        self.plogo.setScaledContents(True)
        self.plogo.resize(500, 200)
        self.plogo.move(200, 0)

        self.personal_portrait = QLabel(self)
        self.personal_portrait.setPixmap(QPixmap(self.info[6]))
        self.personal_portrait.setScaledContents(True)
        self.personal_portrait.resize(250, 250)
        self.personal_portrait.move(50, 210)

        self.change_password = QPushButton("修改密码", self)
        self.change_password.resize(180, 50)
        self.change_password.setFont(QFont("宋体", 12))
        self.change_password.move(650, 215)
        self.change_password.clicked.connect(self.change_password_dialog)

        self.upgrade = QPushButton("提升等级", self)
        self.upgrade.resize(180, 50)
        self.upgrade.setFont(QFont("宋体", 12))
        self.upgrade.move(650, 305)
        self.upgrade.clicked.connect(self.upgrade_dialog)

        self.change_portrait = QPushButton("更改头像", self)
        self.change_portrait.resize(180, 50)
        self.change_portrait.setFont(QFont('宋体', 12))
        self.change_portrait.move(650, 400)
        self.change_portrait.clicked.connect(self.portrait_file_dialog)

        self.change_email = QPushButton("更改邮箱", self)
        self.change_email.resize(180, 50)
        self.change_email.setFont(QFont('宋体', 12))
        self.change_email.move(650, 505)
        self.change_email.clicked.connect(self.change_email_dialog)

        self.change_phone = QPushButton("更改电话", self)
        self.change_phone.resize(180, 50)
        self.change_phone.setFont(QFont('宋体', 12))
        self.change_phone.move(650, 610)
        self.change_phone.clicked.connect(self.change_phone_dialog)

        self.change_address = QPushButton("更换地址", self)
        self.change_address.resize(180, 50)
        self.change_address.setFont(QFont('宋体', 12))
        self.change_address.move(650, 1030)
        self.change_address.clicked.connect(self.change_address_dialog)

        self.quit = QPushButton("退出登录", self)
        self.quit.setStyleSheet("background-color: rgb(238, 44, 44)")
        self.quit.resize(300, 60)
        self.quit.setFont(QFont('幼圆', 14))
        self.quit.move(300, 1200)
        self.quit.clicked.connect(self.quit_to_login)

        self.personal_items = []
        self.personal_items.append(self.plogo)
        self.personal_items.append(self.change_portrait)
        self.personal_items.append(self.personal_portrait)
        self.personal_items.append(self.upgrade)
        self.personal_items.append(self.change_password)
        self.personal_items.append(self.change_email)
        self.personal_items.append(self.change_phone)
        self.personal_items.append(self.change_address)
        self.personal_items.append(self.quit)
        self.all_items.append(self.personal_items)

        self.show_interface(self.MAIN)

    def change_email_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_email = QLineEdit(self.dialog)
        input_email.setFont(QFont("宋体", 12))
        input_email.resize(450, 50)
        input_email.setPlaceholderText("输入新邮箱")
        input_email.move(25, 20)
        input_email.setMaxLength(50)

        confirm = QPushButton("修改邮箱", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_email(input_email.text()))

        self.dialog.setWindowTitle("修改邮箱")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_email(self, email):
        if len(email) == 0:
            QMessageBox.critical(self, "饱了没", "邮箱不能为空!")
        elif sent_email.email_type(email) == -1:
            QMessageBox.critical(self, "饱了没", "邮箱格式错误!")
        else:
            sql = "select count(*) from users where `email` = '%s'" % email
            self.cursor.execute(sql)
            if self.cursor.fetchone()[0] > 0:
                QMessageBox.critical(self, "饱了没", "邮箱已经被注册!")
            else:
                sql = "update users set `email` = '%s' where `username` = '%s'" % (email, self.info[0])
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                    self.info[4] = email
                    self.update()
                    self.dialog.close()
                except:
                    QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

    def portrait_file_dialog(self):
        file_name, file_type = QFileDialog.getOpenFileName(self,
                                                           "选取文件",
                                                           os.getcwd(),  # 起始路径
                                                           "图像文件 (*.bmp *.jpg *.jpeg *.png)")
        if file_name != "":
            sql = "update `rider` set `portrait` = '%s' where username = '%s'" % (file_name, self.info[0])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                self.personal_portrait.setPixmap(QPixmap(file_name))
                self.info[6] = file_name
            except:
                QMessageBox.critical(self, "饱了没", "上传失败!\n请检查数据库连接!")

    def change_phone_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_phone = QLineEdit(self.dialog)
        input_phone.setFont(QFont("宋体", 12))
        input_phone.resize(450, 50)
        input_phone.setPlaceholderText("输入新电话")
        input_phone.move(25, 20)
        input_phone.setMaxLength(50)

        confirm = QPushButton("修改电话", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_phone(input_phone.text()))

        self.dialog.setWindowTitle("修改电话")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_phone(self, phone):
        if len(phone) == 0:
            QMessageBox.critical(self, "饱了没", "电话不能为空!")
        else:
            pattern = re.compile(r"^\+?\d+(-\d+)*$")
            if pattern.match(phone):
                sql = "select count(*) from users where `telephone` = '%s'" % phone
                self.cursor.execute(sql)
                if self.cursor.fetchone()[0] > 0:
                    QMessageBox.critical(self, "饱了没", "电话已经被注册!")
                else:
                    sql = "update users set `telephone` = '%s' where `username` = '%s'" % (phone, self.info[0])
                    try:
                        self.cursor.execute(sql)
                        self.connect.commit()
                        self.info[3] = phone
                        self.update()
                        self.dialog.close()
                    except:
                        QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")
            else:
                QMessageBox.critical(self, "饱了没", "电话格式错误!")

    def change_address_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(325, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        pos_x = QComboBox(self.dialog)
        pos_x.addItems([str(i) for i in range(1, 1000)])
        pos_x.setFont(QFont('宋体', 12))
        pos_x.resize(100, 50)
        pos_x.move(25, 20)

        pos_y = QComboBox(self.dialog)
        pos_y.addItems([str(i) for i in range(1, 1000)])
        pos_y.setFont(QFont('宋体', 12))
        pos_y.resize(100, 50)
        pos_y.move(200, 20)

        confirm = QPushButton("修改地址", self.dialog)
        confirm.move(25, 90)
        confirm.resize(275, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(lambda: self.confirm_change_address(int(pos_x.currentText()), int(pos_y.currentText())))

        self.dialog.setWindowTitle("迁址")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_address(self, x, y):
        sql1 = "update `rider` set `longitude` = %d where `username` = '%s'" % (x, self.info[0])
        sql2 = "update `rider` set `latitude` = %d where `username` = '%s'" % (y, self.info[0])
        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.connect.commit()
            self.info[10] = x
            self.info[11] = y
            self.update()
            self.dialog.close()
        except:
            QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

    def upgrade_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 630)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        QR_code = QLabel(self.dialog)
        QR_code.setPixmap(QPixmap("./image/qrcode_diary.png"))
        QR_code.setScaledContents(True)
        QR_code.resize(450, 450)
        QR_code.move(25, 25)

        input_password = QLineEdit(self.dialog)
        input_password.setFont(QFont("宋体", 12))
        input_password.resize(450, 50)
        input_password.setPlaceholderText("密钥:扫一扫输入网页链接")
        input_password.move(25, 490)
        input_password.setMaxLength(100)

        confirm = QPushButton("确认升级", self.dialog)
        confirm.move(25, 560)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(lambda: self.confirm_upgrade(input_password.text()))

        self.dialog.setWindowTitle("升级等级")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_upgrade(self, password):
        if password == "http://kuroko.info/areyourfull-diary/" \
                or password == "http://kuroko.info/areyourfull-diary" \
                or password == "kuroko.info/areyourfull-diary/" \
                or password == "kuroko.info/areyourfull-diary":
            sql = "update `rider` set `rider_level` = 'expert' where `username` = '%s'" % self.info[0]
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                self.info[7] = "expert"
                self.update()
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "升级失败!\n请检查数据库连接!")
        else:
            QMessageBox.critical(self, "饱了没", "密码错误!\n请检查密钥内容!")

    def quit_to_login(self):
        self.to_login.emit()

    def show_interface(self, index):
        self.INDEX = index
        self.info_refresh()
        self.update()
        self.main_button.setVisible(True)
        self.order_button.setVisible(True)
        self.personal_button.setVisible(True)
        for i in range(len(self.all_items)):
            for j in range(len(self.all_items[i])):
                self.all_items[i][j].setVisible(False)

        for j in range(len(self.all_items[index])):
            self.all_items[index][j].setVisible(True)

    def info_refresh(self):
        self.connect = Connect(
            host="124.71.228.59",
            port=3306,
            user="DB_USER066",
            passwd="DB_USER066@123",
            db="user066db",
            charset="utf8"
        )
        self.cursor = self.connect.cursor()
        sql = "select * from `users` where username = '%s'" % self.username
        self.cursor.execute(sql)
        self.info = list(self.cursor.fetchone())
        sql = "select * from `rider` where username = '%s'" % self.username
        self.cursor.execute(sql)
        self.info += list(self.cursor.fetchone())[1:]
        sql = "select * from `order` where `rider_name` = '%s'" % self.username
        self.cursor.execute(sql)
        self.all_orders = self.cursor.fetchall()

    def menu_choose(self, index):
        if index == 1 and self.sum_order == 0:
            QMessageBox.critical(self, "饱了没", "暂无订单!")
            return
        self.show_interface(index)
        tmp1 = [self.main_button, self.order_button, self.personal_button]
        for e in tmp1: e.setStyleSheet("background-color: rgb(232, 232, 232)")
        tmp1[index].setStyleSheet("background-color: rgb(51, 153, 255)")

        if index == self.ORDER:
            self.display_order(0)

    def func_request_button(self):
        self.info_refresh()
        sql = "select `order_id`,`order_time`,`customer_name`,`order`.merchant_name,`state`" \
        "from `order` inner join `contract` " \
        "on `order`.merchant_name = `contract`.merchant_name " \
        "where `contract`.rider_name = '%s'" \
        "and (`state` = 1 or `state` = 2) " % self.info[0]
        self.cursor.execute(sql)
        all_requests = self.cursor.fetchall()
        print(all_requests)
        if len(all_requests) == 0:
            QMessageBox.about(self, "饱了没", "暂无订单请求!")
            return
        self.dialog = QDialog()
        self.dialog.setFixedSize(1400, 1400)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))
        self.dialog.setWindowTitle("可接订单")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setPalette(self.login_palette)

        request_list = QScrollArea(self.dialog)
        request_list.move(0, 0)
        request_list.resize(1400, 1400)
        items = QWidget()
        vLayout = QVBoxLayout(items)
        for request in all_requests:
            vLayout.addWidget(self.create_request_item(request))
        request_list.setWidget(items)
        self.dialog.exec_()

    def create_request_item(self, request):
        groupBox = QGroupBox(self)
        sql = "select * from customer where `username` = '%s'" % request[2]
        self.cursor.execute(sql)
        cust_info = self.cursor.fetchone()
        sql = "select * from merchant where `username` = '%s'" % request[3]
        self.cursor.execute(sql)
        merchant_info = self.cursor.fetchone()

        pic = QLabel(self)
        pic.setPixmap(QPixmap(cust_info[4]))
        pic.setScaledContents(True)
        pic.resize(50, 50)
        pic.move(0, 0)

        name = QLabel(self)
        name.setText("下单用户: "+cust_info[0])

        mname = QLabel(self)
        mname.setText("店铺名称: " + merchant_info[5])

        order_time = QLabel(self)
        order_time.setText("下单时间: "+request[1].strftime("%Y-%m-%d %H:%M:%S"))

        address = QLabel(self)
        address.setText("店铺地址:(%d,%d) 送达地址:(%d,%d) " % (merchant_info[6], merchant_info[7], cust_info[7], cust_info[8]))

        order_id = QLabel(self)
        order_id.setText("订单号:%d" % request[0])

        text_layout = QVBoxLayout()
        text_layout.addWidget(order_id)
        text_layout.addWidget(name)
        text_layout.addWidget(mname)
        text_layout.addWidget(order_time)
        text_layout.addWidget(address)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        accept_button = QPushButton(self)
        if request[4] == 1:
            accept_button.setText("配送")
            accept_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        elif request[4] == 2:
            accept_button.setText("送达")
            accept_button.setStyleSheet("background-color: rgb(238, 44, 44)")
        accept_button.clicked.connect(lambda: self.accept_order(accept_button, request[0], request[4], cust_info[0], merchant_info[0]))

        button_layout = QVBoxLayout()
        button_layout.addWidget(accept_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        main_layout.addWidget(button_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def accept_order(self, btn, order_id, state, cust_name, merchant_name):
        if state == 1:
            try:
                sql = "update `order` set `rider_name` = '%s' where `order_id` = %d" % (self.info[0], order_id)
                sql1 = "update `order` set `state` = 2 where `order_id` = %d" % order_id
                sql2 = "update `order` set `rider_accept_time` = '%s' where `order_id` = %d" % (util.get_time(), order_id)
                self.cursor.execute(sql)
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)
                self.connect.commit()
                btn.setStyleSheet("background-color: rgb(232, 232, 232)")
                btn.setText("已接受")
            except:
                self.connect.rollback()
                QMessageBox.critical(self, "饱了没", "接受失败!\n请检查数据库连接!")
        elif state == 2:
            try:
                sql = "select sumMoney(%d)" % order_id
                self.cursor.execute(sql)
                money = self.cursor.fetchone()[0]
                sql = ["" for i in range(7)]
                sql[0] = "update `order` set `state` = 3 where `order_id` = %d" % order_id
                sql[1] = "update `order` set `finish_time` = '%s' where `order_id` = %d" % (util.get_time(), order_id)
                sql[2] = "update `customer` set `sum_order` = `sum_order`+1 where `username` = '%s'" % cust_name
                sql[3] = "update `merchant` set `sum_order` = `sum_order`+1 where `username` = '%s'" % merchant_name
                sql[4] = "update `merchant` set `income` = `income`+%f where `username` = '%s'" %(money * 0.9, merchant_name)
                sql[5] = "update `rider` set `sum_order` = `sum_order`+1 where `username` = '%s'" % self.info[0]
                sql[6] = "update `rider` set `income` = `income`+%f where `username` = '%s'" % (money * 0.1, self.info[0])
                for i in range(7): self.cursor.execute(sql[i])
                self.connect.commit()
                btn.setStyleSheet("background-color: rgb(232, 232, 232)")
                btn.setText("已送达")
            except:
                self.connect.rollback()
                QMessageBox.critical(self, "饱了没", "接受失败!\n请检查数据库连接!")


    def func_rank_button(self):
        self.info_refresh()
        sql = "select * from `rider` order by `sum_order` desc"
        self.cursor.execute(sql)
        all_riders = self.cursor.fetchall()

        self.dialog = QDialog()
        self.dialog.setFixedSize(1200, 1200)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))
        self.dialog.setWindowTitle("骑手排行")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setPalette(self.login_palette)

        dishes_list = QScrollArea(self.dialog)
        dishes_list.move(0, 0)
        dishes_list.resize(1200, 1200)
        items = QWidget()
        vLayout = QVBoxLayout(items)
        rank = 1
        for rider in all_riders:
            vLayout.addWidget(self.create_rank_item(rider, rank))
            rank += 1
        dishes_list.setWidget(items)
        self.dialog.exec_()

    def create_rank_item(self, rider, rank):
        groupBox = QGroupBox(self)
        pic = QLabel(self)
        pic.setPixmap(QPixmap(rider[2]))
        pic.setScaledContents(True)
        pic.resize(150, 150)
        pic.move(0, 0)

        name = QLabel(self)
        tmp = rider[0]
        length = 28
        if(len(tmp)) > length: tmp = tmp[:length]
        while(len(tmp)) < length: tmp += " "
        name.setText(tmp)
        rank_label = QLabel("排名: %d" % rank, self)
        sum_order = QLabel("总单数:"+str(rider[4]), self)
        score = QLabel(self)
        if rider[8] == 0: score.setText("评分: 0.0")
        else: score.setText("评分: %.1f" % (rider[5]/rider[8]))


        text_layout = QVBoxLayout()
        text_layout.addWidget(name)
        text_layout.addWidget(rank_label)
        text_layout.addWidget(sum_order)
        text_layout.addWidget(score)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def delete_dish(self, btn, dish_id):
        try:
            sql = "delete from `product` where `product_id` = %d" % dish_id
            self.cursor.execute(sql)
            self.connect.commit()
            btn.setText("已删除")
        except:
            self.connect.rollback()
            QMessageBox.critical(self, "饱了没", "删除失败!\n请检查数据库连接!")

    def change_dish_name(self, btn, dish_id):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_name = QLineEdit(self.dialog)
        input_name.setFont(QFont("宋体", 12))
        input_name.resize(450, 50)
        input_name.setPlaceholderText("输入新名称")
        input_name.move(25, 20)
        input_name.setMaxLength(50)

        confirm = QPushButton("确认修改", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_dish_name(input_name.text(), dish_id, btn))

        self.dialog.setWindowTitle("修改菜品名称")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_dish_name(self, name, dish_id, btn):
        if len(name) == 0:
            QMessageBox.critical(self, "饱了没", "名称不能为空!")
        else:
            try:
                sql = "update `product` set `name` = '%s' where `product_id` = %s" % (name, dish_id)
                self.cursor.execute(sql)
                self.connect.commit()
                length = 28
                if (len(name)) > length: name = name[:length]
                while (len(name)) < length: name += " "
                btn.setText(name)
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

    def change_dish_price(self, btn, dish_id):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_price = QLineEdit(self.dialog)
        input_price.setFont(QFont("宋体", 12))
        input_price.resize(450, 50)
        input_price.setPlaceholderText("输入新价格")
        input_price.move(25, 20)
        input_price.setMaxLength(50)

        confirm = QPushButton("确认修改", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_dish_price(input_price.text(), dish_id, btn))

        self.dialog.setWindowTitle("修改菜品价格")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_dish_price(self, price, dish_id, btn):
        try:
            price = float(price)
            if price <= 0:
                QMessageBox.critical(self, "饱了没", "价格必须是正数!")
                return
        except:
            QMessageBox.critical(self, "饱了没", "输入格式有误")
            return
        try:
            sql = "update `product` set `price` = '%s' where `product_id` = %s" % (price, dish_id)
            self.cursor.execute(sql)
            self.connect.commit()
            btn.setText("价格:" + str(price) + "元")
            self.dialog.close()
        except:
            QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")


    def change_dish_num(self, btn, dish_id):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_num = QLineEdit(self.dialog)
        input_num.setFont(QFont("宋体", 12))
        input_num.resize(450, 50)
        input_num.setPlaceholderText("输入库存")
        input_num.move(25, 20)
        input_num.setMaxLength(50)

        confirm = QPushButton("确认修改", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_dish_num(input_num.text(), dish_id, btn))

        self.dialog.setWindowTitle("修改菜品库存")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_dish_num(self, num, dish_id, btn):
        try:
            num = int(num)
            if num < 0:
                QMessageBox.critical(self, "饱了没", "库存不能是负数!")
                return
        except:
            QMessageBox.critical(self, "饱了没", "输入格式有误")
            return
        try:
            sql = "update `product` set `left` = '%s' where `product_id` = %s" % (num, dish_id)
            self.cursor.execute(sql)
            self.connect.commit()
            btn.setText("剩余:" + str(num))
            self.dialog.close()
        except:
            QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

    def func_evaluate_button(self):
        self.info_refresh()
        sql = "select `order_id`,`customer_name`,`score`,`comment` " \
              "from `order` inner join `evaluate` " \
              "on `order`.`rider_evaluate_id` = `evaluate`.`evaluate_id` " \
              "where `order`.`rider_name` = '%s'" % self.info[0]
        self.cursor.execute(sql)
        all_evaluate = self.cursor.fetchall()
        if len(all_evaluate) == 0:
            QMessageBox.about(self, "饱了没", "暂无评价!")
            return
        self.dialog = QDialog()
        self.dialog.setFixedSize(1200, 1200)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))
        self.dialog.setWindowTitle("我的评价")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setPalette(self.login_palette)

        request_list = QScrollArea(self.dialog)
        request_list.move(0, 0)
        request_list.resize(1200, 1200)
        items = QWidget()
        vLayout = QVBoxLayout(items)
        for evaluate in all_evaluate:
            vLayout.addWidget(self.create_evaluate_item(evaluate))
        request_list.setWidget(items)
        self.dialog.exec_()

    def create_evaluate_item(self, evaluate):
        groupBox = QGroupBox(self)
        sql = "select `portrait` from customer where `username` = '%s'" % evaluate[1]
        self.cursor.execute(sql)
        path = self.cursor.fetchone()[0]
        pic = QLabel(self)
        pic.setPixmap(QPixmap(path))
        pic.setScaledContents(True)
        pic.resize(50, 50)
        pic.move(0, 0)

        name = QLabel(self)
        name.setText("评价用户: " + evaluate[1])

        score = QLabel(self)
        score.setText("评分: " + evaluate[2] * "★")

        comment = QLabel(self)
        comment.setText("评价内容: " + evaluate[3])

        order_id = QLabel(self)
        order_id.setText("订单号:%d" % evaluate[0])

        text_layout = QVBoxLayout()
        text_layout.addWidget(order_id)
        text_layout.addWidget(name)
        text_layout.addWidget(score)
        text_layout.addWidget(comment)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def pull_apply(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_name = QLineEdit(self.dialog)
        input_name.setFont(QFont("宋体", 12))
        input_name.resize(450, 50)
        input_name.setPlaceholderText("输入商家ID")
        input_name.move(25, 20)
        input_name.setMaxLength(50)

        confirm = QPushButton("发送申请", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_pull_apply(input_name.text()))

        self.dialog.setWindowTitle("申请签约")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_pull_apply(self, name):
        if len(name) == 0:
            QMessageBox.critical(self, "饱了没", "名称不能为空!")
        else:
            sql = "select count(*) from `users` where `username` = '%s' and `user_type` = 'merchant'" % name
            self.cursor.execute(sql)
            if self.cursor.fetchone()[0] == 0:
                QMessageBox.critical(self, "饱了没", "该商家不存在!")
            else:
                sql = "select count(*) from `apply` where `rider_name` = '%s' " \
                      "and `merchant_name` = '%s'" % (self.info[0], name)
                self.cursor.execute(sql)
                if self.cursor.fetchone()[0] != 0:
                    QMessageBox.critical(self, "饱了没", "申请已存在!\n请等待商家处理!")
                    return
                sql = "select count(*) from `contract` where `rider_name` = '%s' " \
                      "and `merchant_name` = '%s'" % (self.info[0], name)
                self.cursor.execute(sql)
                if self.cursor.fetchone()[0] != 0:
                    QMessageBox.critical(self, "饱了没", "契约已存在!\n请勿重复操作")
                    return
                try:
                    sql = "insert into `apply` values('%s','%s', 1)" % (self.info[0], name)
                    self.cursor.execute(sql)
                    self.connect.commit()
                    QMessageBox.about(self, "饱了没", "发送成功!")
                    self.dialog.close()
                except:
                    QMessageBox.critical(self, "饱了没", "发送失败!\n请检查数据库连接!")

    def func_contract_button(self):
        self.info_refresh()
        sql = "select * from `apply` where `rider_name` = '%s' and `direction` = 0" % self.info[0]
        self.cursor.execute(sql)
        all_apply = self.cursor.fetchall()
        self.dialog = QDialog()
        self.dialog.setFixedSize(1400, 1400)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))
        self.dialog.setWindowTitle("签约商家")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setPalette(self.login_palette)

        launch = QPushButton("发出申请", self.dialog)
        launch.resize(180, 50)
        launch.setFont(QFont("宋体", 12))
        launch.setStyleSheet("background-color: rgb(51, 153, 255)")
        launch.move(50, 20)
        launch.clicked.connect(self.pull_apply)

        request_list = QScrollArea(self.dialog)
        request_list.move(0, 100)
        request_list.resize(1400, 1300)
        items = QWidget()
        vLayout = QVBoxLayout(items)
        for apply in all_apply:
            vLayout.addWidget(self.create_apply_item(apply))
        request_list.setWidget(items)
        self.dialog.exec_()

    def create_apply_item(self, apply):
        groupBox = QGroupBox(self)
        sql = "select * from `merchant` where `username` = '%s'" % apply[1]
        self.cursor.execute(sql)
        merchant_info = self.cursor.fetchone()
        pic = QLabel(self)
        pic.setPixmap(QPixmap(merchant_info[10]))
        pic.setScaledContents(True)
        pic.resize(50, 50)
        pic.move(0, 0)

        name = QLabel(self)
        name.setText("申请商家: " + merchant_info[0])
        sum_order = QLabel(self)
        sum_order.setText("商家总单数: " + str(merchant_info[3]))

        score = QLabel(self)
        if merchant_info[12] == 0:
            score.setText("商家评分: 0.0")
        else:
            score.setText("商家评分: %.1f" % (merchant_info[4] / merchant_info[12]))
        address = QLabel(self)
        address.setText("商家地址: (%d, %d)" % (merchant_info[6], merchant_info[7]))

        text_layout = QVBoxLayout()
        text_layout.addWidget(name)
        text_layout.addWidget(sum_order)
        text_layout.addWidget(score)
        text_layout.addWidget(address)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        accept_button = QPushButton("接受", self)
        accept_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        accept_button.clicked.connect(lambda: self.accept_contract(accept_button, merchant_info[0]))

        button_layout = QVBoxLayout()
        button_layout.addWidget(accept_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        main_layout.addWidget(button_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def accept_contract(self, btn, name):
        try:
            sql1 = "delete from `apply` " \
                   "where `rider_name` = '%s'" \
                   "and `merchant_name` = '%s'" % (self.info[0], name)
            sql2 = "insert into `contract` values('%s','%s')" % (self.info[0], name)
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.connect.commit()
            btn.setText("已接受")
            btn.setStyleSheet("background-color: rgb(232, 232, 232)")
        except:
            self.connect.rollback()
            QMessageBox.critical(self, "饱了没", "接受失败!\n请检查数据库连接!")


    def change_password_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 360)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        origin_password = QLineEdit(self.dialog)
        origin_password.setFont(QFont("宋体", 12))
        origin_password.resize(450, 50)
        origin_password.setPlaceholderText("输入原密码")
        origin_password.move(25, 20)
        origin_password.setEchoMode(QLineEdit.Password)
        origin_password.setMaxLength(18)

        new_password = QLineEdit(self.dialog)
        new_password.setFont(QFont("宋体", 12))
        new_password.resize(450, 50)
        new_password.setPlaceholderText("输入新密码")
        new_password.move(25, 100)
        new_password.setEchoMode(QLineEdit.Password)
        new_password.setMaxLength(18)

        confirm_password = QLineEdit(self.dialog)
        confirm_password.setFont(QFont("宋体", 12))
        confirm_password.resize(450, 50)
        confirm_password.setPlaceholderText("确认新密码")
        confirm_password.move(25, 180)
        confirm_password.setEchoMode(QLineEdit.Password)
        confirm_password.setMaxLength(18)

        confirm = QPushButton("修改密码", self.dialog)
        confirm.move(25, 260)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_change_password([origin_password.text(), new_password.text(), confirm_password.text()]))

        self.dialog.setWindowTitle("修改密码")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_change_password(self, passwords):
        if passwords[0] != self.info[1]:
            QMessageBox.critical(self, "饱了没", "原密码错误!")
        elif len(passwords[1]) < 6:
            QMessageBox.critical(self, "饱了没", "密码长度过短!")
        elif passwords[1] != passwords[2]:
            QMessageBox.critical(self, "饱了没", "两次输入密码不一致!")
        else:
            sql = "update users set `password` = '%s' where `username` = '%s'" % (passwords[1], self.info[0])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                self.info[1] = passwords[1]
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

    def change_order(self, var):
        self.order_index += var
        self.display_order(self.order_index)

    def display_order(self, index):
        self.order_index = index
        self.show_order.setText(str(self.order_index + 1))
        if index == 0:
            self.pre_order.setVisible(False)
        else:
            self.pre_order.setVisible(True)

        if index == self.sum_order - 1:
            self.next_order.setVisible(False)
        else:
            self.next_order.setVisible(True)
        sql = "select * from `sell` where `order_id` = %d" % self.all_orders[self.order_index][0]
        self.cursor.execute(sql)
        self.all_product = self.cursor.fetchall()
        items = QWidget()
        vLayout = QVBoxLayout(items)
        for product in self.all_product:
            vLayout.addWidget(self.create_product_item_2(product))
        self.products.setWidget(items)
        self.update()

    def create_product_item_2(self, product):
        groupBox = QGroupBox(self)
        num = product[2]
        sql = "select * from `product` where `product_id` = %d" % product[1]
        self.cursor.execute(sql)
        product = self.cursor.fetchone()
        price = num*product[1]
        pic = QLabel(self)
        pic.setPixmap(QPixmap(product[3]))
        pic.setScaledContents(True)
        pic.resize(150, 150)
        pic.move(0, 0)

        name = QLabel(self)
        tmp = product[4]
        length = 25
        if(len(tmp)) > length: tmp = tmp[:length]
        while(len(tmp)) < length: tmp += " "
        name.setText(tmp)
        num_label = QLabel("x %d" % num, self)
        price_label = QLabel("￥%.2f" % price, self)

        text_layout = QVBoxLayout()
        text_layout.addWidget(name)
        text_layout.addWidget(num_label)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        price_layout = QVBoxLayout()
        price_layout.addWidget(price_label)
        price_widget = QWidget()
        price_widget.setLayout(price_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        main_layout.addWidget(price_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.INDEX == self.ORDER:
            self.paint_order(event, qp)
        elif self.INDEX == self.PERSONAL:
            self.paint_personal(event, qp)
        qp.end()

    def val(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def paint_order(self, event, qp):
        item = self.all_orders[self.order_index]
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("宋体", 12))
        qp.drawText(20, 250, "订单号: "+str(item[0]))
        tmp = ["已下单", "商家已接单", "骑手正在配送", "已送达"]
        qp.drawText(20, 300, "订单状态: " + tmp[item[5]])
        qp.drawText(20, 350, "下单用户: " + item[6])
        sql = "select `name` from merchant where `username` = '%s'" % item[8]
        qp.drawText(20, 400, "商家名称: " + self.val(sql))
        if item[7] is not None: qp.drawText(20, 450, "配送骑手: " + item[7])
        else: qp.drawText(20, 450, "配送骑手: 暂无")
        if item[5] == 3: qp.drawText(400, 300, "送达时间: "+str(item[4]))
        qp.drawText(400, 350, "下单时间: "+str(item[1]))
        tmp = "暂无"
        if item[2] is not None: tmp = str(item[2])
        qp.drawText(400, 400, "接单时间: "+tmp)
        tmp = "暂无"
        if item[3] is not None: tmp = str(item[3])
        qp.drawText(400, 450, "配送时间: "+tmp)
        sql = "select sumMoney(%d)" % item[0]
        qp.drawText(20, 500, "订单金额: " + str(self.val(sql)))
        tmp = 0
        for e in self.all_product: tmp += e[2]
        qp.drawText(400, 500, "商品总数: " + str(tmp))

    def paint_personal(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("宋体", 12))
        qp.drawText(350, 250, "ID:" + self.info[0])
        d = {"common": "初级", "medium": "中级", "expert": "高级"}
        qp.drawText(350, 340, "等级:"+d[self.info[7]])
        qp.drawText(350, 435, "注册:" + self.info[5].strftime('%Y-%m-%d'))
        qp.drawText(70, 540, "邮箱: " + self.info[4])
        qp.drawText(70, 645, "电话: " + self.info[3])
        qp.drawText(70, 750, "收入: " + str(float(self.info[13])) + "元")
        if self.info[12] == 0: qp.drawText(70, 855, "评分: 0.0")
        else: qp.drawText(70, 855, "评分: %.1f" % (self.info[9]/self.info[12]))
        qp.drawText(70, 960, "总订单数: " + str(int(self.info[8])))
        qp.drawText(70, 1065, "地址: (%d, %d)" % (int(self.info[10]), int(self.info[11])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Rider("rider")
    win.show()
    sys.exit(app.exec_())
    pass
