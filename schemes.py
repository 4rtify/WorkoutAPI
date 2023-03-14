from marshmallow import Schema, fields


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainExercisesSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainWorkoutLogSchema(Schema):
    id = fields.Int(dump_only=True)
    started_at = fields.DateTime(required=True)
    ended_at = fields.DateTime(required=True)
    tag_id = fields.Int(load_only=True)


class PlainWorkoutActivitiesSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_session_id = fields.Int(required=True, load_only=True)
    exercise_id = fields.Int(required=True, load_only=True)
    set_num = fields.Int(required=True)
    reps_num = fields.Int(required=True)
    rest_time = fields.Float()
    rpe = fields.Int()


class WorkoutLogSchema(PlainWorkoutLogSchema):
    activities = fields.List(fields.Nested(PlainWorkoutActivitiesSchema()), dump_only=True)
    tag = fields.Nested(PlainTagSchema())


class WorkoutActivitiesUpdateSchema(PlainWorkoutActivitiesSchema):
    workout_session_id = fields.Int()
    exercise_id = fields.Int()
    set_num = fields.Int()
    reps_num = fields.Int()
    rest_time = fields.Float()
    rpe = fields.Int()


class WorkoutActivityAddSchema(PlainWorkoutActivitiesSchema):
    workout_session_id = fields.Int(load_only=True)


class TagSchema(PlainTagSchema):
    workout = fields.List(fields.Nested(PlainWorkoutLogSchema()), dump_only=True)
    exercise = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ExercisesSchema(PlainExercisesSchema):
    tags = fields.List(fields.Nested(TagSchema()), dump_only=True)


class WorkoutActivitiesSchema(PlainWorkoutActivitiesSchema):
    workout = fields.Nested(WorkoutLogSchema())
    exercise = fields.Nested(ExercisesSchema())


class WorkoutLogUpdateTagSchema(Schema):
    tag_id = fields.Int()
