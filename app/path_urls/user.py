from app import api
from app.controllers.user import *

def UserAuthentication_Api_Path():
    api.add_resource(RegisterResource, "/api/v1/bpi/resource/register")
    api.add_resource(LoginResource, "/api/v1/bpi/resource/login")