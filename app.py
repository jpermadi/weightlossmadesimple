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

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            bmi = calculate_bmi(weight, height)
            category = assess_bmi(bmi)
            result = f"Your BMI is {bmi} ({category})"
        except ValueError:
            result = "Invalid input. Please enter numbers only."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

