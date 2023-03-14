from db import db


class WorkoutActivitiesModel(db.Model):
    __tablename__ = "workout_activities"

    id = db.Column(db.Integer, primary_key=True)
    workout_session_id = db.Column(db.Integer, db.ForeignKey("workout_log.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)
    set_num = db.Column(db.Integer, nullable=False)
    reps_num = db.Column(db.Integer, unique=False)
    rest_time = db.Column(db.Float(precision=2), unique=False)
    rpe = db.Column(db.Integer, unique=False)

    workout = db.relationship("WorkoutLogModel", back_populates="activities")
    exercise = db.relationship("ExerciseModel", back_populates="workout")