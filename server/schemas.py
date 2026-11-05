
from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    validates_schema,
    ValidationError
)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(r".*\S.*", error="Workout name cannot be blank.")
        ]
    )

    date = fields.Date(required=False)

    notes = fields.Str(
        load_default="",
        validate=validate.Length(max=500)
    )

    exercises = fields.List(
        fields.Dict(),
        dump_only=True
    )

    @validates("name")
    def validate_workout_name(self, value, **kwargs):
        if value.strip() != value:
            raise ValidationError(
                "Remove leading or trailing spaces from workout name."
            )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100),
            validate.Regexp(r".*\S.*", error="Exercise name cannot be blank.")
        ]
    )

    description = fields.Str(
        load_default="",
        validate=validate.Length(max=500)
    )

    difficulty = fields.Str(
        load_default="beginner",
        validate=validate.OneOf(
            ["beginner", "intermediate", "advanced"]
        )
    )

    @validates("name")
    def validate_exercise_name(self, value, **kwargs):
        if value.strip() != value:
            raise ValidationError(
                "Remove leading or trailing spaces from exercise name."
            )


class AddExerciseSchema(Schema):
    exercise_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        load_default=1,
        validate=validate.Range(min=1)
    )

    reps = fields.Int(
        load_default=None,
        allow_none=True,
        validate=validate.Range(min=1)
    )

    duration = fields.Int(
        load_default=None,
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration") is None:
            raise ValidationError(
                "Provide either reps or duration."
            )


class WorkoutResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    date = fields.Date()
    notes = fields.Str()
    exercises = fields.List(fields.Dict())


class ExerciseResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    difficulty = fields.Str()
