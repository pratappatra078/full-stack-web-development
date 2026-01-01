import json
import os

BOOK_FILE = "books.json"

# Ensure book file exists
if not os.path.exists(BOOK_FILE):
    with open(BOOK_FILE, 'w') as f:
        json.dump([], f)

def load_books():
    with open(BOOK_FILE, 'r') as f:
        return json.load(f)

def save_books(books):
    with open(BOOK_FILE, 'w') as f:
        json.dump(books, f, indent=4)

def add_book():
    books = load_books()
    book = {
        "id": input("Enter Book ID: "),
        "title": input("Enter Book Title: "),
        "author": input("Enter Author Name: "),
        "isbn": input("Enter ISBN: "),
        "quantity": int(input("Enter Quantity: "))
    }
    books.append(book)
    save_books(books)
    print("Book added successfully!")

def search_book():
    books = load_books()
    key = input("Enter title/author to search: ").lower()
    found = [b for b in books if key in b['title'].lower() or key in b['author'].lower()]
    if found:
        for b in found:
            print(b)
    else:
        print("Book not found.")

def update_book():
    books = load_books()
    book_id = input("Enter Book ID to update: ")
    for b in books:
        if b['id'] == book_id:
            b['title'] = input("New Title: ") or b['title']
            b['author'] = input("New Author: ") or b['author']
            b['quantity'] = int(input("New Quantity: ") or b['quantity'])
            save_books(books)
            print("Book updated successfully!")
            return
    print("Book ID not found.")

def delete_book():
    books = load_books()
    book_id = input("Enter Book ID to delete: ")
    books = [b for b in books if b['id'] != book_id]
    save_books(books)
    print("Book deleted successfully!")
