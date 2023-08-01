from flask import request, jsonify
from flask_restful import Resource
from app import db
from datetime import datetime
import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.controllers import encrypt, decrypt
from app.models.user import Users

class Login(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        value = Users.query.filter_by(user_id=user_id).first()
        return jsonify(
            username=decrypt(value.username),
            email=decrypt(value.email)
        )

    def post(self):

        # Validasi data
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return {
                "status": 400,
                "message": "Formulir tidak boleh kosong"
            }
        
        # Proses autentikasi
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(days=1))
            
            return {
                "status": 200,
                "message": "Kamu berhasil masuk",
                "token": token,
                "data": {
                    "username": decrypt(user.username)
                }
            }

        else:
            return {
                "status": 401,
                "message": "Username atau Password salah"
            }


class Register(Resource):
    def post(self):
        # fetch data
        ###########################################################
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        ###########################################################

        # data validation
        if not username or not password:
            return {
                "status": 400,
                "message": "Formulir tidak boleh kosong"
            }
        elif len(password) <= 5:
            return {
                "status": 400,
                "message": "Password harus memiliki setidaknya 5 digit karakter"
            }
        else:
            values = Users(username=encrypt(username), password=generate_password_hash(password))

            # handler if username already use
            try:
                db.session.add(values) 
                db.session.commit()
                token = create_access_token(identity=values.user_id, expires_delta=datetime.timedelta(days=1))
            except IntegrityError:
                db.session.rollback()
                return {
                    "status": 400,
                    "message": "Username sudah digunakan atau tidak tersedia"
                }

            return jsonify({
                "message": "Registrasi Berhasil",
                "status": 200,
                "token":token,
                "data": {
                    "user_id": values.user_id,
                    "username": decrypt(values.username)
                }
            })