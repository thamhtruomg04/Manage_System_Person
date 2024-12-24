from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app.models import Employee
from app import db
from datetime import datetime
from flask_paginate import Pagination, get_page_args
import pandas as pd
from app.users.decorators import admin_required  # Import decorator

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/employees', methods=['GET'])
@login_required
def index():
    search = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if search:
        employees = Employee.query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.position.ilike(f'%{search}%'))
        ).offset(offset).limit(per_page).all()
        total = Employee.query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.position.ilike(f'%{search}%'))
        ).count()
    else:
        employees = Employee.query.offset(offset).limit(per_page).all()
        total = Employee.query.count()

    pagination = Pagination(page=page, per_page=per_page, total=total, search=search, record_name='employees')

    return render_template('index.html', employees=employees, pagination=pagination, search=search)

@main.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required  # Bảo vệ route
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        contract_start = request.form['contract_start']
        contract_end = request.form['contract_end']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        status = request.form['status']

        if not all([name, position, salary, hire_date, contract_start, status]):
            return "Missing required fields", 400

        new_employee = Employee(
            name=name,
            position=position,
            salary=salary,
            hire_date=datetime.strptime(hire_date, '%Y-%m-%d'),
            contract_start=datetime.strptime(contract_start, '%Y-%m-%d'),
            contract_end=datetime.strptime(contract_end, '%Y-%m-%d') if contract_end else None,
            email=email,
            phone=phone,
            address=address,
            status=status
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee has been added!', 'success')

        return redirect(url_for('main.index'))
    return render_template('add_employee.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required  # Bảo vệ route
def edit_employee(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.position = request.form['position']
        employee.salary = request.form['salary']
        employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d')
        employee.contract_start = datetime.strptime(request.form['contract_start'], '%Y-%m-%d')
        employee.contract_end = datetime.strptime(request.form['contract_end'], '%Y-%m-%d') if request.form['contract_end'] else None
        employee.email = request.form['email']
        employee.phone = request.form['phone']
        employee.address = request.form['address']
        employee.status = request.form['status']

        db.session.commit()
        flash('Employee has been updated!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_employee.html', employee=employee)

@main.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required  # Bảo vệ route
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee has been deleted!', 'success')
    return redirect(url_for('main.index'))


@main.route('/export_csv')
@login_required
def export_csv():
    employees = Employee.query.all()
    employee_data = [{
        'name': emp.name,
        'position': emp.position,
        'salary': emp.salary,
        'hire_date': emp.hire_date,
        'email': emp.email,
        'phone': emp.phone,
        'address': emp.address,
        'contract_start': emp.contract_start,
        'contract_end': emp.contract_end,
        'status': emp.status
    } for emp in employees]

    df = pd.DataFrame(employee_data)
    response = make_response(df.to_csv(index=False))
    response.headers['Content-Disposition'] = 'attachment; filename=employees.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response
