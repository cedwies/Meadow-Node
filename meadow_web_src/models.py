from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from meadow_web.extensions import db, login_manager

class User(UserMixin, db.Model):
    # Primary key for our users table
    id = db.Column(db.Integer, primary_key=True)
    
    # Each user needs a unique username – required field
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Hashed password – no plain text madness here
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        # Use Werkzeug to hash the password before saving
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Compare incoming password with stored hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        # Helpful for debugging/logs, won't leak sensitive info
        return f'<User {self.username}>'
