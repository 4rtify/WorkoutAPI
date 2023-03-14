from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    workout = db.relationship("WorkoutLogModel", back_populates="tag")
    exercise = db.relationship("ExerciseModel", back_populates="tags", secondary="exercise_tags")
