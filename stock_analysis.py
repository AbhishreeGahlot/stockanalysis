import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates  # Add import statement for mdates

def get_stock_data(api_key, symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        messagebox.showerror("Error", "Failed to fetch data from API")
        return None

def analyze_stock():
    symbol = symbol_entry.get()
    api_key = api_key_entry.get()

    if not symbol or not api_key:
        messagebox.showerror("Error", "Please enter both symbol and API key")
        return

    data = get_stock_data(api_key, symbol)

    if data:
        # Extract relevant data for candlestick plot
        stock_data = data["Time Series (5min)"]
        dates = []
        open_prices = []
        high_prices = []
        low_prices = []
        close_prices = []

        for date, values in stock_data.items():
            dates.append(mdates.datestr2num(date))  # Convert date string to numeric format
            open_prices.append(float(values["1. open"]))
            high_prices.append(float(values["2. high"]))
            low_prices.append(float(values["3. low"]))
            close_prices.append(float(values["4. close"]))

        # Clear previous plot
        for widget in output_frame.winfo_children():
            widget.destroy()

        # Create candlestick plot
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        candlestick_data = zip(dates, open_prices, high_prices, low_prices, close_prices)  # Correct data format
        ax.candlestick(candlestick_data, width=0.6, colorup='g', colordown='r')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title(f'{symbol} Candlestick Chart')

        # Display plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", "Failed to fetch data")

# GUI setup
root = tk.Tk()
root.title("Stock Market Analysis")
root.geometry("800x600")

tk.Label(root, text="Enter Stock Symbol:").pack()
symbol_entry = tk.Entry(root)
symbol_entry.pack()

