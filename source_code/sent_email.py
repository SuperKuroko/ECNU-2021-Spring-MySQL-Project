import re
import smtplib
import random
from email.mime.text import MIMEText


def email_type(email):
    test_type = re.compile("^[a-zA-Z0-9_-]+@test+(\.[a-zA-Z0-9_-]+)+$")
    right_type = re.compile("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$")
    if test_type.match(email):
        return 0
    elif right_type.match(email):
        return 1
    return -1


def sent_email(receiver):
    mail_host = ""       #such as stmp.qq.com
    mail_user = ""  #such as xxx@xxx.com
    mail_pass = ""  #not your account password!
    sender = ""
    title = "饱了没-邮箱验证码"
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))
    content = "【饱了没】验证码：%s，请在 5 分钟内完成操作。如非本人操作，请忽略。" % code
    message = MIMEText(content, "plain", "utf-8")
    message["From"] = "{}".format(sender)
    message["To"] = ",".join(receiver)
    message["Subject"] = title
    try:
        smtp_object = smtplib.SMTP_SSL(mail_host, 465)
        smtp_object.login(mail_user, mail_pass)
        smtp_object.sendmail(sender, receiver, message.as_string())
        return code
    except smtplib.SMTPException as error:
        return str(error)


if __name__ == "__main__":
    pass
    #print(email_type("123456@test.com"))
