from datetime import datetime
from app import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import pytz

Base = declarative_base()

class Galleries (db.Model, Base):
    __tablename__ = 'galleries'

    id_gallery = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = db.Column(db.String(36))
    title = db.Column(db.String(255))
    main_caption = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))

    id_gallery_img = relationship('Galleries_img', backref='Galleries', lazy=True)

class Galleries_img(db.Model, Base):
    __tablename__ = 'galleries_img'

    id_gallery_img = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_gallery = db.Column(db.String(36), db.ForeignKey('galleries.id_gallery'))
    file_name = db.Column(db.String(128))
    caption = db.Column(db.Text)
    file_type = db.Column(db.Text)
    is_main_img = db.Column(db.Integer)