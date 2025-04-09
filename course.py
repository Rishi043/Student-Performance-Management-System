from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # MySQL connection parameters
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "77492652Rt@",  # Update if password is set
            "database": "student_management"
        }

        # Title
        title = Label(self.root, text="Manage Course Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # Widgets
        Label(self.root, text="Course Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        Label(self.root, text="Duration", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        Label(self.root, text="Charges", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        Label(self.root, text="Description", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)

        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_courseName.place(x=150, y=60, width=200)
        Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=150, y=100, width=200)
        Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=150, y=140, width=200)
        self.txt_description = Text(self.root, font=("goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # Buttons
        Button(self.root, text='Save', command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=400, width=110, height=40)
        Button(self.root, text='Update', command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2").place(x=270, y=400, width=110, height=40)
        Button(self.root, text='Delete', command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2").place(x=390, y=400, width=110, height=40)
        Button(self.root, text='Clear', command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2").place(x=510, y=400, width=110, height=40)

        # Search Panel
        Label(self.root, text="Course Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=870, y=60, width=180)
        Button(self.root, text='Search', command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=1070, y=60, width=120, height=28)

        # Table Frame
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = 'headings'
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #__________Functions__________

    def connect_db(self):
        return mysql.connector.connect(**self.db_config)

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)

    def get_data(self, ev):
        self.txt_courseName.config(state='readonly')
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[4])

    def add(self):
        con = self.connect_db()
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=%s", (self.var_course.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Course Name already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (%s, %s, %s, %s)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()
            self.show()

    def update(self):
        con = self.connect_db()
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=%s", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select Course from list", parent=self.root)
                else:
                    cur.execute("UPDATE course SET duration=%s, charges=%s, description=%s WHERE name=%s", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()
            self.show()

    def delete(self):
        con = self.connect_db()
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=%s", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please select course from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM course WHERE name=%s", (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Course deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE %s", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = self.connect_db()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()
            
            
