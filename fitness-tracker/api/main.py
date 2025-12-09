from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import date
import sqlite3

# Import your database and models
from . import database, crud
from .models import UserCreate, UserOut, WorkoutCreate, WorkoutOut

# --- Setup ---
app = FastAPI(title="Fitness Tracker API")

# OAuth2 for simple token-based security (for future use/expansion)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

# --- Endpoints ---

@app.post("/users/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    """Creates a new user account."""
    db = database.get_db_connection()
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # NOTE: You must use a proper password hashing library (like bcrypt) in a real app.
    # For this example, we'll store a mock hash.
    user.password_hash = f"hashed_{user.password}"
    
    new_user = crud.create_user(db, user)
    return new_user

class LoginCredentials(BaseModel):
    username: str
    password: str

@app.post("/users/login")
def login(creds: LoginCredentials):
    """Authenticates a user and returns their user data."""
    db = database.get_db_connection()
    user = crud.get_user_by_username(db, username=creds.username)
    
    if not user or user.get('password_hash') != f"hashed_{creds.password}":
        # NOTE: In a real app, verify the hashed password.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return {"message": "Login successful", "user_id": user['id'], "username": user['username']}

@app.post("/workouts/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def add_workout(user_id: int, workout: WorkoutCreate):
    """Logs a new workout for a user."""
    db = database.get_db_connection()
    new_workout = crud.create_workout(db, user_id, workout)
    return new_workout

@app.get("/workouts/{user_id}", response_model=list[WorkoutOut])
def get_workouts(user_id: int):
    """Retrieves all workouts for a specific user."""
    db = database.get_db_connection()
    return crud.get_workouts_by_user(db, user_id)

# ... (Add endpoints for water, goals, etc. later)

# --- Startup/Shutdown Events (Optional but good practice) ---
@app.on_event("startup")
def startup_event():
    database.init_db()

# NOTE: The `crud.py` file is critical for database interaction.