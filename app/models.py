# create models here
import json 
class Trade:
    def __init__(self, id, type, user_id, symbol, shares, price, timestamp):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.symbol = symbol
        self.shares = shares
        self.price = price
        self.timestamp = timestamp
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)