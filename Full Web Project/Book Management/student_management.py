import json
import os

STUDENT_FILE = "students.json"

if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, 'w') as f:
        json.dump([], f)

def load_students():
    with open(STUDENT_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(STUDENT_FILE, 'w') as f:
        json.dump(students, f, indent=4)

def add_student():
    students = load_students()
    student = {
        "id": input("Enter Student ID: "),
        "name": input("Enter Student Name: "),
        "email": input("Enter Email: "),
        "phone": input("Enter Phone: "),
        "department": input("Enter Department: ")
    }
    students.append(student)
    save_students(students)
    print("Student added successfully!")

def search_student():
    students = load_students()
    name = input("Enter name to search: ").lower()
    found = [s for s in students if name in s['name'].lower()]
    if found:
        for s in found:
            print(s)
    else:
        print("Student not found.")

def update_student():
    students = load_students()
    sid = input("Enter Student ID to update: ")
    for s in students:
        if s['id'] == sid:
            s['name'] = input("New Name: ") or s['name']
            s['email'] = input("New Email: ") or s['email']
            s['phone'] = input("New Phone: ") or s['phone']
            save_students(students)
            print("Student updated successfully!")
            return
    print("Student ID not found.")

def delete_student():
    students = load_students()
    sid = input("Enter Student ID to delete: ")
    students = [s for s in students if s['id'] != sid]
    save_students(students)
    print("Student deleted successfully!")