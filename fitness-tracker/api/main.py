from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import sqlite3

# --- FIXED IMPORTS ---
try:
    # Try importing as a package (standard for Uvicorn)
    from . import database, crud
    from .models import UserCreate, UserOut, WorkoutCreate, WorkoutOut
except ImportError:
    # Fallback for direct execution
    import database
    import crud
    from models import UserCreate, UserOut, WorkoutCreate, WorkoutOut

# --- Setup ---
app = FastAPI(title="FitTracker Pro API", version="1.0.0")

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    # This calls the init function without loading the whole module unnecessarily
    database.init_db()

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Backend is active!"}

# --- SIGNUP ROUTE (Matches Streamlit auth.py) ---
@app.post("/users/signup/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    db = database.get_db_connection()
    try:
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        user.password_hash = f"hashed_{user.password}"
        new_user = crud.create_user(db, user)
        return new_user
    finally:
        db.close()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import sqlite3
import sys
import os

# --- PATH FIX: Ensures Python sees the 'api' folder correctly ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- SAFE IMPORTS: Prevents Circular Import Errors ---
try:
    from api import database, crud
    from api.models import UserCreate, UserOut, WorkoutCreate, WorkoutOut
except ImportError:
    import database
    import crud
    from models import UserCreate, UserOut, WorkoutCreate, WorkoutOut

# --- Setup ---
app = FastAPI(title="FitTracker Pro API", version="1.0.0")

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    # This calls the init function without loading the whole module unnecessarily
    database.init_db()

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Backend is active!"}

# --- SIGNUP ROUTE (Matches Streamlit auth.py) ---
@app.post("/users/signup/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    db = database.get_db_connection()
    try:
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        user.password_hash = f"hashed_{user.password}"
        new_user = crud.create_user(db, user)
        return new_user
    finally:
        db.close()



class LoginCredentials(BaseModel):
    username: str
    password: str

# Updated route to include trailing slash for Streamlit compatibility
@app.post("/users/login/")
def login(creds: LoginCredentials):
    """Authenticates a user and returns their user data."""
    db = database.get_db_connection()
    try:
        user = crud.get_user_by_username(db, username=creds.username)
        
        # Simple verification against our mock hash
        if not user or user['password_hash'] != f"hashed_{creds.password}":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        return {
            "message": "Login successful", 
            "user_id": user['id'], 
            "username": user['username']
        }
    finally:
        db.close()

@app.post("/workouts/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def add_workout(user_id: int, workout: WorkoutCreate):
    """Logs a new workout for a user."""
    db = database.get_db_connection()
    try:
        new_workout = crud.create_workout(db, user_id, workout)
        return new_workout
    finally:
        db.close()

@app.get("/workouts/{user_id}", response_model=List[WorkoutOut])
def get_workouts(user_id: int):
    """Retrieves all workouts for a specific user."""
    db = database.get_db_connection()
    try:
        workouts = crud.get_workouts_by_user(db, user_id)
        return workouts
    finally:
        db.close()

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    # This ensures the database and tables exist when the server starts
    database.init_db()