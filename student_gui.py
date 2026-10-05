import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ================= DATABASE =================

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL
)
""")

connection.commit()


# ================= FUNCTIONS =================

def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    course = course_entry.get().strip()

    if not name or not roll or not course:
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        cursor.execute(
            "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
            (name, roll, course)
        )
        connection.commit()

        messagebox.showinfo("Success", "Student added successfully!")

        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This roll number already exists."
        )


def view_students():
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute(
        "SELECT id, name, roll_no, course FROM students"
    )

    students = cursor.fetchall()

    for student in students:
        student_table.insert("", tk.END, values=student)

    count_label.config(
        text=f"Total Students: {len(students)}"
    )


def search_student():
    roll = search_entry.get().strip()

    if not roll:
        messagebox.showwarning(
            "Warning",
            "Enter a roll number to search."
        )
        return

    cursor.execute(
        "SELECT id, name, roll_no, course FROM students WHERE roll_no = ?",
        (roll,)
    )

    student = cursor.fetchone()

    for item in student_table.get_children():
        student_table.delete(item)

    if student:
        student_table.insert("", tk.END, values=student)
    else:
        messagebox.showinfo(
            "Search Result",
            "Student not found."
        )


def delete_student():
    roll = delete_entry.get().strip()

    if not roll:
        messagebox.showwarning(
            "Warning",
            "Enter a roll number to delete."
        )
        return

    cursor.execute(
        "SELECT name FROM students WHERE roll_no = ?",
        (roll,)
    )

    student = cursor.fetchone()

    if not student:
        messagebox.showinfo(
            "Result",
            "Student not found."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete student {student[0]}?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll,)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        delete_entry.delete(0, tk.END)
        view_students()


def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


def show_all_students():
    search_entry.delete(0, tk.END)
    view_students()


def close_application():
    connection.close()
    root.destroy()


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Student Management System")
root.geometry("950x700")
root.resizable(False, False)

root.configure(bg="#eef2f7")


# ================= TITLE =================

title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 26, "bold"),
    bg="#eef2f7",
    fg="#1f2937"
)

title_label.pack(pady=(25, 5))


subtitle_label = tk.Label(
    root,
    text="Manage student records easily",
    font=("Arial", 12),
    bg="#eef2f7",
    fg="#6b7280"
)

subtitle_label.pack(pady=(0, 20))


# ================= INPUT FRAME =================

input_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

input_frame.pack(padx=50, fill="x")


# Student Name

tk.Label(
    input_frame,
    text="Student Name",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#374151"
).grid(row=0, column=0, padx=20, pady=15, sticky="w")

name_entry = tk.Entry(
    input_frame,
    font=("Arial", 11),
    width=30
)

name_entry.grid(row=0, column=1, padx=10, pady=15)


# Roll Number

tk.Label(
    input_frame,
    text="Roll Number",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#374151"
).grid(row=0, column=2, padx=20, pady=15, sticky="w")

roll_entry = tk.Entry(
    input_frame,
    font=("Arial", 11),
    width=20
)

roll_entry.grid(row=0, column=3, padx=10, pady=15)


# Course

tk.Label(
    input_frame,
    text="Course",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#374151"
).grid(row=1, column=0, padx=20, pady=15, sticky="w")

course_entry = tk.Entry(
    input_frame,
    font=("Arial", 11),
    width=30
)

course_entry.grid(row=1, column=1, padx=10, pady=15)


# Add Button

add_button = tk.Button(
    input_frame,
    text="ADD STUDENT",
    command=add_student,
    font=("Arial", 10, "bold"),
    width=18,
    pady=7,
    bg="#2563eb",
    fg="white",
    relief="flat",
    cursor="hand2"
)

add_button.grid(row=1, column=3, padx=10, pady=15)


# ================= SEARCH FRAME =================

search_frame = tk.Frame(
    root,
    bg="#eef2f7"
)

search_frame.pack(pady=20)


tk.Label(
    search_frame,
    text="Search by Roll Number:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7",
    fg="#374151"
).pack(side="left", padx=10)


search_entry = tk.Entry(
    search_frame,
    font=("Arial", 11),
    width=20
)

search_entry.pack(side="left", padx=5)


search_button = tk.Button(
    search_frame,
    text="SEARCH",
    command=search_student,
    font=("Arial", 10, "bold"),
    width=12,
    pady=5,
    bg="#059669",
    fg="white",
    relief="flat",
    cursor="hand2"
)

search_button.pack(side="left", padx=5)


all_button = tk.Button(
    search_frame,
    text="SHOW ALL",
    command=show_all_students,
    font=("Arial", 10, "bold"),
    width=12,
    pady=5,
    bg="#6b7280",
    fg="white",
    relief="flat",
    cursor="hand2"
)

all_button.pack(side="left", padx=5)


# ================= TABLE =================

table_frame = tk.Frame(
    root,
    bg="white"
)

table_frame.pack(padx=50, fill="both")


columns = (
    "ID",
    "Name",
    "Roll Number",
    "Course"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


student_table.heading("ID", text="ID")
student_table.heading("Name", text="Student Name")
student_table.heading("Roll Number", text="Roll Number")
student_table.heading("Course", text="Course")


student_table.column("ID", width=70, anchor="center")
student_table.column("Name", width=250, anchor="center")
student_table.column("Roll Number", width=200, anchor="center")
student_table.column("Course", width=250, anchor="center")


student_table.pack(fill="both")


# ================= DELETE FRAME =================

delete_frame = tk.Frame(
    root,
    bg="#eef2f7"
)

delete_frame.pack(pady=20)


tk.Label(
    delete_frame,
    text="Delete Roll Number:",
    font=("Arial", 11, "bold"),
    bg="#eef2f7",
    fg="#374151"
).pack(side="left", padx=10)


delete_entry = tk.Entry(
    delete_frame,
    font=("Arial", 11),
    width=20
)

delete_entry.pack(side="left", padx=5)


delete_button = tk.Button(
    delete_frame,
    text="DELETE STUDENT",
    command=delete_student,
    font=("Arial", 10, "bold"),
    width=16,
    pady=6,
    bg="#dc2626",
    fg="white",
    relief="flat",
    cursor="hand2"
)

delete_button.pack(side="left", padx=5)


# ================= BOTTOM =================

count_label = tk.Label(
    root,
    text="Total Students: 0",
    font=("Arial", 11, "bold"),
    bg="#eef2f7",
    fg="#374151"
)

count_label.pack(pady=5)


exit_button = tk.Button(
    root,
    text="EXIT",
    command=close_application,
    font=("Arial", 10, "bold"),
    width=12,
    pady=6,
    bg="#374151",
    fg="white",
    relief="flat",
    cursor="hand2"
)

exit_button.pack(pady=10)


# ================= START =================

view_students()

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

root.mainloop()
