from datetime import datetime


class Document:
    def __init__(self, path, id, name, type, createdBy, createdDate):
        self.path = path
        self.id = id
        self.name = name
        self.type = type
        self.createdBy = createdBy
        self.createdDate = createdDate