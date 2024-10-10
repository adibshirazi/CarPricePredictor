# Car Price Prediction Project

This project is a car price prediction tool that allows users to scrape car data from TrueCar's website, store it in a MySQL database, and use machine learning to predict car prices based on model, car type, and mileage.

## Features

- Web scraping from TrueCar using BeautifulSoup
- Data stored in a MySQL database
- Predict car prices using a DecisionTreeRegressor model
- OneHotEncoder for handling categorical features (car name, model)

## Project Structure

- `fetch_data.py`: Scrapes car data (name, model, price, mileage) from TrueCar and inserts it into a MySQL database.
- `main_app.py`: Uses machine learning to predict car prices based on user input (car name, model, mileage) using previously scraped data.

## License

This project is open-source and available under the [MIT License](LICENSE).
