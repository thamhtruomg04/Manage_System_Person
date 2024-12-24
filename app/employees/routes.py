from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Employee, Attendance, Salary
from app.employees.forms import EmployeeForm, AttendanceForm, SalaryForm

employees = Blueprint('employees', __name__)

@employees.route("/employees", methods=['GET'])
@login_required
def list_employees():
    employees = Employee.query.all()
    return render_template('list_employees.html', employees=employees, title='List Employees')

@employees.route("/employee/new", methods=['GET', 'POST'])
@login_required
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        try:
            employee = Employee(
                name=form.name.data,
                position=form.position.data,
                department=form.department.data,
                hire_date=form.hire_date.data,
                salary=form.salary.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data,
                contract_start=form.contract_start.data,
                contract_end=form.contract_end.data,
                status=form.status.data,
                manager_id=current_user.id
            )
            db.session.add(employee)
            db.session.commit()
            flash('Employee has been created!', 'success')
            return redirect(url_for('employees.list_employees'))
        except Exception as e:
            print(f"Error occurred: {e}")
            flash('An error occurred while creating the employee.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        print(form.errors)  # In lỗi biểu mẫu ra console hoặc terminal
    return render_template('create_employee.html', title='New Employee', form=form, legend='New Employee')

@employees.route("/employee/<int:employee_id>/update", methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm()

    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.department = form.department.data
        employee.hire_date = form.hire_date.data
        employee.salary = form.salary.data
        employee.email = form.email.data
        employee.phone = form.phone.data
        employee.address = form.address.data
        employee.contract_start = form.contract_start.data
        employee.contract_end = form.contract_end.data
        employee.status = form.status.data
        db.session.commit()
        flash('Employee has been updated!', 'success')
        return redirect(url_for('employees.list_employees'))
    elif request.method == 'GET':
        form.name.data = employee.name
        form.position.data = employee.position
        form.department.data = employee.department
        form.hire_date.data = employee.hire_date
        form.salary.data = employee.salary
        form.email.data = employee.email
        form.phone.data = employee.phone
        form.address.data = employee.address
        form.contract_start.data = employee.contract_start
        form.contract_end.data = employee.contract_end
        form.status.data = employee.status
    return render_template('edit_employee.html', title='Update Employee', form=form, legend='Update Employee', employee=employee)

@employees.route("/employee/<int:employee_id>/delete", methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee has been deleted!', 'success')
    return redirect(url_for('employees.list_employees'))

@employees.route("/employee/<int:employee_id>/attendance", methods=['GET', 'POST'])
@login_required
def manage_attendance(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = AttendanceForm()

    if form.validate_on_submit():
        try:
            attendance = Attendance(
                employee_id=employee.id,
                check_in=form.check_in.data,
                check_out=form.check_out.data
            )
            db.session.add(attendance)
            db.session.commit()
            flash('Attendance record has been saved!', 'success')
            return redirect(url_for('employees.manage_attendance', employee_id=employee.id))
        except Exception as e:
            print(f"Error occurred: {e}")
            flash('An error occurred while saving the attendance record.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        print(form.errors)

    attendances = Attendance.query.filter_by(employee_id=employee_id).all()
    total_sessions = len(attendances)  # Tính tổng số buổi làm việc
    return render_template('manage_attendance.html', form=form, employee=employee, attendances=attendances, total_sessions=total_sessions)

@employees.route("/employee/<int:employee_id>/attendance/view", methods=['GET'])
@login_required
def view_attendance(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    attendances = Attendance.query.filter_by(employee_id=employee_id).all()
    return render_template('view_attendance.html', employee=employee, attendances=attendances)

@employees.route("/employee/<int:employee_id>/salary", methods=['GET', 'POST'])
@login_required
def manage_salary(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = SalaryForm()
    salaries = Salary.query.filter_by(employee_id=employee_id).all()

    if form.validate_on_submit():
        try:
            salary = Salary(
                employee_id=employee.id,
                base_salary=form.base_salary.data,
                bonus=form.bonus.data,
                deductions=form.deductions.data,
                total_salary=form.base_salary.data + form.bonus.data - form.deductions.data  # Tính toán tổng lương
            )
            db.session.add(salary)
            db.session.commit()
            flash('Salary record has been saved!', 'success')
            return redirect(url_for('employees.manage_salary', employee_id=employee.id))
        except Exception as e:
            print(f"Error occurred: {e}")
            flash('An error occurred while saving the salary record.', 'danger')
    return render_template('manage_salary.html', form=form, employee=employee, salaries=salaries)

@employees.route("/employee/<int:employee_id>/salary/view", methods=['GET'])
@login_required
def view_salary(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    salaries = Salary.query.filter_by(employee_id=employee_id).all()
    return render_template('view_salary.html', employee=employee, salaries=salaries)
