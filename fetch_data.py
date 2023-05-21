from bs4 import BeautifulSoup
import requests
import mysql.connector

base_url = "https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true&page={}"

num_pages = int(input("how many pages you want to scrape: "))

mydb = mysql.connector.connect(
    host="localhost",
    user="ash",
    password="100100",
    database="truecar_database"
)

mycursor = mydb.cursor()

sql = "INSERT INTO info (car, model, price, mile) VALUES (%s, %s, %s, %s)"

for i in range(1, num_pages + 1):
    url = base_url + str(i)
    response = requests.get(url)

    if response.status_code == 200:
        print(f'Page {i} content length: {len(response.content)}')
    else:
         print(f'Error requesting page {i}: {response.status_code} {response.reason}')

    soup = BeautifulSoup(response.content, 'html.parser')

    miles_info = [int(''.join(filter(str.isdigit, mile.text))) for mile in soup.find_all('div', {'class': 'truncate text-xs', 'data-test': 'vehicleMileage'})]
    prices_info = [int(''.join(filter(str.isdigit, price.text))) for price in soup.find_all('div', class_="heading-3 my-1 font-bold")]

    cars_yearMakeModel_tags = soup.find_all('div', {'data-test': 'vehicleCardYearMakeModel', 'class': 'vehicle-card-header w-full'})
    cars_info = [tag.find('span', 'truncate').text for tag in cars_yearMakeModel_tags]

    model_info = [model.text for model in soup.find_all('div', {'class': 'truncate text-xs', 'data-test': "vehicleCardTrim"})]

    for car, model, price, mile in zip(cars_info, model_info, prices_info, miles_info):
        val = (car, model, price, mile)
        mycursor.execute(sql, val)

mydb.commit()
mycursor.close()
mydb.close()
print("done")
