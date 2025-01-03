from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, FloatField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    position = StringField('Position', validators=[DataRequired(), Length(min=2, max=100)])
    department = StringField('Department', validators=[DataRequired(), Length(min=2, max=100)])
    hire_date = DateField('Hire Date', validators=[DataRequired()], format='%Y-%m-%d')
    salary = FloatField('Salary', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[Length(max=255)])
    contract_start = DateField('Contract Start', validators=[DataRequired()], format='%Y-%m-%d')
    contract_end = DateField('Contract End', format='%Y-%m-%d')
    status = StringField('Status', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Save')

class AttendanceForm(FlaskForm):
    check_in = DateTimeField('Check In', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    check_out = DateTimeField('Check Out', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Save')


class SalaryForm(FlaskForm):
    base_salary = FloatField('Base Salary', validators=[DataRequired()])
    bonus = FloatField('Bonus', default=0.0)
    deductions = FloatField('Deductions', default=0.0)
    submit = SubmitField('Save')


from wtforms import DateField, StringField, SelectField, SubmitField


class LeaveForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    reason = StringField('Reason', validators=[DataRequired(), Length(max=255)])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    submit = SubmitField('Submit')
