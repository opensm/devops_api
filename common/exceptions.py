"""
Exceptions used by django-guardian. All internal and guardian-specific errors
should extend GuardianError class.
"""


class UtilError(Exception):
    pass


class NotUserNorGroup(UtilError):
    pass


class ObjectNotPersisted(UtilError):
    pass


class WrongAppError(UtilError):
    pass


class MixedContentTypeError(UtilError):
    pass


class MultipleIdentityAndObjectError(UtilError):
    pass
