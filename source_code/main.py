from PyQt5.QtWidgets import *
import sys
import login
import customer
import rider
import merchant


class Main:
    def __init__(self):
        self.login = login.Login()
        self.customer = None
        self.rider = None
        self.merchant = None
        self.login.to_customer.connect(self.login_as_customer)
        self.login.to_rider.connect(self.login_as_rider)
        self.login.to_merchant.connect(self.login_as_merchant)

    def start(self):
        self.login.show()
        self.login.username.setText("")
        self.login.password.setText("")
        self.login.verification_code.setText("")
        self.login.change_code()
        if self.customer is not None: self.customer.close()
        if self.rider is not None: self.rider.close()
        if self.merchant is not None: self.merchant.close()

    def login_as_customer(self):
        self.customer = customer.Customer(self.login.username.text())
        self.customer.to_login.connect(self.start)
        self.login.close()
        self.customer.show()

    def login_as_rider(self):
        self.rider = rider.Rider(self.login.username.text())
        self.rider.to_login.connect(self.start)
        self.login.close()
        self.rider.show()

    def login_as_merchant(self):
        self.merchant = merchant.Merchant(self.login.username.text())
        self.merchant.to_login.connect(self.start)
        self.login.close()
        self.merchant.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.start()
    sys.exit(app.exec_())
