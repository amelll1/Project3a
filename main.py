from datetime import datetime
import logging

from dataFetcher import getStockData
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generateGraph
from timeSeriesFunctions import getTimeSeriesFunction  # Import getTimeSeriesFunction from timeSeriesFunctions.py

symbol = getStockSymbol()



# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parseDate(date_string):
    """Parse a string into a datetime object."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        return None

def preprocess_data(api_response, symbol, timeSeriesFunction, apikey, start_date, end_date):
    """Extract and reformat data from Alpha Vantage API response."""
    # This now uses the symbol and apikey variables passed to the function
    raw_data = getStockData(symbol, timeSeriesFunction, apikey)

    # Filter data within the specified date range and reformat
    data = {date: float(details['4. close']) for date, details in raw_data.items() if start_date <= date <= end_date}
    return data

def main():
    apikey = "542MHNFURI47POKH"
    symbol = getStockSymbol()
    timeSeriesFunction = getTimeSeriesFunction()  # Ask for the time series function

    # Ask for the start date
    logging.info("Please enter the start date.")
    startDate = getStartDate()  # Use getStartDate instead of getValidDate

    # Ask for the end date
    endDate = getEndDate(startDate)

    # Ask for the chart type
    chartType = getChartType()

    # Fetch stock data from Alpha Vantage
    raw_data = getStockData(symbol, timeSeriesFunction, apikey)
    if not raw_data:
        logging.error(f"Failed to fetch data for symbol: {symbol}")
        return

    # Preprocess the fetched data
    formattedStartDate = startDate.strftime('%Y-%m-%d')
    formattedEndDate = endDate.strftime('%Y-%m-%d')
    data = preprocess_data(raw_data, symbol, timeSeriesFunction, apikey, formattedStartDate, formattedEndDate)
    if not data:
        logging.error("No data available for the selected date range.")
        return

    # Generate and display the graph
    generateGraph(data, chartType, formattedStartDate, formattedEndDate)




if __name__ == "__main__":
    main()






# # tested to see if api properly hooked up to app: successful
# import requests

# def fetch_stock_data(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             print("Error:", response.status_code)
#             return None
#     except Exception as e:
#         print("Error:", e)
#         return None

# def main():
#     api_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
#     data = fetch_stock_data(api_url)
#     if data:
#         print("Data fetched successfully:")
#         print(data)
#     else:
#         print("Failed to fetch data.")

# if __name__ == "__main__":
#     main()