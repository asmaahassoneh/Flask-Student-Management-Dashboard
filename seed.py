from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    admin_email = "admin@gmail.com"
    admin_password = "Admin123"

    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = User(
            username="admin",
            email=admin_email,
            is_admin=True,
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()

    print("Seed completed successfully.")
