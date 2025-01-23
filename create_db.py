from app import create_app, db
from app.models import User, Agreement, Room, Message

app = create_app()

def create_database():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == '__main__':
    create_database()