from flask import Flask


def create_app():
    app = Flask(__name__) #nombre del archivo flask
    app.config['SECRET_KEY'] = 'elchicolisto'

    from .views import views # importe blueprint
    from .auth import auth #importe blueprint

    app.register_blueprint(views, url_prefix='/') # Registro blueprint en flask app
    app.register_blueprint(auth, url_prefix='/') # Registro blueprint en flask app

    return app

