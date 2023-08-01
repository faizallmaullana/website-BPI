from datetime import datetime
from app import db
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import pytz

from app.models import user

Base = declarative_base()


class Articles_bpi(db.Model, Base):
    __tablename__ = 'articles_bpi'

    id_article = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = db.Column(db.String(36))
    id_img = db.Column(db.String(36), db.ForeignKey('articles_img.id_article_img'))
    title = db.Column(db.String(255))
    author = db.Column(db.String(72))
    article = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    

class Articles_img(db.Model, Base):
    __tablename__ = 'articles_img'

    id_article_img = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    img = db.Column(db.Text)
    file_name = db.Column(db.String(128))
    caption = db.Column(db.Text)
    file_type = db.Column(db.Text)

    id_article = relationship('Articles_bpi', backref='Articles_img', lazy=True)