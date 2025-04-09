# Creating GUI Mock Test Application using Tkinter
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import datetime

# Creating Class with name MockTestApp to handle mock test logic and UI
class MockTestApp:
    def __init__(self, root, student_name):
        self.root = root
        self.root.title("Mock Test")
        self.root.geometry("700x400")
        self.root.config(bg="#f0f0f0")
        self.student_name = student_name

        # Creating questions list with question text, options, and correct answer
        self.questions = [
            {
                'question': "Samuel covers the distance from his home to his office at a speed of 25 km/hr and comes back at 4 km/hr. Journey is 5h 48m. Distance?",
                'options': ["20 km", "18 km", "15 km", "25 km"],
                'answer': "20 km"
            },
            {
                'question': "Policeman sees thief at 100m. Thief: 8 km/hr, Policeman: 10 km/hr. Distance before caught?",
                'options': ["250 meters", "400 meters", "450 meters", "401 meters"],
                'answer': "400 meters"
            },
            {
                'question': "Paul travels 24 km. After 1h 40m, 5/7 of distance left is covered. Speed in m/s?",
                'options': ["5/3 m/s", "7/5 m/s", "2/3 m/s", "8/5 m/s"],
                'answer': "5/3 m/s"
            },
            {
                'question': "Speed ratio of two trains is 7:8. Second train = 400km in 4h. First train speed?",
                'options': ["69.4 km/h", "78.6 km/h", "87.5 km/h", "40.5 km/h"],
                'answer': "87.5 km/h"
            }
        ]

        self.q_index = 0
        self.score = 0
        self.selected_option = tk.StringVar()

        # Displaying question label
        self.question_label = tk.Label(root, text="", wraplength=650, font=('Arial', 14), bg="#f0f0f0")
        self.question_label.pack(pady=20)

        # Creating RadioButtons for options
        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.selected_option, value="", font=('Arial', 12), bg="#f0f0f0")
            rb.pack(anchor="w", padx=50)
            self.options.append(rb)

        # Creating Next button
        self.next_btn = tk.Button(root, text="Next", command=self.next_question, font=('Arial', 12), bg="#4caf50", fg="white")
        self.next_btn.pack(pady=20)

        # Display first question
        self.display_question()

    # Creating method display_question to show each question and its options
    def display_question(self):
        q = self.questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index + 1}: {q['question']}")
        self.selected_option.set(None)
        for i, option in enumerate(q['options']):
            self.options[i].config(text=option, value=option)

    # Creating method next_question to handle answer check and move to next
    def next_question(self):
        if self.selected_option.get() == "":
            messagebox.showwarning("No Selection", "Please select an option!")
            return

        # Checking correct answer
        if self.selected_option.get() == self.questions[self.q_index]['answer']:
            self.score += 1

        self.q_index += 1
        if self.q_index < len(self.questions):
            self.display_question()
        else:
            self.save_result_to_db()
            messagebox.showinfo("Result", f"Your Score: {self.score} out of {len(self.questions)}")
            self.root.destroy()

    # Creating method save_result_to_db to store test result in MySQL
    def save_result_to_db(self):
        try:
            # Connecting to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="77492652Rt@",
                database="student_management"
            )
            cursor = conn.cursor()

            # Calculating percentage
            total_questions = len(self.questions)
            percentage = (self.score / total_questions) * 100

            # Inserting test result with percentage and date_taken
            insert_query = """
                INSERT INTO mock_test_result (student_name, score, total_questions, percentage, date_taken)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                self.student_name,
                self.score,
                total_questions,
                percentage,
                datetime.now()
            ))
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to save result: {e}")

# Creating function run_mock_test to launch the mock test window
def run_mock_test():
    student_name = simpledialog.askstring("Student Name", "Enter your full name:")
    if not student_name:
        messagebox.showerror("Error", "Student name is required to take the test!")
        return

    root = tk.Tk()
    app = MockTestApp(root, student_name)
    root.mainloop()

# Running mock test if file is run directly
if __name__ == "__main__":
    run_mock_test()


