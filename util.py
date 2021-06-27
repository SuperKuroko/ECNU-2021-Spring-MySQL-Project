import time
from pymysql import *


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def sql_connect():
    my_connect = Connect(
        host="124.71.228.59",
        port=3306,
        user="DB_USER066",
        passwd="DB_USER066@123",
        db="user066db",
        charset="utf8"
    )
    return my_connect
