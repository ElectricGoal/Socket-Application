import pip._vendor.requests as requests
import json
from datetime import datetime


key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mzk2NDgwMDcsImlhdCI6MTYzODM1MjAwNywic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.-olG9A8hV20ojuW62TKwgyVXs5xAby_hBGFq-FvrTVw'
url = 'https://vapi.vnappmob.com/api/v2/exchange_rate/vcb'
params  = {'api_key': key}
headers = {'Accept': 'application/json'}

def getDataFromAPI():
    #Lấy data từ api
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    # Lấy thời gian hiện tại
    data["date_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # new_string = json.dumps(data, indent=2)
    write_json(data)

# function to add to JSON
def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["exchange_history"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 2)

def find_currency(currency):
    f = open('data.json')
    data = json.load(f)
    
    check = False
    exchange_data = []

    print(data["exchange_history"][-1]["date_time"])
    exchange_data.append(data["exchange_history"][-1]["date_time"])
    
    for item in data["exchange_history"][-1]["results"]:
        if currency == item["currency"]:
            check = True

            currency_data = "Currency: %s" %item["currency"]
            print(currency_data)

            buy_cash_data = "Buy cash: %s" %item["buy_cash"]
            print(buy_cash_data)

            buy_transfer_data = "Buy transfer: %s" %item["buy_transfer"]
            print(buy_transfer_data)

            sell_data = "Sell: %s" %item["sell"]
            print(sell_data)

            exchange_data.append(currency_data)
            exchange_data.append(buy_cash_data)
            exchange_data.append(buy_transfer_data)
            exchange_data.append(sell_data)

    if check == False:
        print("Cannot find!")   

    return exchange_data

# find_currency("JPY")


# url = 'https://api.exchangerate.host/convert'

# def exchangeRate(currency, date):
#     params = {'from': currency, 'to': 'VND', 'date': date, 'places': '2'}
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data

# currency = input('Enter currency: ')
# date = input('Enter date: ')

# print(exchangeRate(currency, date))