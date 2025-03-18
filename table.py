import mysql.connector as mc

conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='disease_p')

if conn.is_connected():
    print("You are connected.")
else:
    print('Unable to connect.')

mycursor = conn.cursor()


query = """CREATE TABLE data(
    disease VARCHAR(80),
    fever VARCHAR(80),
    cough VARCHAR(80),
    fatigue VARCHAR(80),
    difficulty_breathing VARCHAR(80),
    age INT,
    gender VARCHAR(80),
    blood_pressure INT,
    cholesterol_level INT,
    predicted INT
)
"""

mycursor.execute(query)
print('Your table is created.')

mycursor.close()
conn.close()

