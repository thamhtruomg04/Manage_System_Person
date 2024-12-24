from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@users.route("/delete_account/<int:user_id>", methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('You do not have permission to delete this account.', 'danger')
        return redirect(url_for('main.index'))

@users.route("/admin")
@login_required
def admin_dashboard():
    if current_user.is_admin:
        users = User.query.all()
        return render_template('admin.html', users=users, title='Admin Dashboard')
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))
