from flask import request, jsonify
from flask_restful import Resource
from app import db
from datetime import datetime
import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.controllers import Encrypt, Decrypt
from app.controllers.message import *
from app.models.user import Users

class LoginResource(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        value = Users.query.filter_by(id_user=user_id).first()
        return {
            "status": 200,
            "message": "OK",
            "Data": {
                "username": Decrypt(value.username)
            }
        }, 200

    def post(self):

        # Validasi data
        #############################################################
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        #############################################################

        if not username or not password:
            return {
                "status": 400,
                "message": NotForm()
            }, 400
        
        # Proses autentikasi
        user = Users.query.filter_by(username=Encrypt(username)).first()

        if user and check_password_hash(user.password, password):
            token = create_access_token(identity=user.id_user, expires_delta=datetime.timedelta(days=1))
            
            return {
                "status": 202,
                "message": "Kamu berhasil masuk",
                "token": token,
                "data": {
                    "username": Decrypt(user.username)
                }
            }, 202

        else:
            return {
                "status": 401,
                "message": "Username atau Password salah"
            }, 401


class RegisterResource(Resource):
    def post(self):
        # fetch data
        ###########################################################
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        token = request.json.get('token', None)
        ###########################################################

        # data validation
        if not username or not password:
            return {
                "status": 400,
                "message": NotForm()
            }, 400
        elif len(password) <= 5:
            return {
                "status": 400,
                "message": "Password harus memiliki setidaknya 5 digit karakter"
            }, 400
        elif not token:
            return {
                "status": 400,
                "message": "Anda harus mengisi token"
            }, 400
        elif token != "bpinihbosss2023":
            return {
                "status": 400,
                "message": "Token yang anda masukan salah, silakan lakukan pengecekan kembali!"
            }, 400

        values = Users(username=Encrypt(username), password=generate_password_hash(password))

        # handler if username already use
        try:
            db.session.add(values) 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {
                "status": 400,
                "message": "Username sudah digunakan atau tidak tersedia"
            }, 400
        
        return {
            "status": 201,
            "message": "Registrasi Berhasil",
            "data": {
                "username": Decrypt(values.username)
            }
        }, 201