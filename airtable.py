
from pyairtable import Api
from pyairtable.formulas import match
api = Api('')
baseId = 'appUBZ3kt562wt8Fo'
table = api.table(baseId, 'RefrigerantProviders')

def get_first_record_username(base_id, api, table, username):
    formula = match({"TelegramUserName": username})
    #result = table.first(formula=formula)
    result = table.all(formula=formula)
    return len(result)

def insert_provider_telegram_username(base_id, api, table, username, name, primaryLanguage):
    table.create({"TelegramUserName": username,"PrimaryLanguage": primaryLanguage, "Name": name})
    return 0

