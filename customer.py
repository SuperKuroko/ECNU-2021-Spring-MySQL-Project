from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pymysql import *
import sys
import os
import re
import sent_email
import util


class Customer(QWidget):
    to_login = pyqtSignal()

    def __init__(self, username):
        super(Customer, self).__init__()
        self.connect = Connect(
            host="124.71.228.59",
            port=3306,
            user="DB_USER066",
            passwd="DB_USER066@123",
            db="user066db",
            charset="utf8"
        )
        self.dialog = None
        self.cursor = self.connect.cursor()
        self.setFixedSize(900, 1400)
        self.setWindowIcon(QIcon("./image/icon.jpg"))
        self.setWindowTitle("饱了没-顾客版")
        self.username = username
        self.info = None
        self.all_orders = []
        self.info_refresh()
        print(self.info)
        self.login_palette = QPalette()
        self.login_palette.setColor(self.backgroundRole(), QColor(255, 255, 255))  # 设置背景颜色
        self.setPalette(self.login_palette)
        self.all_items = []
        self.INDEX = 0
        self.MAIN = 0
        self.ORDER = 1
        self.PERSONAL = 2
        self.BROWSE = 3
        self.DETAIL = 4

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
        self.logo.move(200, 0)

        self.search_bar = QLineEdit(self)
        self.search_bar.resize(650, 60)
        self.search_bar.setFont(QFont('宋体', 12))
        self.search_bar.setPlaceholderText("搜索")
        self.search_bar.move(30, 190)
        self.search_bar.setMaxLength(500)

        self.search_button = QPushButton("搜索", self)
        self.search_button.move(700, 190)
        self.search_button.resize(150, 60)
        self.search_button.setFont(QFont('幼圆', 13))
        self.search_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.search_button.clicked.connect(self.search_algorithm)

        self.cate = QLabel(self)
        self.cate.setPixmap(QPixmap("./image/cate_real.jpg"))
        self.cate.setScaledContents(True)
        self.cate.resize(430, 430)
        self.cate.move(10, 280)

        self.cate_button = QPushButton("美食外卖", self)
        self.cate_button.move(10, 710)
        self.cate_button.resize(430, 60)
        self.cate_button.setFont(QFont('幼圆', 13))
        # self.cate_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.cate_button.clicked.connect(self.func_cate_button)

        self.supermarket = QLabel(self)
        self.supermarket.setPixmap(QPixmap("./image/supermarket_real.jpg"))
        self.supermarket.setScaledContents(True)
        self.supermarket.resize(430, 430)
        self.supermarket.move(460, 280)

        self.supermarket_button = QPushButton("超市便利", self)
        self.supermarket_button.move(460, 710)
        self.supermarket_button.resize(430, 60)
        self.supermarket_button.setFont(QFont('幼圆', 13))
        # self.supermarket_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.supermarket_button.clicked.connect(self.func_supermarket_button)

        self.drug = QLabel(self)
        self.drug.setPixmap(QPixmap("./image/drug_real.jpg"))
        self.drug.setScaledContents(True)
        self.drug.resize(430, 430)
        self.drug.move(10, 810)

        self.drug_button = QPushButton("健民药房", self)
        self.drug_button.move(10, 1240)
        self.drug_button.resize(430, 60)
        self.drug_button.setFont(QFont('幼圆', 13))
        # self.drug_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.drug_button.clicked.connect(self.func_drug_button)

        self.fruit = QLabel(self)
        self.fruit.setPixmap(QPixmap("./image/fruit_real.jpg"))
        self.fruit.setScaledContents(True)
        self.fruit.resize(430, 430)
        self.fruit.move(460, 810)

        self.fruit_button = QPushButton("鲜果时蔬", self)
        self.fruit_button.move(460, 1240)
        self.fruit_button.resize(430, 60)
        self.fruit_button.setFont(QFont('幼圆', 13))
        # self.fruit_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.fruit_button.clicked.connect(self.func_fruit_button)

        self.cate.setPixmap(QPixmap("./image/cate_abstract.jpg"))
        self.supermarket.setPixmap(QPixmap("./image/supermarket_abstract.jpg"))
        self.drug.setPixmap(QPixmap("./image/drug_abstract.jpg"))
        self.fruit.setPixmap(QPixmap("./image/fruit_abstract.jpg"))

        self.main_items = []
        self.main_items.append(self.logo)
        self.main_items.append(self.search_bar)
        self.main_items.append(self.search_button)
        self.main_items.append(self.cate)
        self.main_items.append(self.cate_button)
        self.main_items.append(self.drug)
        self.main_items.append(self.drug_button)
        self.main_items.append(self.supermarket)
        self.main_items.append(self.supermarket_button)
        self.main_items.append(self.fruit)
        self.main_items.append(self.fruit_button)
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

        self.evaluate_rider = QPushButton("评价骑手", self)
        self.evaluate_rider.resize(180, 50)
        self.evaluate_rider.setFont(QFont('宋体', 10))
        self.evaluate_rider.move(410, 210)
        self.evaluate_rider.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.evaluate_rider.clicked.connect(lambda: self.evaluate_order(1))

        self.evaluate_merchant = QPushButton("评价商家", self)
        self.evaluate_merchant.resize(180, 50)
        self.evaluate_merchant.setFont(QFont('宋体', 10))
        self.evaluate_merchant.move(650, 210)
        self.evaluate_merchant.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.evaluate_merchant.clicked.connect(lambda: self.evaluate_order(2))

        self.all_product = None
        self.order_items = []
        self.order_items.append(self.pre_order)
        self.order_items.append(self.next_order)
        self.order_items.append(self.show_order)
        self.order_items.append(self.order_logo)
        self.order_items.append(self.products)
        self.order_items.append(self.evaluate_rider)
        self.order_items.append(self.evaluate_merchant)
        self.all_items.append(self.order_items)

        self.personal_portrait = QLabel(self)
        self.personal_portrait.setPixmap(QPixmap(self.info[4]))
        self.personal_portrait.setScaledContents(True)
        self.personal_portrait.resize(250, 250)
        self.personal_portrait.move(50, 210)

        self.change_password = QPushButton("修改密码", self)
        self.change_password.resize(180, 50)
        self.change_password.setFont(QFont("宋体", 12))
        self.change_password.move(650, 215)
        self.change_password.clicked.connect(self.change_password_dialog)

        self.vip_button = QPushButton("充值会员", self)
        self.vip_button.resize(180, 50)
        self.vip_button.setFont(QFont("宋体", 12))
        self.vip_button.move(650, 305)
        self.vip_button.clicked.connect(self.become_vip_dialog)

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

        self.top_up = QPushButton("充值钱包", self)
        self.top_up.resize(180, 50)
        self.top_up.setFont(QFont('宋体', 12))
        self.top_up.move(650, 715)
        self.top_up.clicked.connect(self.top_up_dialog)

        self.use_points = QPushButton("积分兑换", self)
        self.use_points.resize(180, 50)
        self.use_points.setFont(QFont('宋体', 12))
        self.use_points.move(650, 820)
        self.use_points.clicked.connect(self.use_points_dialog)

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
        self.personal_items.append(self.logo)
        self.personal_items.append(self.change_portrait)
        self.personal_items.append(self.personal_portrait)
        self.personal_items.append(self.vip_button)
        self.personal_items.append(self.change_password)
        self.personal_items.append(self.change_email)
        self.personal_items.append(self.change_phone)
        self.personal_items.append(self.use_points)
        self.personal_items.append(self.top_up)
        self.personal_items.append(self.change_address)
        self.personal_items.append(self.quit)
        self.all_items.append(self.personal_items)

        self.entries = [[QLabel(self) for i in range(5)] for j in range(8)]
        self.result = None
        for i in range(8):
            if i < 4:
                x = 10
                y = 280 + i * 260
            else:
                x = 460
                y = 280 + (i - 4) * 260
            self.entries[i][0].setPixmap(QPixmap("./image/cate_real.jpg"))
            self.entries[i][0].setScaledContents(True)
            self.entries[i][0].resize(220, 220)
            self.entries[i][0].move(x, y)

            self.entries[i][1].setText("这是一个标题")
            self.entries[i][1].setFont(QFont("宋体", 12))
            self.entries[i][1].move(x + 230, y + 5)
            self.entries[i][1].resize(200, 50)

            self.entries[i][2].setText("销量1230")
            self.entries[i][2].setFont(QFont("宋体", 10))
            self.entries[i][2].move(x + 230, y + 85)
            self.entries[i][2].resize(200, 50)

            self.entries[i][3].setText("1.0km")
            self.entries[i][3].setFont(QFont("宋体", 10))
            self.entries[i][3].move(x + 230, y + 135)
            self.entries[i][3].resize(200, 50)

            self.entries[i][4].setText("4.6分")
            self.entries[i][4].setFont(QFont("宋体", 10))
            self.entries[i][4].move(x + 230, y + 185)
            self.entries[i][4].resize(200, 50)

        self.page = 0
        self.sum_page = 10
        self.pre_page = QPushButton("上一页", self)
        self.pre_page.resize(160, 50)
        self.pre_page.setFont(QFont('幼圆', 10))
        self.pre_page.move(210, 1287)
        self.pre_page.clicked.connect(lambda: self.change_page(-1))

        self.next_page = QPushButton("下一页", self)
        self.next_page.resize(160, 50)
        self.next_page.setFont(QFont('幼圆', 10))
        self.next_page.move(530, 1287)
        self.next_page.clicked.connect(lambda: self.change_page(1))

        self.show_page = QPushButton(str(self.page + 1), self)
        self.show_page.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.show_page.resize(60, 50)
        self.show_page.setFont(QFont('幼圆', 12))
        self.show_page.move(420, 1287)
        self.current_cnt = 0

        self.browse_items = []
        self.browse_items.append(self.logo)
        self.browse_items.append(self.search_bar)
        self.browse_items.append(self.search_button)
        for i in range(len(self.entries)):
            self.browse_items += self.entries[i]
        self.browse_items.append(self.pre_page)
        self.browse_items.append(self.next_page)
        self.browse_items.append(self.show_page)
        self.all_items.append(self.browse_items)

        self.merchant_logo = QLabel(self)
        self.merchant_logo.setPixmap(QPixmap("./image/logo.png"))
        self.merchant_logo.setScaledContents(True)
        self.merchant_logo.resize(200, 200)
        self.merchant_logo.move(10, 20)

        self.product_list = QScrollArea(self)
        self.product_list.move(0, 230)
        self.product_list.resize(900, 1000)
        self.buy_count = {}
        self.number = [QLabel("", self) for i in range(1000)]
        self.sum_money = 0

        self.back_to_browse_button = QPushButton("返回", self)
        self.back_to_browse_button.setFont(QFont("幼圆", 14))
        self.back_to_browse_button.resize(300, 60)
        self.back_to_browse_button.move(0, 1255)
        self.back_to_browse_button.clicked.connect(self.back_to_browse)

        self.purchase = QPushButton("结算", self)
        self.purchase.setStyleSheet("background-color: rgb(51, 153, 255)")
        self.purchase.setFont(QFont("幼圆", 14))
        self.purchase.resize(300, 60)
        self.purchase.move(600, 1255)
        self.purchase.clicked.connect(self.cost_money_dialog)

        self.sum = QLabel("合计%5d元" % self.sum_money, self)
        self.sum.setFont(QFont("幼圆", 14))
        self.sum.resize(250, 60)
        self.sum.move(340, 1255)
        self.merchant_info = None

        self.detail_items = []
        self.detail_items.append(self.merchant_logo)
        self.detail_items.append(self.product_list)
        self.detail_items.append(self.back_to_browse_button)
        self.detail_items.append(self.purchase)
        self.detail_items.append(self.sum)
        self.all_items.append(self.detail_items)
        self.show_interface(self.MAIN)

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
        sql = "select * from `customer` where username = '%s'" % self.username
        self.cursor.execute(sql)
        self.info = list(self.cursor.fetchone())
        sql = "select * from `users` where username = '%s'" % self.username
        self.cursor.execute(sql)
        self.info += list(self.cursor.fetchone())[1:]
        sql = "select * from `order` where `customer_name` = '%s'" % self.username
        self.cursor.execute(sql)
        self.all_orders = self.cursor.fetchall()

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

    def search_algorithm(self):
        sql = "select * from merchant"
        self.cursor.execute(sql)
        self.result = []
        tmp = self.cursor.fetchall()
        for e in tmp:
            key = e[0]+e[5]
            if e[-3] is not None: key += e[-3]
            if key.find(self.search_bar.text()) != -1:
                self.result.append(e)
        self.show_interface(self.BROWSE)
        self.show_items(0)

    def func_cate_button(self):
        sql = "select * from merchant where `sale_type` = '%s'" % "cate"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.show_interface(self.BROWSE)
        self.show_items(0)

    def func_supermarket_button(self):
        sql = "select * from merchant where `sale_type` = '%s'" % "supermarket"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.show_interface(self.BROWSE)
        self.show_items(0)

    def func_drug_button(self):
        sql = "select * from merchant where `sale_type` = '%s'" % "drug"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.show_interface(self.BROWSE)
        self.show_items(0)

    def func_fruit_button(self):
        sql = "select * from merchant where `sale_type` = '%s'" % "fruit"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.show_interface(self.BROWSE)
        self.show_items(0)

    @staticmethod
    def distance(x1, y1, x2, y2):
        x1 = (x1-x2)**2
        y1 = (y1-y2)**2
        return pow(x1+y1, 0.5)

    def back_to_browse(self):
        self.show_interface(self.BROWSE)
        self.show_items(self.page)

    def show_items(self, page):
        self.page = page
        self.show_page.setText(str(self.page + 1))
        self.sum_page = len(self.result) // 8
        if len(self.result) % 8 != 0: self.sum_page += 1
        if page == 0:
            self.pre_page.setVisible(False)
        else:
            self.pre_page.setVisible(True)

        if page == self.sum_page - 1:
            self.next_page.setVisible(False)
        else:
            self.next_page.setVisible(True)

        if len(self.result) == 0:
            self.pre_page.setVisible(False)
            self.next_page.setVisible(False)

        start_index = page * 8
        self.current_cnt = min(len(self.result)-start_index, 8)
        for i in range(self.current_cnt):
            self.entries[i][0].setPixmap(QPixmap(self.result[start_index + i][10]))
            self.entries[i][1].setText(self.result[start_index + i][5])
            self.entries[i][2].setText("销量%d" % self.result[start_index + i][3])
            x1 = self.info[7]
            y1 = self.info[8]
            x2 = self.result[start_index + i][6]
            y2 = self.result[start_index + i][7]
            self.entries[i][3].setText("%.1fm" % self.distance(x1, y1, x2, y2))
            if self.result[start_index+i][12] == 0: score = 0
            else: score = self.result[start_index+i][4]/self.result[start_index+i][12]
            self.entries[i][4].setText("%.1f分" % score)
        for i in range(self.current_cnt, 8):
            self.entries[i][0].setPixmap(QPixmap(""))
            for j in range(1, 5):
                self.entries[i][j].setText("")

    def evaluate_order(self, type):
        self.info_refresh()
        if self.all_orders[self.order_index][5] != 3:
            QMessageBox.about(self, "饱了没", "订单尚未送达,请送达后评价!")
            return
        if self.all_orders[self.order_index][9] is not None and type == 2:
            sql = "select * from `evaluate` where `evaluate_id` = %d" % (self.all_orders[self.order_index][9])
            self.cursor.execute(sql)
            e = self.cursor.fetchone()
            print(e)
            s = "★"*e[1]
            print(s)
            QMessageBox.about(self, "饱了没", "订单已评价!\n评分:%s\n评价内容:%s" % (s, e[2]))
            return
        if self.all_orders[self.order_index][10] is not None and type == 1:
            sql = "select * from `evaluate` where `evaluate_id` = %d" % (self.all_orders[self.order_index][10])
            self.cursor.execute(sql)
            e = self.cursor.fetchone()
            s = "★"*e[1]
            QMessageBox.about(self, "饱了没", "订单已评价!\n评分:%s\n评价内容:%s" % (s, e[2]))
            return
        self.dialog = QDialog()
        self.dialog.setFixedSize(800, 500)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        text = QLabel("请选择评分:", self.dialog)
        text.resize(200, 50)
        text.move(20, 20)
        text.setFont(QFont('宋体', 11))

        mark = QComboBox(self.dialog)
        mark.addItems([str(i) for i in range(1, 6)])
        mark.setFont(QFont('宋体', 10))
        mark.resize(100, 40)
        mark.move(230, 25)

        comment = QTextEdit(self.dialog)
        comment.resize(760, 400)
        comment.move(20, 80)
        comment.setFont(QFont('宋体', 10))
        comment.setPlaceholderText("请输入评价内容")

        commit = QPushButton("提交", self.dialog)
        commit.setStyleSheet("background-color: rgb(51, 153, 255)")
        commit.move(600, 25)
        commit.resize(150, 45)
        commit.setFont(QFont('宋体', 11))
        commit.clicked.connect(lambda: self.commit_comment(type, int(mark.currentText()), comment.toPlainText(),
                                                           self.all_orders[self.order_index][7],
                                                           self.all_orders[self.order_index][8]))

        self.dialog.setWindowTitle("评价订单")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def commit_comment(self, type, mark, comment, rider_name, merchant_name):
        try:
            sql = "select get_biggest_evaluate_id();"
            self.cursor.execute(sql)
            evaluate_id = self.cursor.fetchone()[0]
            sql = "insert into `evaluate`(`evaluate_id`, `score`, `comment`) values(%d, %d, '%s')" % (evaluate_id, mark, comment)
            self.cursor.execute(sql)
            if type == 1:
                sql1 = "update `order` set `rider_evaluate_id` = %d where `order_id` = %d" % (evaluate_id, self.all_orders[self.order_index][0])
                sql2 = "update `rider` set `evaluate_cnt` = `evaluate_cnt`+1 where `username` = '%s'" % rider_name
                sql3 = "update `rider` set `evaluate_sum` = `evaluate_sum`+%d where `username` = '%s'" % (mark, rider_name)
            else:
                sql1 = "update `order` set `merchant_evaluate_id` = %d where `order_id` = %d" % (evaluate_id, self.all_orders[self.order_index][0])
                sql2 = "update `merchant` set `evaluate_cnt` = `evaluate_cnt`+1 where `username` = '%s'" % merchant_name
                sql3 = "update `merchant` set `evaluate_sum` = `evaluate_sum`+%d where `username` = '%s'" % (mark, merchant_name)
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.cursor.execute(sql3)
            self.connect.commit()
            self.dialog.close()
        except:
            self.connect.rollback()
            QMessageBox.critical(self, "饱了没", "提交失败!\n请检查数据库连接!")

    def change_page(self, var):
        if self.sum_order == 0: return
        self.page += var
        self.show_items(self.page)

    def display_order(self, index):
        self.order_index = index
        self.sum_order = len(self.all_orders)
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
        length = 20
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

    def change_order(self, var):
        self.order_index += var
        self.display_order(self.order_index)

    def get_into_merchant(self, index):
        index = self.page*8+index
        self.merchant_info = self.result[index]
        self.sum_money = 0
        self.sum.setText("合计%5d元" % self.sum_money)
        self.merchant_logo.setPixmap(QPixmap(self.merchant_info[10]))
        sql = "select * from `product` where `master`='%s'" % self.result[index][0]
        self.cursor.execute(sql)
        product_info = self.cursor.fetchall()
        self.show_interface(self.DETAIL)
        items = QWidget()
        vLayout = QVBoxLayout(items)
        for item in product_info:
            vLayout.addWidget(self.create_product_item(item))
            self.buy_count[item[0]] = 0
        self.product_list.setWidget(items)
        self.update()


    def create_product_item(self, item):
        groupBox = QGroupBox(self)
        pic = QLabel(self)
        pic.setPixmap(QPixmap(item[3]))
        pic.setScaledContents(True)
        pic.resize(150, 150)
        pic.move(0, 0)

        name = QLabel(self)
        tmp = item[4]
        length = 20
        if(len(tmp)) > length: tmp = tmp[:length]
        while(len(tmp)) < length: tmp += " "
        name.setText(tmp)

        price = QLabel(self)
        price.setText("售价: " + str(float(item[1])) + "元")
        sales = QLabel(self)
        sales.setText("销量: " + str(item[2]))
        left = QLabel(self)
        left.setText("剩余: " + str(item[-1]))

        text_layout = QVBoxLayout()
        text_layout.addWidget(name)
        text_layout.addWidget(price)
        text_layout.addWidget(sales)
        text_layout.addWidget(left)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        add_button = QPushButton("+", self)
        add_button.setStyleSheet("background-color: rgb(51, 153, 255)")
        add_button.clicked.connect(lambda: self.change_number(item[0], 1, item[-1], float(item[1])))
        minus_button = QPushButton("-", self)
        minus_button.clicked.connect(lambda: self.change_number(item[0], -1, item[-1], float(item[1])))
        self.number[item[0]].setText(" "*5+"0")

        button_layout = QVBoxLayout()
        button_layout.addWidget(minus_button)
        button_layout.addWidget(self.number[item[0]])
        button_layout.addWidget(add_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(pic)
        main_layout.addWidget(text_widget)
        main_layout.addWidget(button_widget)
        groupBox.setLayout(main_layout)
        return groupBox

    def change_number(self, id, var, left, cost):
        if self.buy_count[id] == 0 and var == -1:
            return
        if self.buy_count[id] == left and var == 1:
            return
        self.buy_count[id] += var
        self.sum_money += var*cost
        self.sum.setText("合计%5d元" % self.sum_money)
        self.number[id].setText(" "*5+str(self.buy_count[id]))

    def portrait_file_dialog(self):
        file_name, file_type = QFileDialog.getOpenFileName(self,
                                                           "选取文件",
                                                           os.getcwd(),  # 起始路径
                                                           "图像文件 (*.bmp *.jpg *.jpeg *.png)")
        if file_name != "":
            sql = "update customer set `portrait` = '%s' where username = '%s'" % (file_name, self.info[0])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                self.personal_portrait.setPixmap(QPixmap(file_name))
                self.info[4] = file_name
            except:
                QMessageBox.critical(self, "饱了没", "上传失败!\n请检查数据库连接!")

    def become_vip_dialog(self):
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

        confirm = QPushButton("确认充值", self.dialog)
        confirm.move(25, 560)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(lambda: self.confirm_vip(input_password.text()))

        self.dialog.setWindowTitle("充值会员")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_vip(self, password):
        if password == "http://kuroko.info/areyourfull-diary/" \
                or password == "http://kuroko.info/areyourfull-diary" \
                or password == "kuroko.info/areyourfull-diary/" \
                or password == "kuroko.info/areyourfull-diary":
            sql = "update customer set `user_level` = 'VIP' where `username` = '%s'" % self.info[0]
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                self.info[1] = "VIP"
                self.update()
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "升级失败!\n请检查数据库连接!")
        else:
            QMessageBox.critical(self, "饱了没", "密码错误!\n请检查密钥内容!")

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
        if passwords[0] != self.info[-4]:
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
                self.info[-4] = passwords[1]
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

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
                    self.info[-1] = email
                    self.update()
                    self.dialog.close()
                except:
                    QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

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
                        self.info[-2] = phone
                        self.update()
                        self.dialog.close()
                    except:
                        QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")
            else:
                QMessageBox.critical(self, "饱了没", "电话格式错误!")

    def top_up_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 700)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        QR_code = QLabel(self.dialog)
        QR_code.setPixmap(QPixmap("./image/qrcode_github.png"))
        QR_code.setScaledContents(True)
        QR_code.resize(450, 450)
        QR_code.move(25, 25)

        input_password = QLineEdit(self.dialog)
        input_password.setFont(QFont("宋体", 12))
        input_password.resize(450, 50)
        input_password.setPlaceholderText("密钥:扫一扫输入网页链接")
        input_password.move(25, 490)
        input_password.setMaxLength(100)

        input_money = QLineEdit(self.dialog)
        input_money.setFont(QFont("宋体", 12))
        input_money.resize(450, 50)
        input_money.setPlaceholderText("输入充值金额(<1w)")
        input_money.move(25, 560)
        input_money.setMaxLength(100)

        confirm = QPushButton("确认充值", self.dialog)
        confirm.move(25, 630)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(lambda: self.confirm_top_up(input_password.text(), input_money.text()))

        self.dialog.setWindowTitle("钱包充值")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_top_up(self, password, money):
        if password == "https://github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project" \
                or password == "https://github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project/" \
                or password == "https://github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project" \
                or password == "github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project/":
            if money.isdigit():
                if int(money) < 10000:
                    sql = "update customer set `balance` = `balance`+%d where `username` = '%s'" % (int(money), self.info[0])
                    try:
                        self.cursor.execute(sql)
                        self.connect.commit()
                        self.info[2] += int(money)
                        self.update()
                        self.dialog.close()
                    except:
                        QMessageBox.critical(self, "饱了没", "充值失败!\n请检查数据库连接!")
                else:
                    QMessageBox.critical(self, "饱了没", "金额过大!\n请修改额度")
            else:
                QMessageBox.critical(self, "饱了没", "输入格式有误!")
        else:
            QMessageBox.critical(self, "饱了没", "密码错误!\n请检查密钥内容!")


    def use_points_dialog(self):
        self.dialog = QDialog()
        self.dialog.setFixedSize(500, 160)
        self.dialog.setWindowIcon(QIcon("./image/icon.jpg"))

        input_point = QLineEdit(self.dialog)
        input_point.setFont(QFont("宋体", 12))
        input_point.resize(450, 50)
        input_point.setPlaceholderText("1积分 = 1元, VIP = 2元")
        input_point.move(25, 20)
        input_point.setMaxLength(10)

        confirm = QPushButton("兑换积分", self.dialog)
        confirm.move(25, 90)
        confirm.resize(450, 50)
        confirm.setFont(QFont('幼圆', 12))
        confirm.setStyleSheet("background-color: rgb(51, 153, 255)")
        confirm.clicked.connect(
            lambda: self.confirm_use_points(input_point.text()))

        self.dialog.setWindowTitle("积分兑换")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def confirm_use_points(self, point):
        if len(point) == 0:
            QMessageBox.critical(self, "饱了没", "输入为空!")
        elif not point.isdigit():
            QMessageBox.critical(self, "饱了没", "输入有误!")
        elif int(point) > self.info[3]:
            QMessageBox.critical(self, "饱了没", "积分不足!")
        else:
            money = int(point)
            if self.info[1] == "VIP": money *= 2
            sql1 = "update customer set `balance` = `balance`+%d where `username` = '%s'" % (money, self.info[0])
            sql2 = "update customer set `points` = `points`-%d where `username` = '%s'" % (int(point), self.info[0])
            try:
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)
                self.connect.commit()
                self.info[2] += money
                self.info[3] -= int(point)
                self.update()
                self.dialog.close()
            except:
                QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")

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
        sql1 = "update customer set `longitude` = %d where `username` = '%s'" % (x, self.info[0])
        sql2 = "update customer set `latitude` = %d where `username` = '%s'" % (y, self.info[0])
        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.connect.commit()
            self.info[7] = x
            self.info[8] = y
            self.update()
            self.dialog.close()
        except:
            QMessageBox.critical(self, "饱了没", "修改失败!\n请检查数据库连接!")


    def cost_money_dialog(self):
        if self.info[2] < self.sum_money:
            QMessageBox.critical(self, "饱了没", "余额不足!")
        elif self.sum_money == 0:
            QMessageBox.critical(self, "饱了没", "尚未选择商品!")
        else:
            try:
                sql1 = "update `customer` set `balance` = `balance`-%f where `username` = '%s'" % (self.sum_money, self.info[0])
                sql2 = "update `customer` set `points` = `points`+%d where `username` = '%s'" % (self.sum_money//10, self.info[0])
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)
                sql3 = "select get_biggest_order_id()"
                self.cursor.execute(sql3)
                new_id = self.cursor.fetchone()[0]
                sql4 = "insert into `order` (`order_id`,`order_time`,`state`,`customer_name`,`merchant_name`)values ('%d','%s',0,'%s','%s')" % \
                       (new_id, util.get_time(), self.info[0], self.merchant_info[0])
                self.cursor.execute(sql4)
                for e in self.buy_count:
                    if self.buy_count[e] != 0:
                        sql = "insert into `sell` (`order_id`, `product_id`, `count`) values('%d','%d','%d')" % (new_id, e, self.buy_count[e])
                        self.cursor.execute(sql)
                self.connect.commit()
                s = "支付成功!\n本次消费%.1f元\n获得积分%d\n钱包余额%.1f元" % (self.sum_money, int(self.sum_money//10), float(self.info[2])-self.sum_money)
                QMessageBox.about(self, "饱了没", s)
                self.info[2] = float(self.info[2])+self.sum_money
                self.info[3] += int(self.sum_money//10)
                self.show_interface(self.MAIN)
            except:
                self.connect.rollback()
                QMessageBox.critical(self, "饱了没", "支付失败!\n请检查数据库连接!")

    def quit_to_login(self):
        self.to_login.emit()

    def mousePressEvent(self, event):
        sx = event.x()
        sy = event.y()
        if self.INDEX == self.BROWSE:
            for i in range(self.current_cnt):
                if i < 4:
                    x = 10
                    y = 280 + i * 260
                else:
                    x = 460
                    y = 280 + (i - 4) * 260
                if x + 440 > sx > x and y + 220 > sy > y:
                    self.get_into_merchant(i)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.INDEX == self.ORDER:
            self.paint_order(event, qp)
        elif self.INDEX == self.PERSONAL:
            self.paint_personal(event, qp)
        elif self.INDEX == self.DETAIL:
            self.paint_detail(event, qp)
        qp.end()


    def paint_personal(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("宋体", 12))
        qp.drawText(350, 250, "ID:" + self.info[0])
        if self.info[1] == "common":
            qp.drawText(350, 340, "等级:普通会员")
        else:
            qp.drawText(350, 340, "等级:VIP会员")
        qp.drawText(350, 435, "注册:" + self.info[6].strftime('%Y-%m-%d'))
        qp.drawText(70, 540, "邮箱: " + self.info[12])
        qp.drawText(70, 645, "电话: " + self.info[11])
        qp.drawText(70, 750, "余额: " + str(float(self.info[2])) + "元")
        qp.drawText(70, 855, "积分: " + str(int(self.info[3])))
        qp.drawText(70, 960, "下单次数: " + str(int(self.info[5])))
        qp.drawText(70, 1065, "地址: (%d, %d)" % (int(self.info[7]), int(self.info[8])))

    @staticmethod
    def transform_time(t):
        if t is None: return "00:00"
        t = str(t)
        while t[-1] != ":":
            t = t[:-1]
        t = t[:-1]
        return t

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


    def paint_detail(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont("宋体", 22))
        qp.drawText(220, 70, self.merchant_info[5])
        qp.setFont(QFont("宋体", 10))
        if self.merchant_info[12] == 0: score = 0
        else: score = self.merchant_info[4]/self.merchant_info[12]
        qp.drawText(220, 110, "评分: %1.f分" % score)
        qp.setFont(QFont("宋体", 12))
        qp.drawText(220, 160, "总订单:%d" % self.merchant_info[3])
        qp.drawText(220, 210, "成立于:%s" % self.merchant_info[1].strftime('%Y-%m-%d'))
        qp.drawText(520, 40, "营业时间%s-%s" % (self.transform_time(self.merchant_info[8]), self.transform_time(self.merchant_info[9])))
        if self.merchant_info[11] is None: content = "暂无"
        else: content = self.merchant_info[11]
        d = {"cate": "美食", "supermarket": "超市", "drug": "药店", "fruit": "果蔬"}
        qp.drawText(520, 100, "门店类型:" + d[self.merchant_info[2]])
        qp.drawText(520, 150, "简介:"+content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Customer("customer")
    win.show()
    sys.exit(app.exec_())
    pass
