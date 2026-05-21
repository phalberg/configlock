def traverse(node):
    if isinstance(node, dict):
        for key, value in node.items():
            print(f"Entering Key: {key}")
            traverse(value)
    elif isinstance(node, list):
        for item in node:
            traverse(item)
    else:
        # This is a leaf node (string, int, etc.)
        print(f"Value: {node}")
