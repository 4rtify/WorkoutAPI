from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import WorkoutActivitiesModel, WorkoutLogModel
from schemes import WorkoutActivitiesSchema, WorkoutActivitiesUpdateSchema, WorkoutActivityAddSchema

blp = Blueprint("WorkoutActivities", __name__, description="Operation on activities")


@blp.route("/activities")
class ActivitiesList(MethodView):
    @blp.response(200, WorkoutActivitiesSchema(many=True))
    def get(self):
        return WorkoutActivitiesModel.query.all()

    @blp.arguments(WorkoutActivitiesSchema)
    @blp.response(201, WorkoutActivitiesSchema)
    def post(self, activity_data):
        activity = WorkoutActivitiesModel(**activity_data)

        try:
            db.session.add(activity)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return activity


@blp.route("/activities/<string:activity_id>")
class Activities(MethodView):
    @blp.response(200, WorkoutActivitiesSchema)
    def get(self, activity_id):
        activity = WorkoutActivitiesModel.query.get_or_404(activity_id)
        return activity

    @blp.arguments(WorkoutActivitiesUpdateSchema)
    @blp.response(202, WorkoutActivitiesSchema)
    def put(self, activity_data, activity_id):
        activity = WorkoutActivitiesModel.query.get_or_404(activity_id)
        if activity:
            activity.exercise_id = activity_data["exercise_id"]
            activity.set_num = activity_data["set_num"]
            activity.reps_num = activity_data["reps_num"]
            activity.rest_time = activity_data["rest_time"]
            activity.rpe = activity_data["rpe"]
        else:
            activity = WorkoutActivitiesModel(id=activity_id, **activity_data)
        try:
            db.session.add(activity)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return activity

    @blp.response(200)
    def delete(self, activity_id):
        activity = WorkoutActivitiesModel.query.get_or_404(activity_id)

        try:
            db.session.delete(activity)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Activity deleted"}


@blp.route("/log/<int:workout_session_id>/activities")
class ActivitiesByLogId(MethodView):
    @blp.response(200, WorkoutActivitiesSchema(many=True))
    def get(self, workout_session_id):
        log = WorkoutLogModel.query.get_or_404(workout_session_id)
        return log.activities

    @blp.arguments(WorkoutActivityAddSchema)
    @blp.response(201, WorkoutActivitiesSchema)
    def post(self, activity_data, workout_session_id):
        activity = WorkoutActivitiesModel(workout_session_id=workout_session_id, **activity_data)

        try:
            db.session.add(activity)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return activity
