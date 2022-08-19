from random import Random
from user.models import EmailVerifyRecord
from django.core.mail import send_mail
from login_system.settings import EMAIL_FROM


def random_str(randomlength=20):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email):
    
    code = random_str(40)
    email_record = EmailVerifyRecord.objects.create(email=email, code=code)
    email_record.save()
    email_title = '**网注册激活链接'
    email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/user/active/{0}'.format(code)
    send_mail(email_title, email_body, EMAIL_FROM, [email])
