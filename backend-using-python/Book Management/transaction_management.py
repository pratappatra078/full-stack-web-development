import json
import os
from datetime import datetime

BOOK_FILE = "books.json"
STUDENT_FILE = "students.json"
TRANSACTION_FILE = "transactions.json"

for f in [BOOK_FILE, STUDENT_FILE, TRANSACTION_FILE]:
    if not os.path.exists(f):
        with open(f, 'w') as file:
            json.dump([], file)

def load_data(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def issue_book():
    books = load_data(BOOK_FILE)
    students = load_data(STUDENT_FILE)
    transactions = load_data(TRANSACTION_FILE)

    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    book = next((b for b in books if b['id'] == bid), None)
    student = next((s for s in students if s['id'] == sid), None)

    if not book or not student:
        print("Invalid Student or Book ID.")
        return
    if book['quantity'] <= 0:
        print("Book not available.")
        return

    book['quantity'] -= 1
    transaction = {
        "student_id": sid,
        "book_id": bid,
        "issue_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": None
    }
    transactions.append(transaction)

    save_data(BOOK_FILE, books)
    save_data(TRANSACTION_FILE, transactions)
    print("Book issued successfully!")

def return_book():
    books = load_data(BOOK_FILE)
    transactions = load_data(TRANSACTION_FILE)

    sid = input("Enter Student ID: ")
    bid = input("Enter Book ID: ")

    for t in transactions:
        if t['student_id'] == sid and t['book_id'] == bid and t['return_date'] is None:
            t['return_date'] = datetime.now().strftime("%Y-%m-%d")
            for b in books:
                if b['id'] == bid:
                    b['quantity'] += 1
            save_data(BOOK_FILE, books)
            save_data(TRANSACTION_FILE, transactions)
            print("Book returned successfully!")
            return
    print("No active issue record found.")
