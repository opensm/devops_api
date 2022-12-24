from django.utils.translation import gettext_lazy as _


class ParamErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40004
    message = _('params error.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.message
        else:
            self.message = detail
        if code is None:
            code = self.code
        else:
            self.code = code

class DataNotExistException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40001
    message = _('data not found error.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.message
        else:
            self.message = detail
        if code is None:
            code = self.code
        else:
            self.code = code

class PermissionDeniedException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 40003
    message = _('Permission denied error.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.message
        else:
            self.message = detail
        if code is None:
            code = self.code
        else:
            self.code = code

class ServerErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50000
    message = _('Server error.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.message
        else:
            self.message = detail
        if code is None:
            code = self.code
        else:
            self.code = code

class ContentErrorException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    code = 50003
    message = _('Content error.')

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.message
        else:
            self.message = detail
        if code is None:
            code = self.code
        else:
            self.code = code

__all__ = [
    'ParamErrorException',
    'DataNotExistException',
    'PermissionDeniedException',
    'ServerErrorException',
    'ContentErrorException'
    ]