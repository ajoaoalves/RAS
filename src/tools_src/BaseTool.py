import cv2
import shutil
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum
from messages.ToolProcessingRequest import *
from messages.ToolProcessingResult import *

class BaseTool(ABC):

    def __init__(self):
        self.startTime = datetime.now(timezone.utc)
        self.result = ToolProcessingResult()
        self.request: ToolProcessingRequest = None
        self.inputImage: str = None
        self.outputImage: str = None

    def onProcessStart(self, requestJson: str, microServiceID) -> bool:
        try:
            self.result.metadata = Metadata(microservice=microServiceID)
            self.request = ToolProcessingRequest.from_json(requestJson)
            self.result.correlationId = self.request.messageId
            self.result.messageId = "completion-" + self.request.messageId.split("-")[-1]
            return True
        except ValueError:
            self.result.error = Error(code=str(self.Error.INVALID_REQUEST), message="Unable to parse request")
            return False


    @abstractmethod
    def process(self) -> str:
        pass


    def onProcessSuccess(self) -> str:
        self.result.status = "success"
        return self.onProcessFinished()


    def onProcessError(self) -> str:
        self.result.status = "error"
        return self.onProcessFinished()


    def onProcessFinished(self):
        self.updateTimestamps()
        self.deleteImages()
        return self.result.to_json()


    def updateTimestamps(self):
        now = datetime.now(timezone.utc)
        self.result.timestamp = now.strftime("%Y-%m-%d %H:%M:%SZ")
        elapsed = now - self.startTime
        self.result.metadata.processingTime = str(elapsed.total_seconds())


    def deleteImages(self):
        if (self.inputImage != None):
            os.remove(self.inputImage)
        if (self.outputImage != None):
            os.remove(self.outputImage)


    def downloadImage(self, uri: str) -> cv2.UMat:
        # TODO: download image from server, save it to disk and return the decoded Mat. For now copy and decode local image for testing purposes
        srcImage = os.path.join(os.path.dirname(os.path.abspath(__file__)), uri)
        base_name, extension = os.path.splitext(srcImage)
        self.inputImage = f"{base_name}(2){extension}"
        shutil.copyfile(srcImage, self.inputImage)
        return cv2.imread(self.inputImage)
    

    def uploadImage(self, imageMat: cv2.UMat, uri: str) -> str:
        self.outputImage = os.path.join(os.path.dirname(os.path.abspath(__file__)), uri)
        cv2.imwrite(self.outputImage, imageMat)
        # TODO: upload the saved image to the server


    class Error(Enum):
        INVALID_REQUEST = 1
        DOWNLOAD_ERROR = 2
        INVALID_INPUT_URI = 3
        INVALID_INPUT_IMAGE = 4
        INVALID_PARAMETERS = 5
        PROCESSING_ERROR = 6
        ENCODING_ERROR = 7
        UPLOAD_ERROR = 8