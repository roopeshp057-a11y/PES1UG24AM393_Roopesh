import json
import math

def calculate_dimensional_weight(dimensions_str):
    """
    Calculate dimensional weight (kg) from a dimensions string formatted as LxWxH in cm.
    Formula: round((length * width * height) / 5000.0, 2)
    Returns None if the input is invalid, malformed, non-positive, or cannot be parsed.
    """
    if not isinstance(dimensions_str, str):
        return None
    try:
        parts = dimensions_str.strip().split('x')
        if len(parts) != 3:
            parts = dimensions_str.strip().split('X')
        if len(parts) != 3:
            return None
        length = float(parts[0].strip())
        width = float(parts[1].strip())
        height = float(parts[2].strip())
        if length <= 0 or width <= 0 or height <= 0:
            return None
        if math.isnan(length) or math.isnan(width) or math.isnan(height) or \
           math.isinf(length) or math.isinf(width) or math.isinf(height):
            return None
        return round((length * width * height) / 5000.0, 2)
    except (ValueError, TypeError, OverflowError, AttributeError):
        return None

def format_tracking_label(raw_code):
    """
    Format a raw tracking code into the standard label format: <PREFIX>-<6-digit number>.
    Example: 'E123' -> 'E-000123'.
    Returns None if the input is invalid or malformed.
    """
    if not isinstance(raw_code, str):
        return None
    raw_code = raw_code.strip()
    if len(raw_code) < 2:
        return None
    prefix = raw_code[0].upper()
    if not prefix.isalpha():
        return None
    try:
        tracking_num = int(raw_code[1:])
        if tracking_num < 0:
            return None
        return f"{prefix}-{tracking_num:06d}"
    except (ValueError, TypeError, OverflowError):
        return None

def parse_package_manifest(json_payload):
    """
    Parse a JSON manifest payload and extract package weight as a positive float.
    Example: '{"weight": 12.5}' -> 12.5.
    Returns None if the payload is invalid, missing 'weight', non-positive, or malformed.
    """
    if not isinstance(json_payload, str):
        return None
    try:
        data = json.loads(json_payload)
        if not isinstance(data, dict) or "weight" not in data:
            return None
        weight = float(data["weight"])
        if math.isnan(weight) or math.isinf(weight) or weight <= 0:
            return None
        return weight
    except (json.JSONDecodeError, ValueError, TypeError, OverflowError):
        return None

def main():
    print("==== Running calculate_dimensional_weight ====")
    dims_input = input("Enter dimensions LxWxH in cm (e.g. 20x30x10): ")
    dim_weight = calculate_dimensional_weight(dims_input)
    print("Dimensional Weight (kg):", dim_weight)

    print("\n==== Running format_tracking_label ====")
    code_input = input("Enter raw code (e.g. E123): ")
    label = format_tracking_label(code_input)
    print("Formatted Label:", label)

    print("\n==== Running parse_package_manifest ====")
    json_input = input('Enter manifest JSON (e.g. {"weight": 12.5}): ')
    weight = parse_package_manifest(json_input)
    print("Manifest Weight:", weight)

if __name__ == "__main__":
    main()
