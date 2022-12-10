from program_files import db
from sqlalchemy import DateTime
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    email = db.Column("Email", db.String(180), unique=True, nullable=False)
    password = db.Column("Password", db.String(100), nullable=False)


class Games(db.Model, UserMixin):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    game_outcome = db.Column("Win/Lose", db.String(10), nullable=False)
    user = db.relationship("User", lazy=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column("Date", DateTime, default=datetime.now())
