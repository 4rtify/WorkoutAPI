from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import WorkoutLogModel
from schemes import WorkoutLogSchema

blp = Blueprint("WorkoutLog", __name__, description="Operations on Workout Logs")


@blp.route("/log/<string:log_id>")
class Log(MethodView):
    @blp.response(200, WorkoutLogSchema)
    def get(self, log_id):
        log = WorkoutLogModel.query.get_or_404(log_id)
        return log

    @blp.arguments(WorkoutLogSchema)
    @blp.response(201, WorkoutLogSchema)
    def put(self, log_data, log_id):
        log = WorkoutLogModel.query.get_or_404(log_id)

        if log:
            log.started_at = log_data["started_at"]
            log.ended_at = log_data["ended_at"]
            log.tag_id = log_data["tag_id"]
        else:
            log = WorkoutLogModel(**log_data, id=log_id)

        try:
            db.session.add(log)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return log

    @blp.response(200)
    def delete(self, log_id):
        log = WorkoutLogModel.query.get_or_404(log_id)

        try:
            db.session.delete(log)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        return {"message": "Deleted"}


@blp.route("/log")
class LogList(MethodView):
    @blp.response(200, WorkoutLogSchema(many=True))
    def get(self):
        return WorkoutLogModel.query.all()

    @blp.arguments(WorkoutLogSchema)
    @blp.response(201, WorkoutLogSchema)
    def post(self, log_data):
        log = WorkoutLogModel(**log_data)

        try:
            db.session.add(log)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return log

