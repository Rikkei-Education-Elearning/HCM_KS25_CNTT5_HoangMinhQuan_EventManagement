class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)

class EventNotFoundError(Exception):
    def __init__(self, message: str = "Event not found"):
        self.message = message
        super().__init__(self.message)

class EventTaskNotFoundError(Exception):
    def __init__(self, message: str = "Event task not found"):
        self.message = message
        super().__init__(self.message)

class BadRequestError(Exception):
    def __init__(self, message: str = "Bad request"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedError(Exception):
    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(self.message)

class ForbiddenError(Exception):
    def __init__(self, message: str = "Forbidden"):
        self.message = message
        super().__init__(self.message)

class EmailAlreadyExistsError(Exception):
    def __init__(self, message: str = "Email already exists"):
        self.message = message
        super().__init__(self.message)

class InvalidPasswordOrEmailError(Exception):
    def __init__(self, message: str = "Invalid password or email"):
        self.message = message
        super().__init__(self.message)

class TokenExpiredError(Exception):
    def __init__(self, message: str = "Token expired"):
        self.message = message
        super().__init__(self.message)

class TooManyLoginAttemts(Exception):
    def __init__(self, message: str = "Too many login attempts"):
        self.message = message
        super().__init__(self.message)

