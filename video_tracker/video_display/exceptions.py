# VideoController
class UnknownUnitError(Exception):
    pass


class BadIncrement(Exception):
    pass


class NonPositiveIncrement(BadIncrement):
    pass


class NonIntegerIncrement(BadIncrement):
    pass


# VideoPlayer
class TrackCountError(Exception):
    pass
