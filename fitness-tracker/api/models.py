from pydantic import BaseModel
from typing import Optional

# --- User Models ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    age: Optional[int] = None
    height: Optional[float] = None # in cm
    weight: Optional[float] = None # in kg
    gender: Optional[str] = None
    goal: Optional[str] = None

class UserOut(UserBase):
    id: int
    age: Optional[int]
    height: Optional[float]
    weight: Optional[float]
    gender: Optional[str]
    goal: Optional[str]
    class Config:
        orm_mode = True # Compatibility with ORMs/DBs

# --- Workout Models ---
class WorkoutBase(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    weight: float
    duration_minutes: float
    intensity: str

class WorkoutCreate(WorkoutBase):
    date: str # YYYY-MM-DD format

class WorkoutOut(WorkoutCreate):
    id: int
    user_id: int
    class Config:
        orm_mode = True