from actions import Action, ActionTypes
from datetime import datetime

class Offset:
    def __init__(self, id, testingActions:list= [], offsetActions:list = [], logisticalActions:list= [], createddate:datetime= datetime.now()):
        self.id = id
        self.testingActions = testingActions
        self.offsetActions = offsetActions
        self.logisticalActions = logisticalActions
        self.createddate = createddate

    def add_testingAction(self, action):
        if action.type == ActionTypes.Testing:
            self.testingActions.append(action)
        elif action.type == ActionTypes.Collection:
            self.offsetActions.append(action)
        elif action.type == ActionTypes.Transportation:
            self.logisticalActions.append(action)
        else:
            raise ValueError("Invalid action type")
        return self.testingActions
    
    def add_offsetAction(self, action):
        if action.type == ActionTypes.Testing:
            self.testingActions.append(action)
        elif action.type == ActionTypes.Collection:
            self.offsetActions.append(action)
        elif action.type == ActionTypes.Transportation:
            self.logisticalActions.append(action)
        else:
            raise ValueError("Invalid action type")
        return self.offsetActions
    
    def add_logisticalAction(self, action):
        if action.type == ActionTypes.Testing:
            self.testingActions.append(action)
        elif action.type == ActionTypes.Collection:
            self.offsetActions.append(action)
        elif action.type == ActionTypes.Transportation:
            self.logisticalActions.append(action)
        else:
            raise ValueError("Invalid action type")
        return self.logisticalActions