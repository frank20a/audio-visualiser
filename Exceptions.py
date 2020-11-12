class LedIndexError(Exception):
    """LED List index out of range or not found"""
    pass


class InvalidIndexType(Exception):
    """LED list index is of invalid type. Use pos tuple or index number"""
    pass


class LedNotFound(Exception):
    """LED List index not found for given position"""
    pass


class TargetNotInLine(Exception):
    """Target LED is not in direct line with previous"""
    pass


class NothingToDraw(Exception):
    """Cannot draw nothing"""
    pass


class LedAlreadyPresent(Exception):
    """Tried to insert LED over existing one"""
    pass


class LedLayoutEmpty(Exception):
    """LED Layout is currently empty"""
    pass


class SaveDirNotSet(Exception):
    """Save button is enables but save dir is not set"""
    pass


class ConflictingSizes(Exception):
    """Size of Screen conflicts with size of an attribute"""
    pass


class ConnectionInterrupted(Exception):
    """Connection with Serial or TCP Client has been interrupdet"""
    pass


class Timeout(Exception):
    """Connection timed out"""
    pass


class ConnectionNotACKed(Exception):
    """Server responded with wrong ACK signal"""
    pass
