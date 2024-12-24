# from app import create_app, db
# from app.models import User, Employee
# from app.users.routes import users  # Đảm bảo bạn đang import đúng từ app.users

# app = create_app()

# # Đăng ký blueprint tại đây với tên duy nhất
# app.register_blueprint(users, url_prefix='/users', name='users_bp')

# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app, db
from app.models import User, Employee
from app.users.routes import users  # Đảm bảo bạn đang import đúng từ app.users
from app.employees.routes import employees  # Import Blueprint employees

app = create_app()

# Đăng ký blueprint users tại đây với tên duy nhất
app.register_blueprint(users, url_prefix='/users', name='users_bp')

# Đăng ký blueprint employees tại đây
app.register_blueprint(employees, url_prefix='/employees', name='employees_bp')

if __name__ == '__main__':
    app.run(debug=True)
