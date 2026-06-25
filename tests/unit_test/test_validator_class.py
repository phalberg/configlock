import inspect

import pytest

from cfglock import validator
from cfglock.validator import walk_yaml_with_no_order, walk_yaml_in_order


def helper_debugging():
    # print(inspect.getfullargspec(validator.ValidationContext))
    # sig = inspect.getfullargspec(validator.ValidationContext).annotations
    # print(sig)
    # print("new_path" in sig)
    # print(("return", None) in sig.items())
    # print(helper_sig_class(name_class=validator.walk_yaml_with_no_order))
    # print(inspect.signature(walk_yaml_in_order).parameters.items())
    # walk_n_order_sig = helper_sig_def(name_def=walk_yaml_with_no_order)
    # print(walk_n_order_sig)
    # sig_list = ["current_data", "new_data", "context", "depth"]
    # dict_sig = dict(walk_n_order_sig)
    # print(dict_sig)
    # for param_name, param_obj in walk_n_order_sig:
    #    print(f"Parameter Name: {param_name}")
    #    print(f"  Default Value: {param_obj.default}")
    #    print(f"  Annotation:    {param_obj.annotation}")
    # print(key, value in dict_sig for key in sig_list)
    # print(all(value.name for value in dict_sig.values() for key in sig_list))
    pass


# if "context" in dict_sig.values():


def helper_sig_class(name_class):

    sig = inspect.getfullargspec(name_class).annotations

    return sig


def helper_sig_def(name_def):

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
        (walk_yaml_with_no_order),
        (walk_yaml_in_order),
    ],
    ids=["Signature without order", "Signature with order"],
)
def test_sig_walk_n_order(name_def):

    walk_n_order_sig, sig = helper_sig_def(name_def=name_def)

    sig_list = ["current_data", "new_data", "context", "depth"]

    sig_obj = sig.parameters["context"]
    dict_walk_n_order = dict(walk_n_order_sig)

    assert all(value.name for value in dict_walk_n_order.values() for _ in sig_list)
    assert ("context", sig_obj) in dict_walk_n_order.items()

    # TODO ADD TEST CASES FOR THESE TOO: (check for assert above too.)
    # 1) accept_n_key = helper_sig_class(name_class=validator.accept_new_keys)

    # 2) accept_n_val = helper_sig_class(name_class=validator.accept_new_value)
