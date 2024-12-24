from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    employees = db.relationship('Employee', backref='manager', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)  # Thêm trường department
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    contract_start = db.Column(db.Date, nullable=False)
    contract_end = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    check_in = db.Column(db.DateTime, default=datetime.utcnow)
    check_out = db.Column(db.DateTime)
    date = db.Column(db.Date, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.employee.name} on {self.date}>'

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    bonus = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    total_salary = db.Column(db.Float)

    employee = db.relationship('Employee', backref=db.backref('salaries', lazy=True))

    def __repr__(self):
        return f'<Salary for {self.employee.name}>'

    def calculate_total_salary(self):
        return self.base_salary + self.bonus - self.deductions

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('leaves', lazy=True))

    def __repr__(self):
        return f'<Leave {self.employee.name} from {self.start_date} to {self.end_date}>'
