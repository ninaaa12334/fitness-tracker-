from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    height: float
    weight: float
