def validate_goal_form(form_data):
    errors = {}
    try:
        target_value = int(form_data.get("target_value") or form_data.get("target", 0))
    except (ValueError, TypeError):
        errors["target_value"] = "Must be a number."
        target_value = 0

    try:
        current = int(form_data.get("current") or 0)
    except (ValueError, TypeError):
        current = 0

    if target_value <= 0:
        errors["target_value"] = "Target must be greater than 0."

    if current > target_value:
        errors["current"] = "Current progress cannot exceed target value."

    return errors, target_value, current
