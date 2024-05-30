from actions import Action, ActionTypes
from datetime import datetime




class Offset:
    def __init__(self, id, destructionAction:Action, testingActions:list, collectionActions:list, logisticalActions, createddate:datetime= datetime.now()):
        self.id = id
        self.testingActions = testingActions
        self.offsetActions = collectionActions
        self.logisticalActions = logisticalActions
        self.createddate = createddate
        self.destructionAction = destructionAction
        self.offsetKG= 0

    @property
    def offsetKG(self): 
        collectionOffsetKG= 0 
        collectionEmissions= 0 
        logisticalEmissions=0
        testingEmissions = 0
        destructionOffsetKG = 0
        destructionEmissions = 0
        for action in self.collectionActions:
            if action.type == ActionTypes.Collection:
                collectionEmissions += action.emissionsEmitted
                collectionOffsetKG += action.netOffsetKGCO2E
        
        for action in self.logisticalActions:
            if action.type == ActionTypes.Transportation:
                logisticalEmissions += action.emissionsEmitted
        
        for action in self.testingActions:
            if action.type == ActionTypes.Testing:
                testingEmissions += action.emissionsEmitted
        
        for action in self.destructionAction:
            if action.type == ActionTypes.Destruction:
                destructionOffsetKG += action.netOffsetKGCO2E
        
        offsetKG = destructionOffsetKG - destructionEmissions  - collectionEmissions - logisticalEmissions - testingEmissions
        return offsetKG

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