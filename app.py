from flask import Flask, render_template, request, redirect
import mysql.connector as mc
import joblib
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='disease_p')
model = joblib.load('randomforestclassifier.lb') 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('userdata.html')


@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        
        disease = request.form['disease']
        fever = request.form['fever']
        cough = request.form['cough']
        fatigue = request.form['fatigue']
        difficulty_breathing = request.form['difficulty_breathing']
        age = int(request.form['age'])
        gender = request.form['gender']
        blood_pressure = request.form['blood_pressure']
        cholesterol_level = request.form['cholesterol_level']

        le = LabelEncoder()

        disease_encoded = le.fit_transform([disease])[0]
        fever_encoded = le.fit_transform([fever])[0]
        cough_encoded = le.fit_transform([cough])[0]
        fatigue_encoded = le.fit_transform([fatigue])[0]
        difficulty_breathing_encoded = le.fit_transform([difficulty_breathing])[0]
        gender_encoded = le.fit_transform([gender])[0]

        blood_pressure_mapping = {
            'high': 0,
            'low': 1,
            'normal': 2
        }

        cholesterol_level_mapping = {
            'low': 0,
            'normal': 1,
            'high': 2
        }

        
        blood_pressure_encoded = blood_pressure_mapping.get(blood_pressure, 2)  
        cholesterol_level_encoded = cholesterol_level_mapping.get(cholesterol_level, 1)  


        unseen_data = [[disease_encoded, fever_encoded, cough_encoded, fatigue_encoded, difficulty_breathing_encoded, age, gender_encoded, blood_pressure_encoded, cholesterol_level_encoded]]

        
        output = model.predict(unseen_data)[0]

        query = """INSERT INTO data (disease, fever, cough, fatigue, difficulty_breathing, age, gender, blood_pressure, cholesterol_level, predicted)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        mycursor = conn.cursor()

    
        details = (disease, fever, cough, fatigue, difficulty_breathing, age, gender, blood_pressure_encoded, cholesterol_level_encoded, int(output))

        mycursor.execute(query, details)
        conn.commit()

        mycursor.close()

    
        if output == 0:
            return "Patient doesn't have any disease."
        else:
            return "Patient has a disease."


@app.route('/history')
def patient_history():
    mycursor = conn.cursor()
    query = "SELECT * FROM data"
    mycursor.execute(query)
    data = mycursor.fetchall()

    mycursor.close()

    return render_template('history.html', userdetails=data)

if __name__ == "__main__":
    app.run(debug=True)
