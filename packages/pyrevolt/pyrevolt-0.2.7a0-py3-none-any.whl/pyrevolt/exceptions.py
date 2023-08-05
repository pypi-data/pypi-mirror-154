class WebsocketError(Exception):
    pass

class InternalWebsocketError(WebsocketError):
    pass

class InvalidSession(WebsocketError):
    pass

class OnboardingNotFinished(WebsocketError):
    pass

class AlreadyAuthenticated(WebsocketError):
    pass

class ClosedSocketException(WebsocketError):
    pass

class InvalidMessageException(Exception):
    pass