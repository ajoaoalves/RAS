import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any
from jsonschema import validate, ValidationError
from jsonschema.exceptions import SchemaError

def load_schema():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "schemas/request_schema.json"), 'r') as file:
        return json.load(file)

@dataclass
class ToolProcessingRequest:
    messageId: str
    timestamp: str
    procedure: str
    parameters: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.timestamp, datetime):
            self.timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%SZ")

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def from_json(data: str):
        
        msgJson = json.loads(data)
        schema = load_schema()

        try:
            validate(instance=msgJson, schema=schema)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e.message}")
        except SchemaError as e:
            raise ValueError(f"Schema error: {e.message}")
        
        return ToolProcessingRequest(**msgJson)