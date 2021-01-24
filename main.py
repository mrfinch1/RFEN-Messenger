import sqlite3
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import socket
import threading
import cv2
import cv2 as cv
import struct
import imutils
import pickle
import os
from pyfiglet import Figlet
dosya = b""
def print_cool(text):
    cool_text = Figlet(font="slant")
    os.system('mode con : cols = 75 lines = 30')
    return str(cool_text.renderText(text))
connection = sqlite3.connect("new.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL UNIQUE,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL)")
connection.commit()
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
query=input('Welcome\nEnter "Giriş için Log in Üye olmak için Register. ')
if query=="Register":
    while True:
        name=input("Kullanıcı adı. ")
        n=cursor.execute('SELECT name FROM login').fetchone()
        n=str(n).strip("('',)'")
        if n==name:
            print('Bu kullanıcı adı zaten alınmış başka bir kullanıcı adı bulun ')
            continue
        else:
            while True:
                email=input("Email. ")
                m=cursor.execute('SELECT email FROM login').fetchone()
                m=str(m).strip("('',)'")
                if m == email:
                    print('Bu email zaten var')
                    continue
                else:
                    while True:
                        a = random.randint(1000,9999)
                        mail = smtplib.SMTP("smtp.gmail.com",587)
                        mail.ehlo()
                        mail.starttls()
                        mail.login("gmail adresi", "şifre")
                        mesaj = MIMEMultipart()
                        mesaj["From"] = "gmail adresiniz"
                        mesaj["Subject"] = "Onay Kodu"
                        mesaj["To"] = email
                        body = """{}"""
                        body_text = MIMEText(body, "plain")
                        mesaj.attach(body_text)
                        mail.sendmail(mesaj["From"], mesaj["To"], str(a))
                        print("Onay kodu Gönderildi")
                        aa = int(input(":"))
                        if aa == a:
                            print("Başarılı")
                        else:
                            print("Başarısız")
                        password=input("Şifre. ")
                        rpassword=input("Şifre tekrar. ")
                        if password ==rpassword:
                            cursor.execute('INSERT INTO login VALUES(?,?,?,?)',
                                           (None, name, email, password)) 
                            connection.commit()
                            print('Olustu.')
                            sys.exit()

                        else:
                            print('Sifre uyumsuz')
                            continue

elif query=="Log in":
    while True:
        name = input("Kullanıcı adı")
        password=input("Şifre")
        n=cursor.execute("SELECT name from login WHERE name='"+name+"'").fetchone()
        n = str(n).strip("('',)'")
        if n==name:
            pw = cursor.execute("SELECT password from login WHERE password='" + password + "'").fetchone()
            pw = str(pw).strip("('',)'")
            if pw==password:
                print('Hoşgeldiniz.',name)
                break
            else:
                print("Yanlış kullanıcı adı")
                continue
        else:
            print("Yanlış şifre")
            continue
    else:
        print('Tekrar dene. ')
    connection.close()
print(print_cool(name))
h = '127.0.0.1'
print("@",name)
menu = """
         ####################################################
         #1-Odaya bağlan
         #2-P2P odaya bağlan
         #3-P2P oda oluştur(Sunucu Taraflı)
         #4-Oda oluştur(Sunucu Taraflı)
         #5-Dosya gönder(Sunucu Taraflı)
         #6-Dosya Al
         #7-Video odası oluştur(Sunucu Taraflı)
         #8-Video odasına bağlan
         #Not : Bütün seçeneklerde IP adresini kontrol ediniz
         ####################################################
 """
print(menu)
secim = int(input(""))
if secim == 1 :
    nickname = input("Choose your Nicknames")
    room_token = int(input("PORT"))
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('127.0.0.1',room_token))
    def recevie():
        while 1:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An error occured")
                client.close()
                break
    def write():
        while 1:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))
    receive_thread = threading.Thread(target=recevie)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
elif secim == 2 :
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_id = int(input("PORT"))
    s.connect(('127.0.0.1',user_id))
    while 1:
        print (s.recv(1024))
        message = input("mesajınız")
        try:
            s.send(message.encode('ascii'))
            print("İletildi")
        except socket.error:
            print("HATA")
elif secim == 3:
    h = '127.0.0.1'
    p = random.randint(1000,5555)
    print("PORT:",p)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((h,p))
    s.listen()
    def baglanti():
        while 1:
            c,addr = s.accept()
            print(f' Baglanti kuruldu {addr}')
            while 1:
                message = input("mesajınız")
                c.send(message.encode('ascii'))
                print("İletildi")
                data = c.recv(1024)
                print("Client :",data)
    baglanti()
