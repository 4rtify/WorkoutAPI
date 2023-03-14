from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemes import ExercisesSchema, ExerciseUpdateSchema
from models import ExerciseModel, TagModel

blp = Blueprint("Exercise", __name__, description="Operations on Exercises")


@blp.route("/exercise")
class ExercisesList(MethodView):
    @blp.response(200, ExercisesSchema(many=True))
    def get(self):
        return ExerciseModel.query.all()

    @blp.arguments(ExerciseUpdateSchema)
    @blp.response(201, ExercisesSchema)
    def post(self, exercise_data):
        exercise = ExerciseModel(name=exercise_data["name"])
        if exercise_data.get("tags"):
            tags = [TagModel.query.get_or_404(tag) for tag in exercise_data["tags"]]
            exercise.tags = tags
        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))

        return exercise


@blp.route("/exercise/<string:exercise_id>")
class Exercises(MethodView):
    @blp.response(200, ExercisesSchema)
    def get(self, exercise_id):
        exercise = ExerciseModel.query.get_or_404(exercise_id)
        return exercise

    @blp.arguments(ExerciseUpdateSchema)
    @blp.response(200, ExercisesSchema)
    def put(self, exercise_data, exercise_id):
        exercise = ExerciseModel.query.get_or_404(exercise_id)
        tags = [TagModel.query.get_or_404(tag) for tag in exercise_data["tags"]]

        if exercise:
            exercise.name = exercise_data["name"]
            exercise.tags = tags
        else:
            exercise = ExerciseModel(id=exercise_id, **exercise_data)

        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return exercise

    @blp.response(200)
    def delete(self, exercise_id):
        exercise = ExerciseModel.query.get_or_404(exercise_id)

        try:
            db.session.delete(exercise)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Exercise Deleted"}
