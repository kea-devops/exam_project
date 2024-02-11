
class TransactionError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 500
    pass