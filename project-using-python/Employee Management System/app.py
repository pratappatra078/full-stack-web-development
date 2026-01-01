from flask import Flask, request, jsonify, send_from_directory      # Import Flask utilities
from flask_cors import CORS                                         # Allow CORS (frontend requests)
import sqlite3                                                      # SQLite database
import os                                                           # OS functions
from datetime import datetime                                       # To handle dates

app = Flask(__name__)                                               # Create Flask app
CORS(app)                                                            # Enable CORS

# Database file name
DB_NAME = 'employees.db'

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_NAME)                                 # Connect to database
    cursor = conn.cursor()                                          # Create cursor

    # Create employees table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,                   # Auto ID
            name TEXT NOT NULL,                                     # Employee name
            position TEXT NOT NULL,                                 # Job role
            monthly_salary REAL NOT NULL,                           # Salary
            email TEXT,                                             # Email optional
            phone TEXT,                                             # Phone optional
            date_joined TEXT,                                       # Date joined
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP          # Timestamp
        )
    ''')

    conn.commit()                                                   # Save changes
    conn.close()                                                    # Close connection

# Initialize DB when server starts
init_db()

# PF constant rate
PF_RATE = 0.12  # 12%

def get_db_connection():
    """Create and return a connection to the DB."""
    conn = sqlite3.connect(DB_NAME)                                 # Connect
    conn.row_factory = sqlite3.Row                                  # Access rows by name
    return conn

@app.route('/')
def index():
    """Serve index.html file."""
    return send_from_directory('.', 'index.html')                   # Return file

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Fetch all employees."""
    try:
        conn = get_db_connection()                                  # Open DB
        employees = conn.execute('SELECT * FROM employees ORDER BY id DESC').fetchall()
        conn.close()

        employees_list = []                                         # Store final list
        for emp in employees:
            employees_list.append({                                 # Convert row to dictionary
                'id': emp['id'],
                'name': emp['name'],
                'position': emp['position'],
                'monthly_salary': emp['monthly_salary'],
                'email': emp['email'],
                'phone': emp['phone'],
                'date_joined': emp['date_joined']
            })

        return jsonify(employees_list), 200                         # Return as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500                      # Error

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a single employee using ID."""
    try:
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        conn.close()

        if employee is None:                                        # If no employee found
            return jsonify({'error': 'Employee not found'}), 404

        # Convert row to dictionary
        emp_data = {
            'id': employee['id'],
            'name': employee['name'],
            'position': employee['position'],
            'monthly_salary': employee['monthly_salary'],
            'email': employee['email'],
            'phone': employee['phone'],
            'date_joined': employee['date_joined']
        }

        return jsonify(emp_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def add_employee():
    """Add a new employee to DB."""
    try:
        data = request.json                                         # Read JSON input

        # Validate required fields
        if not data.get('name') or not data.get('position'):
            return jsonify({'error': 'Name and position are required'}), 400

        monthly_salary = float(data.get('monthly_salary', 0))
        if monthly_salary < 0:                                      # Salary cannot be negative
            return jsonify({'error': 'Monthly salary cannot be negative'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new employee
        cursor.execute('''
            INSERT INTO employees (name, position, monthly_salary, email, phone, date_joined)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['position'],
            monthly_salary,
            data.get('email', ''),
            data.get('phone', ''),
            data.get('date_joined', datetime.now().strftime('%Y-%m-%d'))
        ))

        employee_id = cursor.lastrowid                               # Get new ID
        conn.commit()
        conn.close()

        return jsonify({'message': 'Employee added successfully', 'id': employee_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update existing employee."""
    try:
        data = request.json                                          # Input data

        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()

        if employee is None:                                         # If not found
            conn.close()
            return jsonify({'error': 'Employee not found'}), 404

        # Update values (use old values if not provided)
        name = data.get('name', employee['name'])
        position = data.get('position', employee['position'])
        monthly_salary = float(data.get('monthly_salary', employee['monthly_salary']))
        email = data.get('email', employee['email'])
        phone = data.get('phone', employee['phone'])
        date_joined = data.get('date_joined', employee['date_joined'])

        if monthly_salary < 0:
            conn.close()
            return jsonify({'error': 'Monthly salary cannot be negative'}), 400

        # Update query
        conn.execute('''
            UPDATE employees
            SET name = ?, position = ?, monthly_salary = ?, email = ?, phone = ?, date_joined = ?
            WHERE id = ?
        ''', (name, position, monthly_salary, email, phone, date_joined, employee_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Employee updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete employee."""
    try:
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()

        if employee is None:
            conn.close()
            return jsonify({'error': 'Employee not found'}), 404

        conn.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payroll/<int:employee_id>', methods=['GET'])
def get_employee_payroll(employee_id):
    """Calculate payroll for one employee."""
    try:
        conn = get_db_connection()
        employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        conn.close()

        if employee is None:
            return jsonify({'error': 'Employee not found'}), 404

        # Payroll calculations
        monthly_salary = employee['monthly_salary']
        monthly_pf = monthly_salary * PF_RATE
        net_monthly_pay = monthly_salary - monthly_pf
        yearly_gross = monthly_salary * 12
        yearly_pf = monthly_pf * 12
        yearly_net = net_monthly_pay * 12

        payroll_data = {
            'employee_id': employee['id'],
            'employee_name': employee['name'],
            'monthly_gross_pay': round(monthly_salary, 2),
            'monthly_pf_contribution': round(monthly_pf, 2),
            'monthly_net_pay': round(net_monthly_pay, 2),
            'yearly_gross_pay': round(yearly_gross, 2),
            'yearly_pf_contribution': round(yearly_pf, 2),
            'yearly_net_pay': round(yearly_net, 2)
        }

        return jsonify(payroll_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payroll/report', methods=['GET'])
def generate_payroll_report():
    """Generate payroll report for all employees."""
    try:
        conn = get_db_connection()
        employees = conn.execute('SELECT * FROM employees').fetchall()
        conn.close()

        if not employees:                                            # If no employees exist
            return jsonify({'error': 'No employees found'}), 404

        report = []                                                  # List of each employee payroll
        total_monthly_payroll = 0
        total_yearly_payroll = 0
        total_monthly_pf = 0
        total_yearly_pf = 0

        # Loop over all employees
        for emp in employees:
            monthly_salary = emp['monthly_salary']
            monthly_pf = monthly_salary * PF_RATE
            net_monthly_pay = monthly_salary - monthly_pf
            yearly_gross = monthly_salary * 12
            yearly_pf = monthly_pf * 12
            yearly_net = net_monthly_pay * 12

            # Add data to report list
            report.append({
                'id': emp['id'],
                'name': emp['name'],
                'position': emp['position'],
                'monthly_gross_pay': round(monthly_salary, 2),
                'monthly_pf_contribution': round(monthly_pf, 2),
                'monthly_net_pay': round(net_monthly_pay, 2),
                'yearly_gross_pay': round(yearly_gross, 2),
                'yearly_pf_contribution': round(yearly_pf, 2),
                'yearly_net_pay': round(yearly_net, 2)
            })

            # Add totals
            total_monthly_payroll += monthly_salary
            total_yearly_payroll += yearly_gross
            total_monthly_pf += monthly_pf
            total_yearly_pf += yearly_pf

        # Combine report + totals
        summary = {
            'employees': report,
            'totals': {
                'total_monthly_payroll': round(total_monthly_payroll, 2),
                'total_yearly_payroll': round(total_yearly_payroll, 2),
                'total_monthly_pf': round(total_monthly_pf, 2),
                'total_yearly_pf': round(total_yearly_pf, 2)
            }
        }

        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)                                   # Start server
