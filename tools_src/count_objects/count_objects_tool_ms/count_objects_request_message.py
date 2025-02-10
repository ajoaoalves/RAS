from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class CountObjectsParameters(BaseModel):
    inputImageURI: str


CountObjectsRequestMessage = RequestMessage[CountObjectsParameters]
