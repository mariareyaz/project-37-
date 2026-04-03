from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_risk(data):
    risk = 0
    drivers = []

    age = float(data['age'])
    gestation = float(data['gestation'])
    bp = float(data['bp'])
    temp = float(data['temp'])
    hb = float(data['hb'])
    wbc = float(data['wbc'])
    hr = float(data['hr'])
    crp = float(data['crp'])

    if age < 18 or age > 35:
        risk += 0.1
        drivers.append("High Risk Age")

    if gestation < 34:
        risk += 0.15
        drivers.append("Early Gestation")
    elif gestation < 37:
        risk += 0.1

    if hb < 10:
        risk += 0.15
        drivers.append("Low Hemoglobin")
    elif hb < 11:
        risk += 0.1

    if bp < 90:
        risk += 0.15
        drivers.append("Low BP")
    elif bp < 100:
        risk += 0.1

    if temp > 38:
        risk += 0.15
        drivers.append("High Temperature")
    elif temp > 37.5:
        risk += 0.1

    if hr > 110:
        risk += 0.1
        drivers.append("High Heart Rate")
    elif hr > 100:
        risk += 0.05

    if crp > 10:
        risk += 0.1
        drivers.append("High CRP")
    elif crp > 5:
        risk += 0.05

    if wbc > 11000:
        risk += 0.1
        drivers.append("High WBC")
    elif wbc > 10000:
        risk += 0.05

    return risk, drivers


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    risk, drivers = calculate_risk(data)

    if risk > 0.6:
        level = "High"
        action = "Immediate attention required"
    elif risk > 0.3:
        level = "Medium"
        action = "Monitor regularly"
    else:
        level = "Low"
        action = "Normal care"

    return render_template(
        'result.html',
        risk=round(risk, 2),
        level=level,
        drivers=drivers ,
        action=action
    )


if __name__ == '__main__':
    app.run(debug=True)