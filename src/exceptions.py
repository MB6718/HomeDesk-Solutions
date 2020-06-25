class ServiceError(Exception):
    service = None

    def __init__(self, *args):
        super().__init__(self.service, *args)

# class TransactionsServiceError(ServiceError):
    # service = 'transactions'

class CategoryDoesNotExistError(ServiceError):
    pass

class PermissionError(ServiceError):
    pass
