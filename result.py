from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

# Creating class with name resultClass to manage student results
class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        #___title____
        title = Label(self.root, text="Add Student Results", font=("goudy old style", 20, "bold"),
                      bg="orange", fg="#262626").place(x=10, y=20, width=1180, height=50)

        #___variables____
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        # WIDGETS
        lbl_select = Label(self.root, text="Select Student", font=("goudy old style", 20, 'bold'), bg='white').place(x=50, y=100)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 20, 'bold'), bg='white').place(x=50, y=160)
        lbl_course = Label(self.root, text="Course", font=("goudy old style", 20, 'bold'), bg='white').place(x=50, y=220)
        lbl_marks_ob = Label(self.root, text="Marks Obtained", font=("goudy old style", 20, 'bold'), bg='white').place(x=50, y=280)
        lbl_full_marks = Label(self.root, text="Full Marks", font=("goudy old style", 20, 'bold'), bg='white').place(x=50, y=340)

        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list,
                                        font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_student.place(x=280, y=105, width=200)
        self.txt_student.set("Select")

        btn_search = Button(self.root, text='Search', font=("goudy old style", 15, "bold"),
                            bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=500, y=105, width=100, height=28)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20, 'bold'),
                         bg='lightyellow', state='readonly').place(x=280, y=160, width=320)
        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 20, 'bold'),
                           bg='lightyellow', state='readonly').place(x=280, y=220, width=320)
        txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 20, 'bold'),
                          bg='lightyellow').place(x=280, y=280, width=320)
        txt_full_marks = Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 20, 'bold'),
                               bg='lightyellow').place(x=280, y=340, width=320)

        # Buttons
        btn_add = Button(self.root, text='Submit', font=("times new roman", 15), bg="lightgreen",
                         activebackground="lightgreen", cursor="hand2", command=self.add).place(x=300, y=420, width=120, height=35)
        btn_clear = Button(self.root, text='Clear', font=("times new roman", 15), bg="lightgray",
                           activebackground="lightgray", cursor="hand2", command=self.clear).place(x=440, y=420, width=120, height=35)

        # Image
        self.bg_img = Image.open("images/result.jpg")
        self.bg_img = self.bg_img.resize((500, 300), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg = Label(self.root, image=self.bg_img).place(x=650, y=105)

    # Function to connect to MySQL
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="77492652Rt@",  # Use your MySQL root password if any
            database="student_management"
        )

    # Function to fetch student rolls
    def fetch_roll(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list.clear()
            if len(rows) > 0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # Function to search student data
    def search(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll=%s", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # Function to add result
    def add(self):
        try:
            con = self.connect_db()
            cur = con.cursor()
            if self.var_name.get() == "":
                messagebox.showerror("Error", "First Search Student Record", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=%s AND course=%s", (
                    self.var_roll.get(), self.var_course.get()))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Result already present", parent=self.root)
                else:
                    per = (int(self.var_marks.get()) * 100) / int(self.var_full_marks.get())
                    cur.execute("INSERT INTO result (roll, name, course, marks_obtained, full_marks, per) VALUES (%s,%s,%s,%s,%s,%s)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(),
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # Function to clear form fields
    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")

# Run the app
if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()





