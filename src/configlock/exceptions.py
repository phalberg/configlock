
class ConfigLockError(Exception):
    """Basic Error"""

def __init__(self, message, error_code=1):
    super().__init__(message)
    self.message = message
    self.error_code = error_code


def __str__(self):
    return f"{self.message} (Error Code: {self.error_code})"


class ValidationError(ConfigLockError):
    """Error for validation for syncing file"""
        
def __init__(self, path, expected_value, actual_value, message="Validation Failed"):
    super().__init__(message, error_code=100)
    self.path = path    
    self.expected_value = expected_value
    self.actual_value = actual_value
    

def __str__(self):
    return f"In {self.path} it was found: {self.actual_value} but the expected was: {self.expected_value}. (Error Code: {self.error_code})"

    

    
    
    