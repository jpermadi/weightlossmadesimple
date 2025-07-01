from flask import Flask, render_template, request

app = Flask(__name__)

class BMI:
    def __init__(self, weight_kg, height_cm):
        self.lower_limit_bmi = 18.5
        self.upper_limit_bmi = 25

        self.weight = weight_kg
        self.height_cm = height_cm
        self.height_m = height_cm / 100
        self.bmi = self.get_bmi()

    def get_bmi(self):
        try:
            return round(self.weight / (self.height_m ** 2), 2)
        except ZeroDivisionError:
            return 0
    
    def get_category(self):
        if self.bmi < self.lower_limit_bmi:
            return "Underweight"
        elif self.lower_limit_bmi <= self.bmi < self.upper_limit_bmi:
            return "Normal weight"
        elif self.upper_limit_bmi <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_upper_limit_kg(self):
        limit_kg = self.upper_limit_bmi * (self.height_m ** 2)
        return round(limit_kg, 2)

    def get_lower_limit_kg(self):
        limit_kg = self.lower_limit_bmi * (self.height_m ** 2)
        return round(limit_kg, 2)
    
    def get_diff_kg(self):
        if self.bmi < self.lower_limit_bmi:
            return round(self.get_lower_limit_kg() - self.weight, 2)
        elif self.bmi > self.upper_limit_bmi:
            return round(self.weight - self.get_upper_limit_kg(), 2)
        else:
            return 0
        

@app.route("/", methods=["GET", "POST"])
def index():
    context ={
        "result" : None,
        "suggestion" : None,
        "suggested_weight" : None 
    }

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            
            bmi_obj = BMI(weight, height)
            context["result"] = f"Your BMI is {bmi_obj.bmi} ({bmi_obj.get_category()})"
            context["suggested_weight"] = f"Your ideal weight range is {bmi_obj.get_lower_limit_kg()} - {bmi_obj.get_upper_limit_kg()} kg"
            
            if bmi_obj.get_category() == "Underweight":
                context["suggestion"] = f"You need to gain at least {bmi_obj.get_diff_kg()} kg"
            elif bmi_obj.get_category() == "Normal weight":
                context["suggestion"] = f"You are in a healthy weight range"
            elif bmi_obj.get_category() in ("Overweight", "Obese"):
                context["suggestion"] = f"You need to lose at least {bmi_obj.get_diff_kg()} kg"

        except ValueError:
            result = "Invalid input. Please enter numbers only."
        
    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)

