from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, ExerciseTagsModel, WorkoutLogModel
from schemes import TagSchema, WorkoutLogUpdateTagSchema

blp = Blueprint("Tags", __name__, description="Operation on Tags")


@blp.route("/tags")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        tag = TagModel(**tag_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/log/<string:log_id>/tag")
class LogTag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, log_id):
        log = WorkoutLogModel.query.get_or_404(log_id)
        return log.tag

    @blp.arguments(WorkoutLogUpdateTagSchema)
    @blp.response(202, TagSchema)
    def put(self, tag_data, log_id):
        tag = TagModel.query.get_or_404(tag_data["tag_id"])
        log = WorkoutLogModel.query.get_or_404(log_id)
        log.tag = tag

        try:
            db.session.add(log)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @blp.response(202)
    def delete(self, log_id):
        log = WorkoutLogModel.query.get_or_404(log_id)
        log.tag = None

        try:
            db.session.add(log)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Tag Removed"}
