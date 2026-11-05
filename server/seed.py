
from server import create_app
from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise


app = create_app()


def seed_database():
    with app.app_context():
        db.create_all()

        # Prevent duplicate seed data.
        if Workout.query.first() or Exercise.query.first():
            print("Database already contains data. Skipping seed.")
            return

        # Create exercises.
        pushups = Exercise(
            name="Push-ups",
            description="Upper body bodyweight exercise.",
            difficulty="beginner"
        )

        squats = Exercise(
            name="Squats",
            description="Lower body strength exercise.",
            difficulty="beginner"
        )

        plank = Exercise(
            name="Plank",
            description="Core stability exercise.",
            difficulty="intermediate"
        )

        running = Exercise(
            name="Running",
            description="Cardiovascular endurance exercise.",
            difficulty="beginner"
        )

        db.session.add_all([
            pushups,
            squats,
            plank,
            running
        ])

        db.session.flush()

        # Create workouts.
        workout1 = Workout(
            name="Full Body Workout",
            notes="Complete full body strength training."
        )

        workout2 = Workout(
            name="Cardio and Core",
            notes="Improve endurance and core strength."
        )

        db.session.add_all([workout1, workout2])
        db.session.flush()

        # Associate exercises with workouts.
        db.session.add_all([
            WorkoutExercise(
                workout=workout1,
                exercise=pushups,
                sets=3,
                reps=12
            ),
            WorkoutExercise(
                workout=workout1,
                exercise=squats,
                sets=3,
                reps=15
            ),
            WorkoutExercise(
                workout=workout2,
                exercise=plank,
                sets=3,
                duration=60
            ),
            WorkoutExercise(
                workout=workout2,
                exercise=running,
                sets=1,
                duration=1200
            )
        ])

        db.session.commit()

        print("Database seeded successfully!")
        print("Created 2 workouts.")
        print("Created 4 exercises.")
        print("Created 4 workout-exercise relationships.")


if __name__ == "__main__":
    seed_database()
