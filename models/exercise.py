from db import db


class ExerciseModel(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    workout = db.relationship("WorkoutActivitiesModel", back_populates="exercise")
    tags = db.relationship("TagModel", back_populates="exercise", secondary="exercise_tags")
