def apply_transformations(text, transformations):
    for t in transformations:
        action = t.get("action")
        if action == "strip":
            text = text.strip()
        elif action == "lowercase":
            text = text.lower()
        elif action == "cause_error":
            raise ValueError("Artificial error triggered for testing.")
        else:
            raise ValueError(f"Unknown transformation action: {action}")
    return text