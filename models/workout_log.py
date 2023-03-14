from db import db


class WorkoutLogModel(db.Model):
    __tablename__ = "workout_log"

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, unique=True, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    # Add relationship with workout.log and exercises
    activities = db.relationship("WorkoutActivitiesModel", back_populates="workout", cascade="all, delete")
    tag = db.relationship("TagModel", back_populates="workout")