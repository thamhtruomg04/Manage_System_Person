from app import create_app, db
from app.models import User, Employee
from app.users.routes import users  # Đảm bảo bạn đang import đúng từ app.users

app = create_app()

# Đăng ký blueprint tại đây với tên duy nhất
app.register_blueprint(users, url_prefix='/users', name='users_bp')

if __name__ == '__main__':
    app.run(debug=True)
