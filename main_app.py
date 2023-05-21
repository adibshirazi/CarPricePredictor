from sklearn.tree import DecisionTreeRegressor
import mysql.connector
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

mydb = mysql.connector.connect(
    host="localhost",
    user="ash",
    password="100100",
    database="truecar_database"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT car, model, mile, price FROM info")
results = mycursor.fetchall()

car = input("Enter car name: ").lower()  
model_name = input("Enter model: ").lower()  
mile = int(input("Enter mile: "))

car = car.lower()
model_name = model_name.lower()

user_input_exists = False
for row in results:
    if row[0].lower() == car and row[1].lower() == model_name:
        user_input_exists = True
        break

if user_input_exists:
    X = []
    y = []
    for row in results:
        X.append([row[0], row[1], row[2]])
        y.append(row[3])

    df = pd.DataFrame(X, columns=['car', 'model', 'mile'])

    df['car'] = df['car'].str.lower()
    df['model'] = df['model'].str.lower()

    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    df_ohe = pd.DataFrame(ohe.fit_transform(df[['car', 'model']]), columns=ohe.get_feature_names(['car', 'model']))
    df = pd.concat([df.drop(['car', 'model'], axis=1), df_ohe], axis=1)

    model = DecisionTreeRegressor()
    model.fit(df.values, y)

    car_ohe = pd.DataFrame(ohe.transform([[car, model_name]]), columns=ohe.get_feature_names(['car', 'model']))
    user_input = pd.concat([pd.DataFrame({'mile': [mile]}), car_ohe], axis=1)
    prediction = model.predict(user_input.values)

    print(f"The predicted price for {car} {model_name} with {mile} miles is ${prediction[0]:,.2f}")
else:
    print("Your car doesn't exist in the database")

mycursor.close()
mydb.close()
