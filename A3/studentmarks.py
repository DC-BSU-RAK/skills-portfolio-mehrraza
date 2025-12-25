import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2f")  

        self.students = []
        self.load_students()

        self.title_label = tk.Label(root, text="📚 Student Manager", font=("Arial", 28, "bold"), bg="#1e1e2f", fg="#00ffff")
        self.title_label.pack(pady=15)

        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        menu_buttons = [
            ("View All Students", self.view_all),
            ("View Individual Student", self.view_individual),
            ("Highest Overall Mark", self.highest_student),
            ("Lowest Overall Mark", self.lowest_student),
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Student", self.update_student)
        ]

        colors = ["#ff4b5c","#ff6f61","#ffcc5c","#88d8b0","#6a2c70","#f08a5d","#b83b5e","#3a506b"]

        for i, (text, cmd) in enumerate(menu_buttons):
            btn = tk.Button(btn_frame, text=text, font=("Arial", 12, "bold"), width=28, bg=colors[i], fg="white",
                            activebackground="#00ffff", activeforeground="#1e1e2f", bd=0, relief=tk.FLAT, command=cmd)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#00ffff", fg="#1e1e2f"))
            btn.bind("<Leave>", lambda e, b=btn, c=colors[i]: b.config(bg=c, fg="white"))

        self.output_area = tk.Text(root, height=22, width=110, bg="#2e2e3f", fg="white", font=("Courier", 11))
        self.output_area.pack(pady=15, padx=20)
        self.output_area.config(state=tk.DISABLED)

    def load_students(self):
        if not os.path.exists(FILE_PATH):
            messagebox.showerror("Error", f"{FILE_PATH} not found!")
            return
        self.students = []
        with open(FILE_PATH, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue
                code, name, m1, m2, m3, exam = parts
                try:
                    marks = [int(m1), int(m2), int(m3)]
                    exam_mark = int(exam)
                    self.students.append({
                        "code": code,
                        "name": name,
                        "marks": marks,
                        "exam": exam_mark
                    })
                except ValueError:
                    continue

    def save_students(self):
        with open(FILE_PATH, "w") as f:
            f.write(f"{len(self.students)}\n")
            for s in self.students:
                f.write(f"{s['code']},{s['name']},{s['marks'][0]},{s['marks'][1]},{s['marks'][2]},{s['exam']}\n")

    def calculate_total(self, student):
        return sum(student["marks"])

    def calculate_percentage(self, student):
        return round((self.calculate_total(student) + student["exam"]) / 160 * 100, 2)

    def calculate_grade(self, percent):
        if percent >= 70: return "A"
        elif percent >= 60: return "B"
        elif percent >= 50: return "C"
        elif percent >= 40: return "D"
        return "F"

    def display_students(self, students):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        total_percent = 0
        for idx, s in enumerate(students):
            total_marks = self.calculate_total(s)
            percent = self.calculate_percentage(s)
            grade = self.calculate_grade(percent)
            total_percent += percent
            bg_color = "#3a3a4f" if idx % 2 == 0 else "#2e2e3f"
            self.output_area.tag_configure(f"row{idx}", background=bg_color)
            self.output_area.insert(tk.END, f"Code: {s['code']} | Name: {s['name']}\n", f"row{idx}")
            self.output_area.insert(tk.END, f"Coursework: {total_marks} | Exam: {s['exam']} | Overall %: {percent} | Grade: {grade}\n", f"row{idx}")
            self.output_area.insert(tk.END, "-"*90 + "\n", f"row{idx}")
        if students:
            avg = round(total_percent / len(students), 2)
            self.output_area.insert(tk.END, f"Total Students: {len(students)} | Average %: {avg}\n")
        self.output_area.config(state=tk.DISABLED)

    def view_all(self):
        self.display_students(self.students)

    def view_individual(self):
        code = simpledialog.askstring("Input", "Enter student code:")
        if code is None: return
        student = next((s for s in self.students if s["code"] == code), None)
        if not student:
            messagebox.showinfo("Not Found", f"No student found with code {code}")
            return
        self.display_students([student])

    def highest_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        student = max(self.students, key=lambda s: self.calculate_percentage(s))
        self.display_students([student])

    def lowest_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        student = min(self.students, key=lambda s: self.calculate_percentage(s))
        self.display_students([student])

    def sort_records(self):
        choice = simpledialog.askstring("Sort", "Sort by percentage ascending or descending? (asc/desc)")
        if choice is None: return
        if choice not in ["asc", "desc"]: return
        reverse = True if choice == "desc" else False
        sorted_list = sorted(self.students, key=lambda s: self.calculate_percentage(s), reverse=reverse)
        self.display_students(sorted_list)

    def add_student(self):
        code = simpledialog.askstring("Input", "Student code:")
        if code is None: return
        name = simpledialog.askstring("Input", "Student name:")
        if name is None: return
        marks = []
        for i in range(1, 4):
            m = simpledialog.askinteger("Input", f"Coursework mark {i} (0-20):", minvalue=0, maxvalue=20)
            if m is None: return
            marks.append(m)
        exam = simpledialog.askinteger("Input", "Exam mark (0-100):", minvalue=0, maxvalue=100)
        if exam is None: return
        self.students.append({"code": code, "name": name, "marks": marks, "exam": exam})
        self.save_students()
        messagebox.showinfo("Success", "Student added successfully!")

    def delete_student(self):
        code = simpledialog.askstring("Input", "Enter student code to delete:")
        if code is None: return
        student = next((s for s in self.students if s["code"] == code), None)
        if not student:
            messagebox.showinfo("Not Found", f"No student found with code {code}")
            return
        self.students.remove(student)
        self.save_students()
        messagebox.showinfo("Deleted", "Student record deleted.")

    def update_student(self):
        code = simpledialog.askstring("Input", "Enter student code to update:")
        if code is None: return
        student = next((s for s in self.students if s["code"] == code), None)
        if not student:
            messagebox.showinfo("Not Found", f"No student found with code {code}")
            return
        options = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam"]
        choice = simpledialog.askstring("Update", f"What do you want to update? {options}")
        if choice is None: return
        choice_lower = choice.lower()
        if choice_lower == "name":
            new_name = simpledialog.askstring("Input", "Enter new name:")
            if new_name is not None: student["name"] = new_name
        elif choice_lower.startswith("coursework"):
            try:
                index = int(choice[-1]) - 1
            except ValueError:
                messagebox.showinfo("Error", "Invalid coursework selection.")
                return
            new_mark = simpledialog.askinteger("Input", f"Enter new mark for coursework {index+1} (0-20):", minvalue=0, maxvalue=20)
            if new_mark is not None: student["marks"][index] = new_mark
        elif choice_lower == "exam":
            new_exam = simpledialog.askinteger("Input", "Enter new exam mark (0-100):", minvalue=0, maxvalue=100)
            if new_exam is not None: student["exam"] = new_exam
        else:
            messagebox.showinfo("Error", "Invalid choice")
            return
        self.save_students()
        messagebox.showinfo("Updated", "Student record updated.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
