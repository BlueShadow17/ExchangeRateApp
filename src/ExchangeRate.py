import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv

class ExchangeRateApp:
    def __init__(self, root):
        # Main application window.
        self.root = root
        self.root.title("Exchange Rate Tracker")

        # Set up for labels. 
        # Dollar lable:
        self.usd_to_zar_label = tk.Label(root, text="1 Dollar to ZAR", font=('Helvetica', 14, 'bold'), fg='blue')
        self.usd_to_zar_label.grid(row=0, column=0, padx=10, pady=5)

        self.usd_to_zar_value_label = tk.Label(root, text="", font=('Arial', 12))
        self.usd_to_zar_value_label.grid(row=1, column=0, padx=10, pady=10)

        # Date lable:
        self.date_label = tk.Label(root, text="", font=('Arial', 14, 'bold'))
        self.date_label.grid(row=0, column=1, padx=10, pady=5)

        # Rand lable:
        self.zar_to_usd_label = tk.Label(root, text="1 Rand to Dollar", font=('Helvetica', 14, 'bold'), fg='blue')
        self.zar_to_usd_label.grid(row=0, column=2, padx=10, pady=5)

        self.zar_to_usd_value_label = tk.Label(root, text="", font=('Arial', 12))
        self.zar_to_usd_value_label.grid(row=1, column=2, padx=10, pady=10)

        # Set up history button.
        self.history_button = tk.Button(root, text="Show History", command=self.show_history, font=('Arial', 12),
                                        fg='white', bg='green')
        self.history_button.grid(row=2, column=1, pady=10)
        # Set up csv export button.
        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv, font=('Arial', 12),
                                       fg='white', bg='blue')
        self.export_button.grid(row=3, column=1, pady=10)

        # Initialize the exchange rates.
        self.update_rates()

        # Update every hour if applaction up and running.
        self.root.after(3600000, self.auto_update)

        # Bind the close event to save data.
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # Function to scrape exchange rates from a website.
    def scrape_exchange_rates(self):
        url = "https://www.x-rates.com/table/?from=ZAR&amount=1"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            usd = soup.find("a", {"href": "https://www.x-rates.com/graph/?from=ZAR&to=USD"})
            USDto1ZAR = '{:.2f}'.format(round(float(usd.get_text(strip=True)), 2))

            zar = soup.find("a", {"href": "https://www.x-rates.com/graph/?from=USD&to=ZAR"})
            ZARto1USD = '{:.2f}'.format(round(float(zar.get_text(strip=True)), 2))

            return ZARto1USD, USDto1ZAR
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None, None

    # Function to update exchange rates and labels.
    def update_rates(self):
        usd_to_zar_rate, zar_to_usd_rate = self.scrape_exchange_rates()

        if usd_to_zar_rate is not None and zar_to_usd_rate is not None:
            current_date = datetime.now().strftime("%Y-%m-%d")

            self.usd_to_zar_value_label.config(text=f"{usd_to_zar_rate} ZAR")
            self.zar_to_usd_value_label.config(text=f"{zar_to_usd_rate} USD")
            self.date_label.config(text=current_date)

            self.store_data_in_history(current_date, usd_to_zar_rate, zar_to_usd_rate)

    # Function to perform automatic update after 1 hour.
    def auto_update(self):
        self.update_rates()
        self.root.after(3600000, self.auto_update)

    # Function to handle application close event.
    def on_close(self):
        self.root.destroy()

    # Function to store exchange rate data once a day in history table.
    def store_data_in_history(self, date, usd_to_zar_rate, zar_to_usd_rate):
        conn = sqlite3.connect("exchange_rate_history.db")
        cursor = conn.cursor()

        # Makes db and table if it does not exists.
        cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, usd_to_zar_rate TEXT, zar_to_usd_rate TEXT)''')

        cursor.execute("SELECT * FROM history WHERE date=?", (date,))
        existing_entry = cursor.fetchone()

        # Checks if the date exists in databas if not it inserts new data for a new date.
        if not existing_entry:
            cursor.execute("INSERT INTO history (date, usd_to_zar_rate, zar_to_usd_rate) VALUES (?, ?, ?)",
                           (date, usd_to_zar_rate, zar_to_usd_rate))
            conn.commit()

        conn.close()

    # Function to show exchange rate history in a new window.
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Exchange Rate History")

        history_tree = ttk.Treeview(history_window, columns=("ID", "Date", "USD to ZAR Rate", "ZAR to USD Rate"),
                                    show="headings", height=10)
        history_tree.heading("ID", text="ID")
        history_tree.heading("Date", text="Date")
        history_tree.heading("USD to ZAR Rate", text="USD to ZAR Rate")
        history_tree.heading("ZAR to USD Rate", text="ZAR to USD Rate")
        history_tree.pack(pady=10)

        conn = sqlite3.connect("exchange_rate_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()

        for row in rows:
            history_tree.insert("", "end", values=row)

        conn.close()

    # Function to export exchange rate data to a CSV file.
    def export_to_csv(self):
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")

        if start_date and end_date:
            conn = sqlite3.connect("exchange_rate_history.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history WHERE date BETWEEN ? AND ?", (start_date, end_date))
            rows = cursor.fetchall()

            if rows:
                # Asks for path where csv must be saved.
                file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

                if file_path:
                    data_for_csv = []
                    for row in rows:
                        currency_code = row[3]
                        if currency_code.upper() == "USD":
                            exchange_rate = row[2]
                        else:
                            exchange_rate = row[3]
                        data_for_csv.append([row[0], row[1], f"{exchange_rate} {currency_code}"])

                    with open(file_path, 'w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter='|')

                        csv_writer.writerow(["ID", "Date", "Exchange Rate"])
                        csv_writer.writerows(data_for_csv)

                    conn.close()

                    print(f"Data exported to {file_path}")
                else:
                    print("Export canceled by user.")
            else:
                print(f"No data found in the specified date range.")
        else:
            print("Export canceled by user.")

# Main entry point of the program.
if __name__ == "__main__":
    root = tk.Tk()
    app = ExchangeRateApp(root)
    root.mainloop()
