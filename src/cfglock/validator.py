from dataclasses import dataclass
from itertools import zip_longest

keys_to_ignore = {"version"}
# TODO: this needs to actually change for each new versioning that is being made.

"""
Note:
This is a strict file, meaning that webassembly will use this class.
Beware of the contents, and try to be efficient, keep the class minimal.
"""


@dataclass
class ValidationContext:
    new_path: str
    current_path: str
    order_matters: bool


# add other metadata if needed.


class ConfigLockError(Exception):
    """Basic Error"""

    def __init__(self, message, error_code=1):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class ValidationError(ConfigLockError):
    """Error for validation for syncing file"""

    def __init__(
        self,
        path,
        expected_value,
        actual_value,
        message="Validation Failed",
        order_matters=False,
    ):
        super().__init__(message, error_code=100)
        self.path = path
        self.expected_value = expected_value
        self.actual_value = actual_value
        self.order_matters = order_matters

    def __str__(self):
        base_msg = f""" 
        In path: {self.path} 
        Expected: {self.expected_value}
        Found: {self.actual_value}
        """
        if self.order_matters:
            base_msg += "Additional: remember that order matters for keys!"
        return f"{base_msg}\n(Error Code: {self.error_code})"


def walk_yaml_with_no_order(
    current_data, new_data, context: ValidationContext, depth=0
):
    """Recursively walks through a YAML-loaded object with no order."""

    if isinstance(current_data, dict):
        if not isinstance(new_data, dict):
            accept_new_value(
                current_value=current_data, new_value=new_data, context=context
            )
            return

        for curr_k, curr_v in current_data.items():
            # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue

            if curr_k not in new_data:
                accept_new_keys(curr_k, None, context)

            new_v = new_data[curr_k]

            walk_yaml_with_no_order(curr_v, new_v, context, depth + 1)

    else:
        accept_new_value(
            current_value=current_data, new_value=new_data, context=context
        )


def walk_yaml_in_order(current_data, new_data, context: ValidationContext, depth=0):
    """Recursively walks through a YAML-loaded object in order."""

    if isinstance(current_data, dict):
        for new_pair, curr_pair in zip_longest(
            new_data.items(), current_data.items(), fillvalue=(None, None)
        ):
            new_k, new_v = new_pair
            curr_k, curr_v = curr_pair

            # specific values for our own interpretation of versionings etc.
            if curr_k in keys_to_ignore:
                continue

            accept_new_keys(curr_k, new_k, context)

            walk_yaml_in_order(curr_v, new_v, context, depth + 1)

    else:
        accept_new_value(
            current_value=current_data, new_value=new_data, context=context
        )


def accept_new_keys(
    current_key: str | None, new_key: str | None, context: ValidationContext
) -> None:
    """
    General logic for accepting new keys:
    1) the name of new_key cannot be different than the name of current_key
    2) the order of new_key cannot be different than the current_key
    3) the precedence (i.e indentation) cannot be different than the current_key
    """

    if current_key != new_key:
        raise ValidationError(
            path=context.new_path,
            expected_value=current_key,
            actual_value=new_key,
            order_matters=context.order_matters,
        )


def accept_new_value(current_value, new_value, context: ValidationContext) -> None:
    """
    General logic for accepting new values:
    1) the type of the new_value cannot be different than the type of the current_value
    """

    def typed_value(value):
        return f"<{type(value).__name__}> with value: {value!r}"

    if type(current_value) is not type(new_value):
        raise ValidationError(
            path=context.new_path,
            expected_value=typed_value(current_value),
            actual_value=typed_value(new_value),
        )
