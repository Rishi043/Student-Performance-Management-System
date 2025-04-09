from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import mysql.connector

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=35)

        # Search
        self.var_search = StringVar()
        self.var_id = ""
        lbl_search = Label(self.root, text="Search By Roll No.", font=("goudy old style", 20, "bold"), bg="white").place(x=280, y=100)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg="lightyellow").place(x=520, y=100, width=150)
        btn_search = Button(self.root, text='Search', font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=680, y=100, width=100, height=35)
        btn_clear = Button(self.root, text='Clear', font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.clear).place(x=800, y=100, width=100, height=35)

        # Result Labels
        labels = ["Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage"]
        positions = [150, 300, 450, 600, 750, 900]
        self.fields = []

        for i, label in enumerate(labels):
            Label(self.root, text=label, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=positions[i], y=230, width=150, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)
        self.name = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)
        self.course = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)
        self.marks = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.marks.place(x=600, y=280, width=150, height=50)
        self.full = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.full.place(x=750, y=280, width=150, height=50)
        self.per = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)

        # Delete Button
        btn_delete = Button(self.root, text='Delete', font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.delete)
        btn_delete.place(x=500, y=350, width=150, height=35)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="77492652Rt@",  
            database="student_management"
        )

    def search(self):
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
                return

            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll=%s", (self.var_search.get(),))
            row = cur.fetchone()
            con.close()

            if row is not None:
                self.var_id = row[0]
                self.roll.config(text=row[1])
                self.name.config(text=row[2])
                self.course.config(text=row[3])
                self.marks.config(text=row[4])
                self.full.config(text=row[5])
                self.per.config(text=row[6])
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_id = ""
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        try:
            if self.var_id == "":
                messagebox.showerror("Error", "Select Student result first", parent=self.root)
                return

            con = self.connect_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE rid=%s", (self.var_id,))
            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", "Invalid Student Result", parent=self.root)
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                if op:
                    cur.execute("DELETE FROM result WHERE rid=%s", (self.var_id,))
                    con.commit()
                    messagebox.showinfo("Delete", "Result Deleted Successfully", parent=self.root)
                    self.clear()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()


