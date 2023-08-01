from flask_login import UserMixin
from app import db
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(db.Model, UserMixin, Base):
    __tablename__ = 'users'

    id_user = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(36), unique=True)
    password = db.Column(db.String(36))

    def get_id(self):
        return str(self.id_user)