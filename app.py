import os

from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.workout_log import blp as WorkoutLogBlp
from resources.exercise import blp as ExercisesBlp
from resources.workout_activities import blp as ActivitiesBlp
from resources.tags import blp as TagsBlp


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Workout Tracker REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/doc"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(WorkoutLogBlp)
    api.register_blueprint(ExercisesBlp)
    api.register_blueprint(ActivitiesBlp)
    api.register_blueprint(TagsBlp)

    return app
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
