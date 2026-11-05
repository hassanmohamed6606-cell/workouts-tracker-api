
from datetime import date

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from server.extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_workout_name_not_empty"
        ),
        CheckConstraint(
            "length(name) <= 100",
            name="check_workout_name_length"
        ),
        CheckConstraint(
            "length(notes) <= 500",
            name="check_workout_notes_length"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.String(500), nullable=False, default="")

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValueError("Workout name cannot exceed 100 characters.")
        return value.strip()

    @validates("notes")
    def validate_notes(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Workout notes must be text.")
        if len(value) > 500:
            raise ValueError("Workout notes cannot exceed 500 characters.")
        return value

    def to_dict(self, include_exercises=True):
        result = {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat(),
            "notes": self.notes,
        }

        if include_exercises:
            result["exercises"] = [
                item.to_dict()
                for item in self.workout_exercises
            ]

        return result


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_exercise_name_not_empty"
        ),
        CheckConstraint(
            "length(name) <= 100",
            name="check_exercise_name_length"
        ),
        CheckConstraint(
            "difficulty IN ('beginner', 'intermediate', 'advanced')",
            name="check_exercise_difficulty"
        ),
        UniqueConstraint("name", name="unique_exercise_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    difficulty = db.Column(
        db.String(20),
        nullable=False,
        default="beginner"
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Description must be text.")
        if len(value) > 500:
            raise ValueError("Description cannot exceed 500 characters.")
        return value

    @validates("difficulty")
    def validate_difficulty(self, key, value):
        allowed = {"beginner", "intermediate", "advanced"}
        if value not in allowed:
            raise ValueError(
                "Difficulty must be beginner, intermediate, or advanced."
            )
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
        }


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_exercise_per_workout"
        ),
        CheckConstraint("sets > 0", name="check_sets_positive"),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_reps_positive"
        ),
        CheckConstraint(
            "duration IS NULL OR duration > 0",
            name="check_duration_positive"
        ),
        CheckConstraint(
            "reps IS NOT NULL OR duration IS NOT NULL",
            name="check_reps_or_duration_required"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False
    )

    sets = db.Column(db.Integer, nullable=False, default=1)
    reps = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("Sets must be a positive integer.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError("Reps must be a positive integer.")
        return value

    @validates("duration")
    def validate_duration(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError("Duration must be a positive integer.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            "exercise": self.exercise.to_dict(),
            "sets": self.sets,
            "reps": self.reps,
            "duration": self.duration,
        }
