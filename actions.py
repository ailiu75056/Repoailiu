from datetime import datetime
from enum import Enum
from users import User, Agent, Buyer

offset_dict = {
    'R32': 675,
    'R134A': 1430,
    'R404A': 3922,
    'R407C': 1774,
    'R410A': 2088,
    'R22': 1810,
    'Other': 1430
}



class ActionTypes(Enum): 
    Collection = "Collection"
    Testing = "Testing"
    Transportation = "Transportation"
    Destruction = "Destruction"

class ActionStatus(Enum): 
    Completed = "Completed"
    In_Progress = "In Progress"
    Disputed = "Disputed"


class RefrigerantTypes(Enum):
     R_32 = "R 32"
     R_22 = "R 22"
     R_134a = "R 134a"
     R_404a = "R 404a"
     R_407c = "R 407c"
     R_410a = "R 410a"
     Other = "Other"



class Action:
    def __init__(self, id, refrigerantType: str, quantityKG: float, documents:list,  agentUsers:list, createdDate, actionType: ActionTypes, emissionsEmitted = 0):
        #both  emissions and offset are assumed to be positive numbers, so if 1 KG of COE of gasoline is used to transport and 2000 KG of Coe is offset, the net offset is 1999 KG, input both as positive values
        self.id = id
        self.documents = documents
        self.agentUsers = agentUsers
        self.createdDate = createdDate
        self.type = actionType
        self.quantityKG = quantityKG
        self.offsetCo2E = quantityKG*offset_dict[self.refrigerantType]
        if self.emissionsEmitted < 0:
            raise ValueError("Emissions emitted must be a positive number")
        if self.offsetCo2E < 0:
            raise ValueError("Offset must be a positive number")
        
        # Check for duplicate document IDs
        document_ids = [doc.id for doc in documents]
        if len(set(document_ids)) != len(document_ids):
            raise ValueError("Duplicate document IDs found")
   
    @property
    def netOffsetKGCO2E(self):
        return self.offsetCo2E - self.emissions_emitted
    
    def add_document(self, document):
        if any(document.id == doc.id for doc in self.documents):
            self.documents.append(document)
            return self.documents
        else:
            raise  ValueError("Document already exists in the action")


class Destruction(Action):
    def __init__(self, id, logData, quantityKG, refrigerantType: str,  documents:list, agentUsers:list, cementKiln, address, startDate, endDate, createdDate, actionType: ActionTypes, emissionsEmitted = 0):
        super().__init__(id, documents, quantityKG,refrigerantType,  agentUsers, createdDate, actionType, emissionsEmitted)
        self.cementKiln = cementKiln
        self.address = address
        self.startDate = startDate
        self.endDate = endDate
        self.logData = logData

class Collection(Action):
    def __init__(self, id, documents:list, refrigerantType: str,  quantityKG,  agentUsers:list, createdDate, actionType: ActionTypes,  paymentAMT: float, paymentApiLink: str, primaryAgent: Agent, emissionsEmitted = 0):
        super().__init__(id, documents, refrigerantType, quantityKG, agentUsers, createdDate, actionType, emissionsEmitted)
        self.paymentAMT = paymentAMT
        self.paymentApiLink = paymentApiLink
        self.PrimaryAgent = primaryAgent
        if primaryAgent.userType != "Agent":
            raise ValueError("Primary agent must be an agent")
        if primaryAgent not in agentUsers:
            raise ValueError("Primary agent must be in agent users")
        