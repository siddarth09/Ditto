import time
import random
import cv2
import pandas as pd
import os
import numpy as np
import pyqrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pyqrcode as qr
import png
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import re

import pyrebase


class App():

    def __init__(self,master):

        self.master=master
        self.name = 'deliveryditto@gmail.com'
        self.password = 'gkbltrhhngtfsxrm'
        self.image = cv2.imread('3.png')
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        self.disp = ttk.Label(master, image=self.image)
        self.disp.pack()
        self.parentframe=Frame(master,relief=RAISED,height=150,width=300,bg='black')
        self.parentframe.place(relx=0.50,rely=0.80,anchor=CENTER)
        #variables for Email
        global username
        global password
        global prod
        username = StringVar()
        password = StringVar()
        prod=StringVar()
        self.emaillabel = Label(self.parentframe, text='EMAIL ID:', font=("Times", "10", "bold"),foreground='white',background='black')
        self.emaillabel.place(relx=0.16, rely=0.40, anchor=CENTER)
        self.passwordLabel = Label(self.parentframe, text='PASSWORD:', font=("Times", "10", "bold"),foreground='white',background='black')
        self.passwordLabel.place(relx=0.16, rely=0.65, anchor=CENTER)

        self.email_idEntry = Entry(self.parentframe, textvariable=username)
        self.email_idEntry.place(relx=0.60, rely=0.40, anchor=CENTER)
        self.passwordEntry = Entry(self.parentframe, textvariable=password, show='*')
        self.passwordEntry.place(relx=0.60, rely=0.65, anchor=CENTER)

        self.submitButton = Button(self.parentframe, text='SUBMIT', command=self.loginform, font=("Times", "12", "bold"))
        self.submitButton.place(relx=0.50, rely=0.85, anchor=CENTER)

        #AFTER LOGIN PAGE
        self.img = cv2.imread('college.jpg')
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(self.img)
        self.college_location = ttk.Label(master, image=self.img)

        global location
        location= StringVar()
        self.destination = Label(self.master, text="DESTINATION", font=("Times", "15", "bold"),foreground='white',background='black')
        self.get_location=Entry(self.master, textvariable=location)
        self.description=Label(self.master,text="ENTER DESTINATION", font=("Times", "24", "bold"),foreground='white',background='black')
        self.nextbutton=Button(self.master, text="DELIVER", command=self.qrcode_gen, font=("Times", "15", "bold"))
        
        # for otp storing
        
    def loginform(self):
        """
        gets user's email address for sending email
        """
        global email
        email = username.get()
        Password = password.get()
        print(email)

        # print(mail)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            messagebox.showinfo(title='EMAIL VERIFICATION', message='WELCOME TO DITTO')
            self.disp.pack_forget()
            self.parentframe.place_forget()
            self.master.geometry("800x500")
            self.college_location.pack()  
            self.location()          
        else:
            messagebox.showinfo(title='EMAIL VERIFICATION', message='INVALID PLEASE TRY AGAIN')

    def qrcode_gen(self):
        """generates QR Codes for locking system to open
            and also send the location information
        """
        otp=random.randint(1000,9999)
        destiny=location.get()
        final_info={"OTP":otp,
                    "destination":destiny}
        qr=pyqrcode.create(otp,version=10)
        qr.png('otp.png',scale=5)
       
        print(destiny)
        print(otp)
        message="DITTO WLL BE ARRIVING AT {}".format(destiny)
        messagebox.showinfo(title='PACKAGE GETTING DELIVERED', message=message)
        self.mail(to_email=email)
        messagebox.showinfo(title='ALERT', message="QR CODE IS SENT TO YOUR MAIL PLEASE SCAN INFRONT OF CAMERA")
        
    
    def location(self):
        message="Currently supports SET BLOCK TO MUNCHIES"
        messagebox.showinfo(title='support', message=message)
        self.description.place(relx=0.50,rely=0.10,anchor=CENTER)
        self.destination.place(relx=0.16,rely=0.85,anchor=CENTER)
        self.get_location.place(relx=0.16, rely=0.90, anchor=CENTER)
        
        self.nextbutton.place(relx=0.90, rely=0.90, anchor=CENTER)

    def mail(self,html=None,amount=None,subject='YOUR BILL',
             from_mail='ditto delivery<deliveryditto@gmail.com>',
             to_email=None):
        # assert isinstance(to_email, list)
        # Html,Total=get_bill()
        
        msg = MIMEMultipart('alternative')
        msg['From'] = from_mail
        msg['To'] = to_email
        msg['Subject'] = subject
        html_file = "email.html"

        with open(html_file, 'r') as f:
            html_attachment = MIMEText(f.read(), 'html')
            msg.attach(html_attachment)

        qr_code_file='otp.png'

        with open(qr_code_file, 'rb') as f:
            qr_code_attachment = MIMEBase('application', 'octet-stream')
            qr_code_attachment.set_payload((f).read())
            encoders.encode_base64(qr_code_attachment)
            qr_code_attachment.add_header('Content-Disposition', "attachment; filename= %s" % qr_code_file)
            msg.attach(qr_code_attachment)

        
        

        msg_str = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.name,self.password)
        server.sendmail(from_mail, to_email, msg_str)
        print("QR CODE SENT")
        server.quit()



def main():
    root=Tk()
    root.title("DITTO: Enhanced Delivery")
    root.geometry("600x500")


    obj=App(root)
    root.mainloop()

if __name__=="__main__":
    main()

    