elif secim == 4:
    def create_room():
        room_token1 = random.randint(1000,5555)
        print("PORT:",room_token1)
        host = '127.0.0.1'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,room_token1))
        server.listen()
        clients = []
        nicknames=[]
        def broadcast(message):
            for client in clients:
                client.send(message)
        def handle(client):
            while 1:
                try:
                    message = client.recv(1024)
                    broadcast(message)
                except:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    broadcast(f'{nickname} left the chat '.encode('ascii'))
                    nickname = nicknames[index]
                    nicknames.remove(nickname)
                    break
        def recevie():
            while 1:
                client , address = server.accept()
                print(f'Connected with {str(address)}')
                client.send('s'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                nicknames.append(nickname)
                clients.append(client)
                print(f'Nickname of the client is {nickname}')
                broadcast(f'{nickname} joined the chat'.encode('ascii'))
                client.send('Connected to the server'.encode('ascii'))
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
        recevie()

    create_room()
elif secim == 5:
    one_connection_only = (True)
    filename = input("dosya adı ve uzantısı")
    port = random.randint(1000,5555)
    print("TOKEN:",port)
    sock = socket.socket()
    sock.bind((h,port))
    sock.listen(10)
    print("Başladı")
    while 1:
        conn , addr = sock.accept()
        print(f"----->{addr}")
        data = conn.recv(1024)
        print(f"alındı{data}")
        with open (filename,"rb") as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                print(f"sent{data!r}")
                data = file.read(1024)
            print("tamamlandı.")
            conn.close()
            if(one_connection_only):
                break

    sock.close()
elif secim == 6:
    sock = socket.socket()
    port = int(input("port"))
    sock.connect(('127.0.0.1',port))
    sock.send(b"1")
    a = input("dosya size gönderlilicek adını uzantıyla beraber girin")
    with open(a,"wb") as file :
        print("Dosya Açıldı")
        print("receiving data...")
        while 1:
            data = sock.recv(1024)
            print(f"data={data}")
            if not data:
                break
            file.write(data)
    print("Gönderildi")
    sock.close()
elif secim == 7:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    h = '127.0.0.1'
    p = random.randint(1000,5555)
    print("port:",p)
    s.bind((h,p))
    s.listen(5)
    while 1:
        c,addr = s.accept()
        print('Bağlantı',addr)
        if c:
            print("1-Video yayını yap")
            print("2-Kameradan yayın yap")
            option = int(input(":"))
            if option == 1:
                video = input("Video adını girin")
                screen = cv.VideoCapture(video)
                while(screen.isOpened()):
                    img,frame = screen.read()
                    frame = imutils.resize(frame,width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q",len(a))+a
                    c.sendall(message)
                    cv.imshow('.',frame)
                    key = cv.waitKey(1) & 0xFF
                    if key ==ord('q'):
                        c.close()
            elif option == 2:
                screen = cv.VideoCapture(0)
                while(screen.isOpened()):
                    img,frame = screen.read()
                    frame = imutils.resize(frame,width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q",len(a))+a
                    c.sendall(message)
                    cv.imshow('.',frame)
                    key = cv.waitKey(1) & 0xFF
                    if key ==ord('q'):
                        c.close()
            else:
                print("Hata")
elif secim == 8:
    p = int(input("port"))
    c.connect((h,p))
    yukleme_boyutu = struct.calcsize("Q")
    while 1:
        while len(dosya) < yukleme_boyutu:
            paket = c.recv(4*1024)
            if not paket: 
                break
            dosya+=paket
        paket_msg_size = dosya[:yukleme_boyutu]
        dosya = dosya[yukleme_boyutu:]
        msg_size = struct.unpack("Q",paket_msg_size)[0]

        while len(dosya) < msg_size:
            dosya += c.recv(4*1024)
        frame_data = dosya[:msg_size]
        dosya  = dosya[msg_size:]
        frame = pickle.loads(frame_data)
        cv.imshow(":",frame)
        key = cv.waitKey(1) & 0xFF
        if key  == ord('a'):
            break
    c.close()
else:
    print("Geçersiz giriş")
#---Yaralanılan Kaynaklar--- #
#https://www.neuralnine.com #
#https://github.com/E-Renshaw/ftp-socket-server-python#
#https://github.com/sachinyadav3496/VideoChatApp/blob/master/server.py#

