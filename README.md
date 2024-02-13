# ExchangeRateApp
Python program with docker.
## Introdution
    This is a simple Python application that tracks exchange rates between the US Dollar (USD) and South African Rand (ZAR). The application uses a graphical user interface (GUI) built with Tkinter and retrieves exchange rates from a website using web scraping techniques. The exchange rate data is stored in a SQLite database, and users can view historical exchange rates and export data to a CSV file.

### Prerequisites
    Make sure you have Docker installed on your machine before running the application. You can download Docker from https://www.docker.com/get-started.

### How to Run
    Clone the repository to your local machine:

    ```bash
    git clone https://github.com/BlueShadow17/ExchangeRateApp.git
    ```
    Navigate to the project directory:

    ```bash
    cd exchange-rate-tracker
    ```
    Build the Docker image:

    ```bash
    docker-compose build
    
    ```
    Run the Docker container:

    ```bash
    docker-compose up
    ```
    This will start the Exchange Rate application, and you can access it by opening your web browser and navigating to http://localhost:8888.
    Alternatively you can right click on the docker-compose and navagate to the compose up option.

### Usage
    The main application window displays the current exchange rates for 1 USD to ZAR and 1 ZAR to USD.
    The date of the last update is shown in the middle of the window.
    You can click the "Show History" button to view a new window with a table displaying historical exchange rates.
    Clicking the "Export to CSV" button allows you to export exchange rate data to a CSV file for a specified date range.
### Notes
    The application updates exchange rates automatically every hour.
    Exchange rate history is stored in a SQLite database (exchange_rate_history.db).
    The application updates the database every new day it is run.
    Dependencies are listed in the requirements.txt file and include requests and beautifulsoup4.

