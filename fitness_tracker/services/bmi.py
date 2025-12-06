def calculate_bmi(weight: float, height: float) -> float:
    if height <= 0:
        raise ValueError("Height must be positive")
    return round(weight / (height ** 2), 2)

def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"
