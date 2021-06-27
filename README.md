# ECNU-2021-Spring-MySQL-Project
ECNU 2021春季《数据库系统实践》课程期末项目作品

参考"饿了么"APP外卖软件制作的一个简易客户端"饱了没"

+ 操作系统: **Win10** 
+ 前端环境
  + 开发语言： **Python3.9**
  + 开发工具： **PyQT5**
  + 需**pip**的包：**PyQT5, py-emails, pymysql** 
+ 后端环境: **MySQL**
+ 后端简介与效果预览请参见:[introduction](https://github.com/SuperKuroko/ECNU-2021-Spring-MySQL-Project/blob/main/introduction/introduction.pdf)
+ [开发者日志](http://kuroko.info/areyourfull-diary/)


程序运行方法:
+ 首先确保**Python**环境下安装好了**PyQT5, py-emails, pymysql**包
+ 创建一个空数据库，运行根目录下的**data.sql**文件导入数据
+ 在**util.py**的**sql_connect**函数中修改数据库接口
+ 在**sent_email.py**的**sent_email**函数中填写**smtp**服务的账户和口令
  + 如果不需要邮箱验证码功能，请在注册账户时以@**test.xxx**的域名进行注册，系统将会对任意输入通过验证
  + 填写的方式在**sent_email**函数中有说明
+ 在根目录下以**python main.py**的方式运行程序




文件简介:
+ **image,product,cover**文件夹存储了系统需要的图片
+ **verification**文件夹为验证码图片库
+ **venv, .idea**为**Pycharm**工程文件
+ **customer.py**为顾客版本的端界面
+ **merchant.py**为商家版本的端界面
+ **rider.py**为骑手版本的端界面
+ **login.py**为登录和注册的端界面
+ **util.py**定义了数据库连接接口以及其他小工具
+ **verification_code.py**定义了随机验证码函数
+ **sent_email.py**定义了邮箱验证码发送服务和邮箱格式的正则表达式匹配
+ **main.py**为程序入口
+ **data.sql**为后端表和数据文件



需要注意的事项有:
+ 因为学校要求用华为云存储后端文件，而账户没有图片数据存储的权限，因此系统中的文件均以路径名的方式进行存储，不支持跨机器浏览
+ 请设置数据库事务等级为"不可重复读"
+ 当前尚无**release**版本，后续版本更新也许会上传


[更新日志](http://kuroko.info/areyourfull-diary/)
+ **2021-6-20 1.0**版本发布
+ **2021-6-27 1.1**版本更新
  + 修改了数据库接口方式，将之前的7个接口改接到**util.py**中，现在仅需修改**util.py**的**sql_connect**函数即可更改数据库接口
  + 修复了部分图片大小不兼容的bug
