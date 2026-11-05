
import unittest

from server import create_app
from server.extensions import db
from server.models import Workout, Exercise


class WorkoutAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_workout(self):
        response = self.client.post(
            "/workouts",
            json={"name": "Morning Workout"}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json["name"],
            "Morning Workout"
        )

    def test_reject_empty_workout_name(self):
        response = self.client.post(
            "/workouts",
            json={"name": ""}
        )

        self.assertEqual(response.status_code, 400)

    def test_create_exercise(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Push-ups",
                "description": "Upper body exercise",
                "difficulty": "beginner"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Push-ups")

    def test_reject_invalid_difficulty(self):
        response = self.client.post(
            "/exercises",
            json={
                "name": "Push-ups",
                "difficulty": "expert"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_add_exercise_to_workout(self):
        workout_response = self.client.post(
            "/workouts",
            json={"name": "Strength Training"}
        )

        exercise_response = self.client.post(
            "/exercises",
            json={"name": "Squats"}
        )

        workout_id = workout_response.json["id"]
        exercise_id = exercise_response.json["id"]

        response = self.client.post(
            f"/workouts/{workout_id}/exercises",
            json={
                "exercise_id": exercise_id,
                "sets": 3,
                "reps": 12
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["sets"], 3)
        self.assertEqual(response.json["reps"], 12)

    def test_reject_duplicate_exercise(self):
        workout = self.client.post(
            "/workouts",
            json={"name": "Workout"}
        ).json

        exercise = self.client.post(
            "/exercises",
            json={"name": "Plank"}
        ).json

        payload = {
            "exercise_id": exercise["id"],
            "sets": 3,
            "duration": 30
        }

        self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json=payload
        )

        response = self.client.post(
            f"/workouts/{workout['id']}/exercises",
            json=payload
        )

        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
