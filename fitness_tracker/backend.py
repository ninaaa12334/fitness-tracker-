from fastapi import FastAPI
from .services import storage, bmi
from .services.user import User

app = FastAPI()

@app.on_event("startup")
def startup_event():
    storage.init_db()

@app.post("/users")
def create_user(user: User):
    conn = storage.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, age, height, weight) VALUES (?, ?, ?, ?)",
        (user.name, user.age, user.height, user.weight)
    )
    conn.commit()
    conn.close()
    return {"message": "User created"}

@app.post("/bmi/{user_id}")
def add_bmi(user_id: int):
    conn = storage.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT weight, height FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "User not found"}
    weight, height = row
    value = bmi.calculate_bmi(weight, height)
    cursor.execute("INSERT INTO bmi_history (user_id, bmi) VALUES (?, ?)", (user_id, value))
    conn.commit()
    conn.close()
    return {"bmi": value, "category": bmi.bmi_category(value)}
