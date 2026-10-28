
class AuthenticationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class RegistrationConflict(Exception):
    def __init__(self, msg):
        super().__init__(msg)
