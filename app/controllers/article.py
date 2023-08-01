import uuid
from datetime import datetime
import pytz
from flask import Flask, session, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from app import db

from app.models.bpi_article import *
from app.controllers import *
from app.controllers.message import *

class ArtikelResource(Resource):
    @jwt_required()
    def post(self):
        if Access() == False:
            return {
                "status": 401,
                "message": NotAccess()
            }, 401
        
        ####################################################################
        title = request.json.get("title", None)
        author = request.json.get("author", "Anon")
        article = request.json.get("article", None)
        img = request.file("img", None)
        caption = request.json.get("caption", None)
        ####################################################################

        if not title or not article:
            return {
                "status": 400,
                "message": "Judul dan artikel harus diisi"
            }, 400

        if not img:
            return {
                "status": 400,
                "message": "Anda belum memasukan gambar"
            }, 400
        
        filename = img.filename
        mimetype = img.mimetype

        val_img = Articles_img(
            img=img.read(),
            filename=filename,
            caption=Encrypt(caption),
            file_type=mimetype
        )

        db.session.add(val_img)
        db.session.commit()

        val_article = Articles_bpi(
            id_user=get_jwt_identity(),
            id_img=val_img.id_article_img,
            title=Encrypt(title),
            author=Encrypt(author),
            article=Encrypt(article)
        )

        db.session.add(val_article)
        db.session.commit()

        return {
            "status": 201,
            "message": Created(),
            "data": {
                "article_bpi": {
                    "id_article": val_article.id_article,
                    "id_user": Decrypt(val_article.id_user),
                    "id_img": Decrypt(val_article.id_img),
                    "title": Decrypt(val_article.title),
                    "author": Decrypt(val_article.author),
                    "article": Decrypt(val_article.article),
                    "created_at": val_article.created_at
                },
                "article_img": {
                    "id_article_img": val_img.id_article_img,
                    "img": val_img.img,
                    "file_name": val_img.file_name,
                    "caption": Decrypt(val_img.caption),
                    "file_type": val_img.file_type
                }
            }
        }, 201
    

    @jwt_required()
    def put(self, get_id_article): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        val_article = Articles_bpi.query.filter_by(id_article=get_id_article).first()
        val_img = Articles_img.query.filter_by(id_article_img=val_article.id_img).first()

        ####################################################################
        title = request.json.get("title", Decrypt(val_article.title))
        author = request.json.get("author", Decrypt(val_article.author))
        article = request.json.get("article", Decrypt(val_article.article))
        img = request.file("img", val_img.img)
        caption = request.json.get("caption", Decrypt(val_img.catpion))
        ####################################################################

        val_img.img = img
        val_img.file_name = img.filename
        val_img.caption = Encrypt(caption)
        val_img.file_type = img.mimetype
    
        val_article.id_user = get_jwt_identity()
        val_article.id_img = val_img.id_article_img
        val_article.title = Encrypt(title)
        val_article.author = Encrypt(author)
        val_article.article = Encrypt(article)
        db.session.commit()

        return {
            "status": 201,
            "message": Created(),
            "data": {
                "article_bpi": {
                    "id_article": val_article.id_article,
                    "id_user": Decrypt(val_article.id_user),
                    "id_img": Decrypt(val_article.id_img),
                    "title": Decrypt(val_article.title),
                    "author": Decrypt(val_article.author),
                    "article": Decrypt(val_article.article),
                    "created_at": val_article.created_at
                },
                "article_img": {
                    "id_article_img": val_img.id_article_img,
                    "img": val_img.img,
                    "file_name": val_img.file_name,
                    "caption": Decrypt(val_img.caption),
                    "file_type": val_img.file_type
                }
            }
        }, 201


    def delete(self, get_id_article): ########################### ini isinya bukan bookkeeping account, tapi money bookkeeping id
        val_article = Articles_bpi.query.filter_by(id_article=get_id_article).first()
        val_img = Articles_img.query.filter_by(id_article_img=val_article.id_img).first()
        db.session.delete(val_img)
        db.session.delete(val_article)
        db.session.commit()

        return {
            "status": 201,
            "message": Deleted(),
            "data": {
                "title": Decrypt(val_article.title),
                "author": Decrypt(val_article.author)
            }
        }, 201