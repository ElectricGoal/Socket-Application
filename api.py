import pip._vendor.requests as requests
import json
from datetime import datetime

'''
CÁC GIÁ TRỊ MẶC ĐỊNH, KHÔNG ĐƯỢC THAY ĐỔI
'''
key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mzk2NDgwMDcsImlhdCI6MTYzODM1MjAwNywic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.-olG9A8hV20ojuW62TKwgyVXs5xAby_hBGFq-FvrTVw'
url = 'https://vapi.vnappmob.com/api/v2/exchange_rate/vcb'
params = {'api_key': key}
headers = {'Accept': 'application/json'}


def getDataFromAPI():
    '''Lấy data từ api và ghi dữ liệu lấy được vào file data.json'''

    # Lấy data từ api
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    # Lấy thời gian hiện tại
    data["date_time"] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    write_json(data)


def write_json(new_data, filename='data.json'):
    '''Ghi dữ liệu {new_data} vào file data.json'''

    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["exchange_history"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=2)


def find_currency(currency):
    '''Tìm dữ liệu của {currency} và trả về {exchange_data} kiểu dictionary'''

    #Mở file data.json
    f = open('data.json')
    data = json.load(f)
    
    #Biến kiểm tra có dữ liệu client đang tìm không
    check = False

    exchange_data = {}

    for item in data["exchange_history"][-1]["results"]:

        #Tìm kiếm giá trị currency giống với giá trị client đang tìm kiếm
        if currency == item["currency"]:
            check = True

            exchange_data = {
                "date_time": data["exchange_history"][-1]["date_time"],
                "results": {
                    "currency": item["currency"],
                    "buy_cash": item["buy_cash"],
                    "buy_transfer": item["buy_transfer"],
                    "sell": item["sell"]
                }
            }

    if check == False:
        return "   Cannot find"

    return exchange_data


def dictToDataSendClient(dict_data):
    '''Chuyển đổi dictionary {dict_data} sang dạng list cho client {exchange_data_list}'''

    exchange_data_list = []
    exchange_data_list.append("   %s" %dict_data["date_time"])

    currency_data = "   - Currency: %s" % dict_data["results"]["currency"]
    exchange_data_list.append(currency_data)

    buy_cash_data = "   - Buy cash: %s" % dict_data["results"]["buy_cash"]
    exchange_data_list.append(buy_cash_data)

    buy_transfer_data = "   - Buy transfer: %s" % dict_data["results"]["buy_transfer"]
    exchange_data_list.append(buy_transfer_data)

    sell_data = "   - Sell: %s" % dict_data["results"]["sell"]
    exchange_data_list.append(sell_data)

    return exchange_data_list


def saveUserHistory(user_name, new_data, filename='users_history.json'):
    '''
    Lưu dữ liệu user tìm kiếm vào file users_history.json
    Arguments: tên người dùng {user_name}, data người dùng tìm kiếm {new_data} 
    '''
    check = False
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        users_data = file_data["users_history"]
        for user in users_data:
            if user["name"] == user_name:
                check = True
                user["history"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=2)
        if check == False:
            new_user = {
                "name": user_name,
                "history": [
                    new_data
                ]
            }
            users_data.append(new_user)
            file.seek(0)
            json.dump(file_data, file, indent=2)

def sendUserHistory(user_name, filename='users_history.json'):
    history_data = []
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        users_data = file_data["users_history"]
        for user in users_data:
            if user["name"] == user_name:
                history_data = convertUserHistoryData(user["history"])
                break
    # print(history_data)
    return history_data

def convertUserHistoryData(user_history_data):
    history_data = []
    for item in user_history_data:
        new_data = dictToDataSendClient(item)
        history_data.append(new_data)

    return history_data


# print(sendUserHistory("A"))