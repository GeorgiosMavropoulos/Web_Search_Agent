"""This file contains a function to convert json to python dict"""
import json
from types import SimpleNamespace
def to_obj(json_input):
    """
    Converts a JSON string or a dictionary into a Python object with dot notation.
    """
    try:
        # If it's a string, load it into a dictionary first
        if isinstance(json_input, (str, bytes)):
            json_input = json.loads(json_input)
            
        # Recursively convert dictionaries to SimpleNamespace objects
        return json.loads(json.dumps(json_input), object_hook=lambda d:SimpleNamespace(**d))
    except Exception as e:
        raise RuntimeError('Error, cannot convert json to dictionary') from e
