from actions import Action
from offset import Offset
from user import User



class Purchase:
    def __init__(self, id, purchase, user, offsets, amount, purchasedate):
        self.id = id
        self.purchase = purchase
        self.user = user
        self.offsets = offsets
        self.amount = amount
        self.purchasedate = purchasedate