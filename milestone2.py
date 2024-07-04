import csv
import os

data_sources = []

def checker():
    if not data_sources:
        print("No data sources available.")
    else:
        for i, (file_path, metric) in enumerate(data_sources[-3:], 1):
            file_name = os.path.basename(file_path)
            print(f"{i}) Datasource: {file_name} | Metric: {metric}")

def calculate_metric():
    if not data_sources:
        print("No data sources available.")
        return

    print("Select data source:")
    for i, (file_path, _) in enumerate(data_sources, 1):
        file_name = os.path.basename(file_path)
        print(f"{i}. {file_name}")

    try:
        choice = int(input("Enter the number of the data source: ").strip())
        if 1 <= choice <= len(data_sources):
            file_path = data_sources[choice - 1][0]
            data = read_csv(file_path)
            if data:
                headers, records = add_data(data)
                print(f"Selected data source: {os.path.basename(file_path)} | Total records: {records}")
                net_profit_margin = calculate_net_profit_margin(data)
                print(f"Net Profit Margin: {net_profit_margin:.2f}%")
                data_sources[choice - 1] = (file_path, f"Net Profit Margin = {net_profit_margin:.2f}%")
            else:
                print("Failed to read the data source. Please check the file and try again.")
        else:
            print("Invalid choice. Try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")

def calculate_net_profit_margin(data):
    try:
        total_revenue = sum(float(row[8]) for row in data[1:])  # assuming revenue is in the 9th column
        net_income = sum(float(row[30]) for row in data[1:])  # assuming net income is in the 31st column
        return (net_income / total_revenue) * 100 if total_revenue else 0
    except ValueError:
        print("Error in data format. Please ensure the CSV contains valid numeric values for revenue and net income.")
        return 0

def read_csv(path):
    try:
        with open(path.strip(), mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            data = [row for row in csv_reader]
        return data
    except PermissionError:
        print(f"Permission denied: '{path}'. Please check the file permissions.")
        return None
    except FileNotFoundError:
        print(f"File not found: '{path}'. Please check the file path.")
        return None

def add_data(read_data):
    if read_data:
        headers = ' | '.join(read_data[0])
        records = len(read_data[1:])
        return headers, records
    else:
        return "", 0

while True:
    print("1. Check existing information")
    print("2. Add a new data source(file)")
    print("3. Calculate metric")
    print("4. Exit")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        checker()
    elif choice == "2":
        file_path = input("Enter file path: ").strip()
        data = read_csv(file_path)
        if data:
            headers, records = add_data(data)
            data_sources.append((file_path, "Metric not calculated"))
            print(f'Outline: {headers}\nTotal records: {records}')
    elif choice == "3":
        calculate_metric()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Try again")

