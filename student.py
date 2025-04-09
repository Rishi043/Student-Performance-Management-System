from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class studentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Management System")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==== Variables ====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_admission = StringVar()
        self.var_course = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()

        self.course_list = []
        self.fetch_course()

        # ==== Title ====
        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20), bg="#033054", fg="white").place(x=10, y=15, width=1080)

        # ==== Content ====
        lbl_roll = Label(self.root, text="Roll No", font=("goudy old style", 15), bg="white").place(x=10, y=60)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=10, y=100)
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=10, y=140)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=10, y=180)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=10, y=220)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=10, y=260)
        lbl_admission = Label(self.root, text="Admission", font=("goudy old style", 15), bg="white").place(x=400, y=60)
        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15), bg="white").place(x=400, y=100)
        lbl_state = Label(self.root, text="State", font=("goudy old style", 15), bg="white").place(x=400, y=140)
        lbl_city = Label(self.root, text="City", font=("goudy old style", 15), bg="white").place(x=400, y=180)
        lbl_pin = Label(self.root, text="Pin", font=("goudy old style", 15), bg="white").place(x=400, y=220)
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=400, y=260)

        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15), bg="lightyellow")
        self.txt_roll.place(x=150, y=60)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=100)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=140)
        self.cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state='readonly', font=("goudy old style", 13))
        self.cmb_gender.place(x=150, y=180)
        self.cmb_gender.current(0)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=220)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=260)

        txt_admission = Entry(self.root, textvariable=self.var_admission, font=("goudy old style", 15), bg="lightyellow").place(x=550, y=60)
        self.cmb_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, state='readonly', font=("goudy old style", 13))
        self.cmb_course.place(x=550, y=100)
        self.cmb_course.set("Select")
        txt_state = Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15), bg="lightyellow").place(x=550, y=140)
        txt_city = Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15), bg="lightyellow").place(x=550, y=180)
        txt_pin = Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15), bg="lightyellow").place(x=550, y=220)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=550, y=260, width=300, height=60)

        # ==== Buttons ====
        btn_add = Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=850, y=60, width=200, height=30)
        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=850, y=100, width=200, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=850, y=140, width=200, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=850, y=180, width=200, height=30)

        # ==== Search Panel ====
        self.var_search = StringVar()
        lbl_search_roll = Label(self.root, text="Roll No", font=("goudy old style", 15), bg="white").place(x=280, y=330)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg="lightyellow").place(x=370, y=330, width=180)
        btn_search = Button(self.root, text="Search", command=self.search, font=("goudy old style", 15), bg="#03a9f4", fg="white").place(x=560, y=330, width=100, height=30)

        # ==== Treeview ====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=0, y=370, relwidth=1, height=130)

        scroll_x = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.C_Frame, orient=VERTICAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CourseTable.xview)
        scroll_y.config(command=self.CourseTable.yview)

        for col in self.CourseTable["columns"]:
            self.CourseTable.heading(col, text=col.capitalize())
            self.CourseTable.column(col, width=100)

        self.CourseTable["show"] = "headings"
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def fetch_course(self):
        self.course_list.clear()
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="77492652Rt@",
                database="student_management"
            )
            cur = con.cursor()
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def add(self):
        con = mysql.connector.connect(host="localhost", user="root", password="77492652Rt@", database="student_management")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=%s", (self.var_roll.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Roll No already assigned, try different", parent=self.root)
            else:
                cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_contact.get(),
                    self.var_admission.get(),
                    self.var_course.get(),
                    self.var_state.get(),
                    self.var_city.get(),
                    self.var_pin.get(),
                    self.txt_address.get("1.0", END).strip()
                ))
                con.commit()
                messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def show(self):
        con = mysql.connector.connect(host="localhost", user="root", password="77492652Rt@", database="student_management")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.CourseTable.focus()
        content = self.CourseTable.item(f)
        row = content['values']
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_admission.set(row[6])
        self.var_course.set(row[7])
        self.var_state.set(row[8])
        self.var_city.set(row[9])
        self.var_pin.set(row[10])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[11])

    def update(self):
        con = mysql.connector.connect(host="localhost", user="root", password="77492652Rt@", database="student_management")
        cur = con.cursor()
        try:
            cur.execute("UPDATE student SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, admission=%s, course=%s, state=%s, city=%s, pin=%s, address=%s WHERE roll=%s", (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_admission.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0", END).strip(),
                self.var_roll.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete(self):
        con = mysql.connector.connect(host="localhost", user="root", password="77492652Rt@", database="student_management")
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM student WHERE roll=%s", (self.var_roll.get(),))
            con.commit()
            messagebox.showinfo("Success", "Record Deleted Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("Select")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")
        self.show()

    def search(self):
        con = mysql.connector.connect(host="localhost", user="root", password="77492652Rt@", database="student_management")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student WHERE roll=%s", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.CourseTable.delete(*self.CourseTable.get_children())
                self.CourseTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


