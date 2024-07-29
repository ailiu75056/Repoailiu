
from pyairtable import Api
from pyairtable.formulas import match
import os
import datetime

api = Api(os.environ["AT_API_TOKEN"])
baseId = 'appUBZ3kt562wt8Fo'
tableProviders = api.table(baseId, 'RefrigerantProviders')
tableManagement = api.table(baseId, 'Refrigerant Management')
tableChatlog= api.table(baseId, 'TelegramChatLog')

def get_first_record_username(base_id, api, table, username):
    formula = match({"TelegramUserName": username})
    #result = table.first(formula=formula)
    result = table.all(formula=formula)
    print(result)
    if 'PhoneNumber' in result[0]['fields'].keys():
            ifPhoneNumber = True
    else:
            ifPhoneNumber = False
    if len(result) > 0:
        userId = result[0]['fields']['ProviderID']
   
    return [len(result), ifPhoneNumber, userId]

def insert_new_refrigerant(base_id, api, table, providerId, refrigerantType, amountKG=0):
    result = table.create({"RefrigerantType": str.upper(refrigerantType), "AmountKG": amountKG, "Provider": [providerId]})
    return result
#takes a refrigerantID and args in form of a dictionary
def update_refrigerant(base_id, api, table, refrigerantId, args: dict):
    result = table.update(refrigerantId, args)
    return result 

def insert_provider_telegram_username(base_id, api, table, username, name, primaryLanguage):
    table.create({"TelegramUserName": username,"PrimaryLanguage": primaryLanguage, "Name": name})
    return 0

def update_provider_telegram_phoneNumber(base_id, api, table, userName, phoneNumber):
    formula = match({"TelegramUserName": userName})
    result = table.first(formula=formula)
    table.update(result['id'], {"PhoneNumber": phoneNumber})
    return 0


def insert_telegram_chat_log(base_id, api, table, update_id, chat_id, text,date):
    table.create({"ChatId": chat_id, "Text": text,"UpdateID": update_id, "DateTime": date})
    return 0

#print(insert_new_refrigerant(baseId, api, tableManagement, "recEQ7oAfatBYb8mz", "R134a", 10 ))