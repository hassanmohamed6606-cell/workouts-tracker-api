
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise
from server.schemas import (
    WorkoutSchema,
    ExerciseSchema,
    AddExerciseSchema,
)

workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
add_exercise_schema = AddExerciseSchema()


def register_routes(app):

    # HOME
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Welcome to the Workout Tracker API",
            "endpoints": {
                "workouts": "/workouts",
                "exercises": "/exercises",
                "add_exercise": "/workouts/<workout_id>/exercises"
            }
        }), 200

    # WORKOUT ENDPOINTS

    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.order_by(Workout.id).all()

        return jsonify([
            workout.to_dict() for workout in workouts
        ]), 200

    @app.route("/workouts", methods=["POST"])
    def create_workout():
        try:
            data = workout_schema.load(request.get_json() or {})

            workout = Workout(**data)

            db.session.add(workout)
            db.session.commit()

            return jsonify(workout.to_dict()), 201

        except ValidationError as error:
            return jsonify({"errors": error.messages}), 400

        except ValueError as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 400

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Invalid workout data."}), 400

    @app.route("/workouts/<int:workout_id>", methods=["GET"])
    def get_workout(workout_id):
        workout = db.session.get(Workout, workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        return jsonify(workout.to_dict()), 200

    @app.route("/workouts/<int:workout_id>", methods=["DELETE"])
    def delete_workout(workout_id):
        workout = db.session.get(Workout, workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        db.session.delete(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout deleted successfully."
        }), 200

    # EXERCISE ENDPOINTS

    @app.route("/exercises", methods=["GET"])
    def get_exercises():
        exercises = Exercise.query.order_by(Exercise.id).all()

        return jsonify([
            exercise.to_dict() for exercise in exercises
        ]), 200

    @app.route("/exercises", methods=["POST"])
    def create_exercise():
        try:
            data = exercise_schema.load(request.get_json() or {})

            exercise = Exercise(**data)

            db.session.add(exercise)
            db.session.commit()

            return jsonify(exercise.to_dict()), 201

        except ValidationError as error:
            return jsonify({"errors": error.messages}), 400

        except ValueError as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 400

        except IntegrityError:
            db.session.rollback()
            return jsonify({
                "error": "Exercise already exists or violates a database constraint."
            }), 400

    @app.route("/exercises/<int:exercise_id>", methods=["GET"])
    def get_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)

        if not exercise:
            return jsonify({"error": "Exercise not found."}), 404

        return jsonify(exercise.to_dict()), 200

    @app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
    def delete_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)

        if not exercise:
            return jsonify({"error": "Exercise not found."}), 404

        db.session.delete(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully."
        }), 200

    # ADD EXERCISE TO WORKOUT

    @app.route(
        "/workouts/<int:workout_id>/exercises",
        methods=["POST"]
    )
    def add_exercise_to_workout(workout_id):
        workout = db.session.get(Workout, workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        try:
            data = add_exercise_schema.load(request.get_json() or {})

            exercise = db.session.get(
                Exercise,
                data["exercise_id"]
            )

            if not exercise:
                return jsonify({"error": "Exercise not found."}), 404

            existing = WorkoutExercise.query.filter_by(
                workout_id=workout_id,
                exercise_id=exercise.id
            ).first()

            if existing:
                return jsonify({
                    "error": "This exercise is already in the workout."
                }), 409

            workout_exercise = WorkoutExercise(
                workout_id=workout_id,
                exercise_id=exercise.id,
                sets=data["sets"],
                reps=data["reps"],
                duration=data["duration"]
            )

            db.session.add(workout_exercise)
            db.session.commit()

            return jsonify(workout_exercise.to_dict()), 201

        except ValidationError as error:
            return jsonify({"errors": error.messages}), 400

        except ValueError as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 400

        except IntegrityError:
            db.session.rollback()
            return jsonify({
                "error": "Could not add exercise to workout."
            }), 400
