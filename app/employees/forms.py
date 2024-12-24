from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, FloatField, DateField, SubmitField
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
