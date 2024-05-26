from datetime import datetime
from enum import Enum
from users import User, Agent

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
    def __init__(self, id, documents:list, agentUsers:list, createdDate, actionType: ActionTypes, emissionsOffset, emissionsEmitted):
        self.netEmissions = emissionsOffset - emissionsEmitted
        self.id = id
        self.documents = documents
        self.agentUsers = agentUsers
        self.createdDate = createdDate
        self.type = actionType
        
        # Check for duplicate document IDs
        document_ids = [doc.id for doc in documents]
        if len(set(document_ids)) != len(document_ids):
            raise ValueError("Duplicate document IDs found")
    
    def update_net_emissions(self):
        self.netEmissions = self.emissions_offset - self.emissions_emitted
    
    def add_document(self, document):
        if any(document.id == doc.id for doc in self.documents):
            self.documents.append(document)
            return "Document added to the action"
        else:
            return "Document already exists in the action"
    