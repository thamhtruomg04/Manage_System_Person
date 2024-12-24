from datetime import datetime
from app import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)  # Thêm trường department
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    contract_start = db.Column(db.Date, nullable=False)
    contract_end = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'
