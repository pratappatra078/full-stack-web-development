import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox

# Connect to Database
try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="192009",   # Change if needed
        database="student_management"
    )
    cursor = con.cursor()
except:
    print("Database Connection Failed! Check MySQL settings")
    exit()


def clear_fields():
    entry_roll.delete(0, END)
    entry_name.delete(0, END)
    entry_semester.set("")   # Because semester is dropdown
    entry_m1.delete(0, END)
    entry_m2.delete(0, END)
    entry_m3.delete(0, END)


def add_student():
    try:
        roll = int(entry_roll.get())
        name = entry_name.get()
        semester = entry_semester.get()
        m1 = int(entry_m1.get())
        m2 = int(entry_m2.get())
        m3 = int(entry_m3.get())
        total = m1 + m2 + m3
        percentage = (total * 5) / 3

        cursor.execute("INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (roll, name, semester, m1, m2, m3, total, percentage))
        con.commit()
        messagebox.showinfo("Success", "Student Added Successfully!")
        view_students()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")


def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", END, values=row)


def search_student():
    try:
        roll = entry_roll.get()
        name = entry_name.get()
        semester = entry_semester.get()

        if roll:
            cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll,))
        elif name:
            cursor.execute("SELECT * FROM students WHERE name LIKE %s", ("%" + name + "%",))
        elif semester:
            cursor.execute("SELECT * FROM students WHERE semester=%s", (semester,))
        else:
            messagebox.showwarning("Input Error", "Enter Roll No, Name OR Select Semester!")
            return

        rows = cursor.fetchall()
        student_table.delete(*student_table.get_children())

        if rows:
            for row in rows:
                student_table.insert("", END, values=row)
        else:
            messagebox.showwarning("Not Found", "No student data found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_marks():
    try:
        roll = int(entry_roll.get())
        m1 = int(entry_m1.get())
        m2 = int(entry_m2.get())
        m3 = int(entry_m3.get())
        total = m1 + m2 + m3
        percentage = (total * 5) / 3

        cursor.execute(
            "UPDATE students SET marks1=%s,marks2=%s,marks3=%s,total=%s,percentage=%s WHERE roll_no=%s",
            (m1, m2, m3, total, percentage, roll))
        con.commit()
        messagebox.showinfo("Updated", "Marks Updated Successfully!")
        view_students()
    except:
        messagebox.showerror("Error", "Select a student or enter valid data!")


def sem_update():
    try:
        roll = int(entry_roll.get())
        semester = entry_semester.get()

        cursor.execute("UPDATE students SET semester=%s WHERE roll_no=%s",
                       (semester, roll))
        con.commit()

        messagebox.showinfo("Updated", "Semester Updated Successfully!")
        view_students()
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")


def delete_student():
    try:
        roll = entry_roll.get()
        cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll,))
        con.commit()
        messagebox.showinfo("Deleted", "Record Deleted")
        view_students()
        clear_fields()
    except:
        messagebox.showerror("Error", "Enter a valid Roll Number")


# GUI Window
root = Tk()
root.title("Student Result Management System")
root.geometry("1100x600")
root.config(bg="#cfe2ff")  # Light soft blue background

# Modern Style
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview.Heading",
                background="#0047AB",
                foreground="white",
                font=("Arial", 11, "bold"))
style.configure("Treeview",
                font=("Arial", 11),
                rowheight=28)

# White Input Card
frame = Frame(root, bg="white", bd=4, relief=GROOVE)
frame.place(x=20, y=20, width=450, height=260)

Label(frame, text="Student Details", font=("Arial", 16, "bold"), bg="white", fg="#0047AB").place(x=120, y=5)

Label(frame, text="Roll No", bg="white", font=("Arial", 12)).place(x=20, y=50)
entry_roll = Entry(frame, width=25); entry_roll.place(x=150, y=50)

Label(frame, text="Name", bg="white", font=("Arial", 12)).place(x=20, y=85)
entry_name = Entry(frame, width=25); entry_name.place(x=150, y=85)

Label(frame, text="Semester", bg="white", font=("Arial", 12)).place(x=20, y=120)
entry_semester = Combobox(frame, values=["1","2","3","4","5","6","7","8"], width=23, state="readonly")
entry_semester.place(x=150, y=120)

Label(frame, text="Marks 1", bg="white", font=("Arial", 12)).place(x=20, y=155)
entry_m1 = Entry(frame, width=25); entry_m1.place(x=150, y=155)

Label(frame, text="Marks 2", bg="white", font=("Arial", 12)).place(x=20, y=190)
entry_m2 = Entry(frame, width=25); entry_m2.place(x=150, y=190)

Label(frame, text="Marks 3", bg="white", font=("Arial", 12)).place(x=20, y=225)
entry_m3 = Entry(frame, width=25); entry_m3.place(x=150, y=225)

# Buttons Frame
btn_frame = Frame(root, bg="#cfe2ff")
btn_frame.place(x=500, y=40)

button_style = {"width":16, "font":("Arial", 11, "bold"), "bg":"#0047AB", "fg":"white", "bd":3}

Button(btn_frame, text="Add", command=add_student, **button_style).grid(row=0, column=0, padx=10, pady=5)
Button(btn_frame, text="View All", command=view_students, **button_style).grid(row=0, column=1, padx=10, pady=5)
Button(btn_frame, text="Search", command=search_student, **button_style).grid(row=1, column=0, padx=10, pady=5)
Button(btn_frame, text="Update Marks", command=update_marks, **button_style).grid(row=1, column=1, padx=10, pady=5)
Button(btn_frame, text="Delete", command=delete_student, **button_style).grid(row=2, column=0, padx=10, pady=5)
Button(btn_frame, text="Update Semester", command=sem_update, **button_style).grid(row=2, column=1, padx=10, pady=5)

# Table Frame
table_frame = Frame(root, bg="white", bd=4, relief=GROOVE)
table_frame.place(x=20, y=300, width=1050, height=270)

columns = ("Roll No","Name","Semester","Marks1","Marks2","Marks3","Total","Percentage")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=120)

student_table.pack(fill=BOTH, expand=True)

view_students()
root.mainloop()
