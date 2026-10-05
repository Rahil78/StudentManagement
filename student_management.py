import sqlite3

# Connect to database
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL
)
""")

connection.commit()


def add_student():
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    course = input("Enter course: ")

    try:
        cursor.execute(
            "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
            (name, roll_no, course)
        )

        connection.commit()
        print("\nStudent added successfully!\n")

    except sqlite3.IntegrityError:
        print("\nRoll number already exists!\n")


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("\nNo students found.\n")
        return

    print("\n===== STUDENT LIST =====")

    for student in students:
        print("ID:", student[0])
        print("Name:", student[1])
        print("Roll Number:", student[2])
        print("Course:", student[3])
        print("------------------------")


def search_student():
    roll_no = input("Enter roll number to search: ")

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:
        print("\n===== STUDENT FOUND =====")
        print("ID:", student[0])
        print("Name:", student[1])
        print("Roll Number:", student[2])
        print("Course:", student[3])
    else:
        print("\nStudent not found.\n")


def delete_student():
    roll_no = input("Enter roll number to delete: ")

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("\nStudent deleted successfully!\n")
    else:
        print("\nStudent not found.\n")


while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("\nThank you for using Student Management System!")
        connection.close()
        break

    else:
        print("\nInvalid choice. Please try again.")