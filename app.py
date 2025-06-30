from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height):
    height_m = height / 100  # cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def assess_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def calculate_upper_limit_kg(height):
    upper_limit = 24.9
    height_m = height / 100  # cm to meters
    weight = upper_limit * (height_m ** 2)
    return round(weight, 2)


def calculate_lower_limit_kg(height):
    lower_limit = 18.5
    height_m = height / 100  # cm to meters
    weight = lower_limit * (height_m ** 2)
    return round(weight, 2)

def calculate_weight_diff(weight, limit):
    return round(abs(limit - weight),2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestion = None
    suggested_weight = None

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            bmi = calculate_bmi(weight, height)
            category = assess_bmi(bmi)
            upper_limit_weight = calculate_upper_limit_kg(height)
            lower_limit_weight = calculate_lower_limit_kg(height)
            

            result = f"Your BMI is {bmi} ({category})"
            suggested_weight = f"Your ideal weight range is {lower_limit_weight} - {upper_limit_weight} kg"

            if bmi < 18.5:
                weight_diff = calculate_weight_diff(weight, lower_limit_weight)
                suggestion = f"You need to gain at least {weight_diff} kg"
            elif bmi > 24.9:
                weight_diff = calculate_weight_diff(weight, upper_limit_weight)
                suggestion = f"You need to lose at least {weight_diff} kg"
            else:
                suggestion = f"You are in a healthy weight range"   
        
        except ValueError:
            result = "Invalid input. Please enter numbers only."
    return render_template("index.html", result=result, suggested_weight=suggested_weight, suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)

