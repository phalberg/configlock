
class ConfigLockError(Exception):
    """Basic Error"""

def __init__(self, message, error_code):
    super().__init__(message)
    self.error_code = error_code


def __str__(self):
    return f"{self.message} (Error Code: {self.error_code})"


class ValidationError(ConfigLockError):
    """Error for validation for syncing file"""
    
    
def __init__(self, message, error_code):
    pass


def __str__(self):
    pass

    

    
    
    