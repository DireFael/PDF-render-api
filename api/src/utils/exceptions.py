
def make_error_message(error_code=None, error_message=None, field=None):
 # Making error message for all exception

    if field is None:
        field = []

    result = {
        "errors": {
            "error_code": error_code or 500,
            "error_message": error_message or "",
            "field": [field] if type(field) is not list else field 
        }
    }

    return result

# Making own Exception to raise anywhare with same format
class ErrorException(Exception):

    def __init__(self, status_message, status_code=None, data=None):

        super().__init__()

        self.status_message = status_message
        self.status_code = status_code or 500
        self.data = data if data else ""


class InvalidArgumentsException(ErrorException):

    def __init__(self, error_code=None, error_message=None, field=None, data=None):

        if data is None:
            data = make_error_message(error_code, error_message, field)

        super().__init__("Invalid arguments", 422, data)


class BadRequestException(ErrorException):

    def __init__(self, data=None):
        super().__init__("Bad Request", 400, data)


class NotFoundException(ErrorException):

    def __init__(self, data=None):
        super().__init__("Not found", 404, data)


class UnexpectedErrorException(ErrorException):

    def __init__(self, status_message=None, data=None):

        message = status_message or "Unexpected error occured"

        super().__init__(message, 500, data)
