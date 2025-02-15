from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class ScrapeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    data_type = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=True)
    date_scraped = db.Column(db.DateTime, default=datetime.utcnow)

def create_tables(app):
    """Ensures tables are created within the Flask app context."""
    with app.app_context():
        db.create_all()
