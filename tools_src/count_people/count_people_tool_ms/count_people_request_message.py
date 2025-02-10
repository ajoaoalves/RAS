from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class CountPeopleParameters(BaseModel):
    inputImageURI: str


CountPeopleRequestMessage = RequestMessage[CountPeopleParameters]
