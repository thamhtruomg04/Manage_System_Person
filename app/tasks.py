from app import create_app
from app.celery import celery

@celery.task
def send_reminder_notification(to, subject, body):
    app = create_app()
    with app.app_context():
        # Thực hiện một tác vụ khác thay vì gửi email
        print(f"Gửi thông báo đến {to} với tiêu đề '{subject}' và nội dung '{body}'")
