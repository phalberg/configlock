
import inspect

from configlock import validator


def helper_sig(name_class) -> inspect.Signature:
    
    sig = inspect.getfullargspec(name_class).annotations
    
    return sig


def test_sig_context():
    
    val_context_sig = helper_sig(name_class=validator.ValidationContext)
    
    sig_list = ["new_path", "current_path", "order_matters"]
    
    assert ("return", None) in val_context_sig.items()
    assert(all(key in val_context_sig for key in sig_list))
    assert ("new_path", str) in val_context_sig.items()
    assert ("current_path", str) in val_context_sig.items()
    
    
def test_sig_walk_n_order():
    
    
    walk_n_order_sig = helper_sig(name_class=validator.walk_yaml_with_no_order)
    
    
    sig_list = ["current_data", "new_data", "context", "depth"]
    
    assert(all(key in walk_n_order_sig for key in sig_list))
    assert ("context", validator.ValidationContext) in walk_n_order_sig.items()
    
    
    
def test_sig_walk_w_order():
    
    walk_w_order = helper_sig(name_class=validator.walk_yaml_in_order)

    
    sig_list = ["current_data", "new_data", "context", "depth"]
    
    assert(all(key in walk_w_order for key in sig_list))
    assert ("context", validator.ValidationContext) in walk_w_order.items()
    
    
    
    
    
    accept_n_key  = helper_sig(name_class=validator.accept_new_keys)
    
    
    accept_n_val = helper_sig(name_class=validator.accept_new_value)
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    #print(inspect.getfullargspec(validator.ValidationContext))
    sig = inspect.getfullargspec(validator.ValidationContext).annotations
    print(sig)
    print("new_path" in sig)
    print( ("return", None) in sig.items())
    print(helper_sig(name_class=validator.walk_yaml_with_no_order))
    print(inspect.signature(validator.walk_yaml_in_order(0,0,0)))
