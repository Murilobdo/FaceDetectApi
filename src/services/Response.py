class Response():
    def __init__(self, message, isValid):
        self.message = message
        self.isValid = isValid

    def to_dict(self):
        return { 'message': self.message, 'isValid': self.isValid }