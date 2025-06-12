# bmi_package/bmi_functions.py

def calculate_bmi(weight, height):
    """Calculate BMI using the formula: weight (kg) / height (cm^2)."""
    return weight / ((height/100) ** 2)

def bmi_category(bmi):
    """Determine the BMI category based on the BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"
