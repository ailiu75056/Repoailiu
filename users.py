class User:
    def __init__(self, id, firstName, lastName, middleName, dateOfBirth, userType, createdDate, company, email = '', phone = ''):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.middleName = middleName
        self.dateOfBirth = dateOfBirth
        self.userType = userType
        self.createdDate = createdDate
        self.company = company
        self.email = email
        self.phone = phone
        

class Agent(User):
    def __init__(self, id, username, firstName, lastName, middleName, dateOfBirth, userType, createdDate, company, apiId, description, employmentType):
        super().__init__(id, firstName, lastName, middleName, dateOfBirth, userType, createdDate)
        self.apiId = apiId
        self.description = description
        self.employmentType = employmentType
        self.company = company
        self.username = username 


class Buyer(User):
    def __init__(self, id, firstName, lastName, middleName, dateOfBirth, userType, createdDate, buyerType, segment, paymentMethods):
        super().__init__(id, firstName, lastName, middleName, dateOfBirth, userType, createdDate)
        self.buyerType = buyerType
        self.segment = segment
        self.paymentMethods = paymentMethods


