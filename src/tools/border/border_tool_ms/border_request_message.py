from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class borderParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    bordersize: int 
    bordercolor: str

BorderRequestMessage = RequestMessage[borderParameters]
