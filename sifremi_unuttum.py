import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import random
import sqlite3
import os
from pyfiglet import Figlet
def print_cool(text):
    cool_text = Figlet(font="slant")
    os.system('mode con : cols = 75 lines = 30')
    return str(cool_text.renderText(text))
print(print_cool("Sifremi Unuttum"))
connection = sqlite3.connect("new.db")
cursor = connection.cursor()
a = random.randint(1000,9999)
def sifre_update(new_password,email):
    cursor.execute(''' UPDATE login SET password =  ? WHERE email = ? ''',(new_password,email))
    connection.commit()
try:
    mail = smtplib.SMTP("smtp.gmail.com",587)
    mail.ehlo()
    mail.starttls()
    mail.login("mail adresiniz", "şifre")

    mesaj = MIMEMultipart()
    mesaj["From"] = "mail adresiniz"
    mesaj["Subject"] = "Onay Kodu"
    mesaj["To"] = input("Mailinizi giriniz")
    body = """{}"""


    body_text = MIMEText(body, "plain")
    mesaj.attach(body_text)

    mail.sendmail(mesaj["From"], mesaj["To"], str(a))
    print("Mail başarılı bir şekilde gönderildi.")
    mail.close()


except:
    print("Hata:", sys.exc_info()[0])
aa = int(input("Gelen kodu giriniz"))
if aa == a:
    password = input("Yeni Şifre")
    rpassword = input("Yeni Şifreyi onayla")
    if password == rpassword:
        sifre_update(rpassword,mesaj["TO"])
        print("Şifre değiştirme başarılı")
else:
    print("Şifre değiştirme başarısız")
