from tkinter import *
from PIL import Image, ImageTk, ImageDraw  # pip install Pillow
from datetime import *
import time
from math import *
import mysql.connector  
from tkinter import messagebox
import os

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        # Creating left and right background colors
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # Creating login frame
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=100, width=800, height=500)

        title = Label(login_frame, text="LOGIN HERE", font=("times new roman", 30, "bold"), bg="white", fg="#08A3D2").place(x=250, y=35)

        email = Label(login_frame, text="EMAIL ADDRESS", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=150)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=250, y=180, width=350, height=35)

        pass_ = Label(login_frame, text="PASSWORD", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=250)
        self.txt_pass_ = Entry(login_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass_.place(x=250, y=280, width=350, height=35)

        btn_reg = Button(login_frame, command=self.register_window, text="Register New Account?", font=("times new roman", 14, "bold"), bg="white", bd=0, fg="#B00857").place(x=245, y=320)
        btn_login = Button(login_frame, command=self.login, text="Login", font=("times new roman", 18, "bold"), fg="white", bg="#B00857").place(x=245, y=370, width=180, height=40)

        # Creating clock label
        self.lbl = Label(self.root, text="\nC.L.O.C.K", font=("Book Antiqua", 25, "bold"), fg="white", compound=BOTTOM, bg="#081923", bd=0)
        self.lbl.place(x=90, y=120, height=450, width=350)
        self.working()

    def register_window(self):
        self.root.destroy()
        os.system("python register.py")

    def login(self):
        if self.txt_email.get() == "" or self.txt_pass_.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                # ✅ Connecting to MySQL database
                con = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="77492652Rt@",  
                    database="student_management"     
                )
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=%s AND password=%s", (
                    self.txt_email.get(),
                    self.txt_pass_.get()
                ))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid USERNAME & PASSWORD", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome: {self.txt_email.get()}", parent=self.root)
                    self.root.destroy()
                    os.system("python dashboard.py")
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Database Error: {str(es)}", parent=self.root)

    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)
        bg = Image.open("images/c.png")
        bg = bg.resize((300, 300), Image.LANCZOS)
        clock.paste(bg, (50, 50))

        # Draw hands
        origin = 200, 200
        draw.line((origin, 200 + 50 * sin(radians(hr)), 200 - 50 * cos(radians(hr))), fill="#DF005E", width=4)
        draw.line((origin, 200 + 80 * sin(radians(min_)), 200 - 80 * cos(radians(min_))), fill="white", width=3)
        draw.line((origin, 200 + 100 * sin(radians(sec_)), 200 - 100 * cos(radians(sec_))), fill="yellow", width=4)
        draw.ellipse((195, 195, 210, 210), fill="#1AD5D5")

        clock.save("images/clock_new.png")

    def working(self):
        t = datetime.now().time()
        hr = (t.hour % 12) / 12 * 360
        min_ = t.minute / 60 * 360
        sec_ = t.second / 60 * 360

        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="images/clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(1000, self.working)


root = Tk()
obj = Login_window(root)
root.mainloop()

