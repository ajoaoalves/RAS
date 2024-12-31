import json
import os
from dateutil import parser
from dataclasses import dataclass
from typing import Optional, Dict, Union, Literal
from jsonschema import validate, ValidationError
from jsonschema.exceptions import SchemaError

def load_schema():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "schemas/result_schema.json"), 'r') as file:
        return json.load(file)


@dataclass
class Output:
    type: Literal["image", "number", "json", "text", "other"]
    imageURI: Optional[str] = None
    value: Optional[Union[str, float, dict, None]] = None


@dataclass
class Error:
    code: str = ""
    message: Optional[str] = None
    details: Optional[Dict[str, str]] = None


@dataclass
class Metadata:
    processingTime: Optional[float] = None
    microservice: Optional[str] = None


@dataclass
class ToolProcessingResult:
    messageId: str = ""
    correlationId: str = ""
    timestamp: str = ""
    status: str = ""
    output: Optional[Output] = None
    error: Optional[Error] = None
    metadata: Optional[Metadata] = None

    def __post_init__(self):
        self.setTimestamp(self.timestamp)

    def setTimestamp(self, timestampStr: str):
        try:
            self.timestamp = parser.parse(timestampStr).strftime("%Y-%m-%d %H:%M:%SZ")
        except parser.ParserError:
            self.timestamp = ""

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
        
        return ToolProcessingResult(**msgJson)