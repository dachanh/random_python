from flask import Flask 
from server_flask.controllers.api.testapi import testapi
from server_flask.factories.configuration import Config 


def create_application()-> Flask:
    app =  Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(testapi)
    return app