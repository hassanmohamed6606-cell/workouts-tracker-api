# workouts-tracker-api
A Flask REST API for managing workouts and reusable exercises

The application allows personal trainers to create and manage workouts and reusable exercises. Each workout can contain multiple exercises, with individual sets, repetitions, or duration assigned to each exercise.

## Technologies Used

- Python 3.12
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- SQLAlchemy
- Marshmallow 3.20.1
- SQLite
- Pipenv

## Project Structure

```text
workout-tracker-api/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── extensions.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── migrations/
├── tests/
│   └── test_app.py
├── instance/
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/hassanmohamed6606-cell/workouts-tracker-api.git
cd workouts-tracker-api
```

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialize Flask migrations:

```bash
flask --app server:create_app db init
```

Generate the initial migration:

```bash
flask --app server:create_app db migrate -m "Initial database migration"
```

Apply the migration:

```bash
flask --app server:create_app db upgrade
```

Seed the database:

```bash
python -m server.seed
```

## Running the Application

Start the Flask development server:

```bash
flask --app server:create_app run
```

The API will be available at:

http://127.0.0.1:5000

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | /workouts | View all workouts |
| POST | /workouts | Create a workout |
| GET | /workouts/id | View one workout |
| DELETE | /workouts/id | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | /exercises | View all exercises |
| POST | /exercises | Create an exercise |
| GET | /exercises/id | View one exercise |
| DELETE | /exercises/id | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | /workouts/id/exercises | Add an exercise to a workout |

## Example Requests

### Create a Workout

POST /workouts

```json
{
    "name": "Full Body Workout",
    "notes": "Strength training session"
}
```

### Create an Exercise

POST /exercises

```json
{
    "name": "Push-ups",
    "description": "Upper body exercise",
    "difficulty": "beginner"
}
```

### Add an Exercise to a Workout

POST /workouts/1/exercises

```json
{
    "exercise_id": 1,
    "sets": 3,
    "reps": 12
}
```

For a timed exercise, use:

```json
{
    "exercise_id": 2,
    "sets": 3,
    "duration": 60
}
```

Duration is measured in seconds.

## Validations and Constraints

The application includes:

- Non-empty workout names.
- Non-empty exercise names.
- Unique exercise names.
- Valid exercise difficulty levels.
- Positive sets, repetitions, and duration.
- Unique exercise-workout combinations.
- Required repetitions or duration when adding exercises.
- Marshmallow request validation.
- SQLAlchemy model validation.
- Database-level check and unique constraints.

## Relationships

The application uses a many-to-many relationship between workouts and exercises through the WorkoutExercise association model.

The association model stores sets, repetitions, and duration for each exercise in a particular workout.

## Running Tests

Run:

```bash
python -m unittest discover -s tests -v
```

## Author

Hassan Mohamed

## License

This project was created for educational purposes as part of a Flask backend development summative lab.