import inspect

import pytest

from cfglock import validator
from cfglock.validator import (
    accept_new_keys,
    accept_new_value,
    walk_yaml_with_no_order,
    walk_yaml_in_order,
)


def helper_sig_class(name_class):
    """
    Retrive the signature of a class.
    """

    sig = inspect.getfullargspec(name_class).annotations

    return sig


def helper_sig_def(name_def):
    """
    Retrive parameters and signature of a defintion.
    """
    sig = inspect.signature(name_def)

    params = sig.parameters.items()

    return params, sig


def test_sig_context():

    val_context_sig = helper_sig_class(name_class=validator.ValidationContext)

    sig_list = ["new_path", "current_path", "order_matters"]

    assert ("return", None) in val_context_sig.items()
    assert all(key in val_context_sig for key in sig_list)
    assert ("new_path", str) in val_context_sig.items()
    assert ("current_path", str) in val_context_sig.items()


@pytest.mark.parametrize(
    "name_def",
    [
        walk_yaml_with_no_order,
        walk_yaml_in_order,
    ],
    ids=["Signature without order", "Signature with order"],
)
def test_sig_walk_n_order(name_def):

    walk_n_order_sig, sig = helper_sig_def(name_def=name_def)

    param_list = ["current_data", "new_data", "context", "depth"]

    sig_obj = sig.parameters["context"]
    dict_walk_n_order = dict(walk_n_order_sig)

    assert all(param in sig.parameters for param in param_list)
    assert ("context", sig_obj) in dict_walk_n_order.items()


@pytest.mark.parametrize(
    "name_def",
    [
        accept_new_keys,
        accept_new_value,
    ],
    ids=[
        "check signature of accepting new keys",
        "check signature for accepting new values",
    ],
)
def test_accept_new_value_and_keys(name_def):
    accept_new, sig = helper_sig_def(name_def)

    sig_list_keys = ["current_key", "new_key", "context"]
    sig_list_value = ["current_value", "new_value", "context"]

    expected_params = []
    # change sig. list based on which function we are trying to receive
    if name_def.__name__ == "accept_new_keys":
        expected_params.extend(sig_list_keys)
    elif name_def.__name__ == "accept_new_value":
        expected_params.extend(sig_list_value)

    dict_accept = dict(accept_new)
    sig_obj = sig.parameters["context"]

    # TODO: fix to use something like: sig.parameters.get("context").annotation.__name__, later sine we dont need to actually create a dict here!
    assert all(param in sig.parameters for param in expected_params)
    assert ("context", sig_obj) in dict_accept.items()
