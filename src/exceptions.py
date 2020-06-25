class ServiceError(Exception):
    service = None

    def __init__(self, *args):
        super().__init__(self.service, *args)

class PermissionError(ServiceError):
    pass