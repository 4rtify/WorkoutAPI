from db import db


class ExerciseTagsModel(db.Model):
    __tablename__ = "exercise_tags"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
