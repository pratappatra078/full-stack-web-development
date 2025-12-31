from flask import Flask, render_template, request, redirect, flash
from book_management import load_books, save_books
from student_management import load_students, save_students
from transaction_management import issue_book, return_book
import json
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-here'  # Required for flash messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        try:
            # Validate form data
            required_fields = ['id', 'title', 'author', 'isbn', 'quantity']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'Error: {field} is required', 'error')
                    return redirect('/books')
            
            books = load_books()
            
            # Check for duplicate ID
            book_id = request.form['id']
            if any(book['id'] == book_id for book in books):
                flash(f'Error: Book with ID {book_id} already exists', 'error')
                return redirect('/books')
            
            new_book = {
                "id": book_id,
                "title": request.form['title'],
                "author": request.form['author'],
                "isbn": request.form['isbn'],
                "quantity": int(request.form['quantity'])
            }
            books.append(new_book)
            save_books(books)
            flash('Book added successfully!', 'success')
            return redirect('/books')
        except ValueError:
            flash('Error: Quantity must be a number', 'error')
            return redirect('/books')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect('/books')
    
    try:
        books_list = load_books()
    except Exception as e:
        flash(f'Error loading books: {str(e)}', 'error')
        books_list = []
    
    return render_template('books.html', books=books_list)

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        try:
            # Validate form data
            required_fields = ['id', 'name', 'email', 'phone', 'department']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'Error: {field} is required', 'error')
                    return redirect('/students')
            
            students = load_students()
            
            # Check for duplicate ID
            student_id = request.form['id']
            if any(student['id'] == student_id for student in students):
                flash(f'Error: Student with ID {student_id} already exists', 'error')
                return redirect('/students')
            
            new_student = {
                "id": student_id,
                "name": request.form['name'],
                "email": request.form['email'],
                "phone": request.form['phone'],
                "department": request.form['department']
            }
            students.append(new_student)
            save_students(students)
            flash('Student added successfully!', 'success')
            return redirect('/students')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect('/students')
    
    try:
        students_list = load_students()
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        students_list = []
    
    return render_template('students.html', students=students_list)

@app.route('/transactions', methods=['GET'])
def transactions_page():
    try:
        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as f:
                transactions = json.load(f)
        else:
            transactions = []
            # Create empty transactions file
            with open("transactions.json", "w") as f:
                json.dump(transactions, f)
    except json.JSONDecodeError:
        flash('Error: Invalid transactions file', 'error')
        transactions = []
    except Exception as e:
        flash(f'Error loading transactions: {str(e)}', 'error')
        transactions = []
    
    return render_template('transactions.html', transactions=transactions)

@app.route('/issue_book', methods=['POST'])
def issue_book_route():
    try:
        # Get form data
        student_id = request.form.get('student_id')
        book_id = request.form.get('book_id')
        
        # Validate inputs
        if not student_id or not book_id:
            flash('Error: Student ID and Book ID are required', 'error')
            return redirect('/transactions')
        
        # Call issue_book with parameters
        result = issue_book(student_id, book_id)
        
        if result:
            flash('Book issued successfully!', 'success')
        else:
            flash('Error: Could not issue book', 'error')
            
    except Exception as e:
        flash(f'Error issuing book: {str(e)}', 'error')
    
    return redirect('/transactions')

@app.route('/return_book', methods=['POST'])
def return_book_route():
    try:
        # Get form data
        transaction_id = request.form.get('transaction_id')
        
        # Validate input
        if not transaction_id:
            flash('Error: Transaction ID is required', 'error')
            return redirect('/transactions')
        
        # Call return_book with parameter
        result = return_book(transaction_id)
        
        if result:
            flash('Book returned successfully!', 'success')
        else:
            flash('Error: Could not return book', 'error')
            
    except Exception as e:
        flash(f'Error returning book: {str(e)}', 'error')
    
    return redirect('/transactions')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    # Create necessary JSON files if they don't exist
    for filename in ['books.json', 'students.json', 'transactions.json']:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)
    
    app.run(debug=True)