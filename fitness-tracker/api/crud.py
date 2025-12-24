import sqlite3

def get_user_by_username(db: sqlite3.Connection, username: str):
    """Fetch a user from the DB by their username."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def create_user(db: sqlite3.Connection, user):
    """Inserts a new user into the database with full profile details."""
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO users (username, password_hash, age, height, weight, gender, goal) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            user.username, 
            user.password_hash, 
            user.age, 
            user.height, 
            user.weight, 
            user.gender, 
            user.goal
        )
    )
    db.commit()
    # Fetch and return the newly created user to confirm success
    return get_user_by_username(db, user.username)

def create_workout(db: sqlite3.Connection, user_id: int, workout):
    """Logs a workout session for a specific user."""
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO workouts (user_id, date, exercise_name, sets, reps, weight, duration_minutes, intensity) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id, workout.date, workout.exercise_name, workout.sets, 
            workout.reps, workout.weight, workout.duration_minutes, workout.intensity
        )
    )
    db.commit()
    workout_id = cursor.lastrowid
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
    return cursor.fetchone()

def get_workouts_by_user(db: sqlite3.Connection, user_id: int):
    """Retrieves all historical workouts for a user."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC", (user_id,))
    return cursor.fetchall()