class ServiceError(Exception):
    service = None
    
    def __init__(self, *args):
        super().__init__(self.service, *args)

# class CategoriesServiceError(ServiceError):
    # service = 'categories'

class CategoryConflictError(ServiceError):
    def __init__(self, category):
        ServiceError.__init__(self)
        self.category = category

class ConflictError(ServiceError):
    pass

class CategoryDoesNotExistError(ServiceError):
    pass

class PermissionError(ServiceError):
    pass
