from BaseTool import *
import cv2

class ResizeTool(BaseTool):

    microServiceID = "picturas-resize-tool-ms"

    def process(self) -> str:

        # dowload and decode input image
        inputImageURI = self.request.parameters.get("inputImageURI")
        image = self.downloadImage(inputImageURI)

        # read resize parameters
        width = int(self.request.parameters.get("width"))
        height = int(self.request.parameters.get("height"))

        # resize image
        resizedImage = cv2.resize(image, (width, height))

        # show output - testing only
        cv2.imshow('Resized Image', resizedImage)
        cv2.waitKey(0)
        
        # encode and upload output image
        outputImageURI = self.request.parameters.get("outputImageURI")
        self.uploadImage(resizedImage, outputImageURI)

        # update output message
        self.result.output = Output(type="image", imageURI=outputImageURI)

        # finish process
        return self.onProcessSuccess()
    

request = """{
                "messageId": "request-1",
                "timestamp": "2024-12-30T22:08:00Z",
                "procedure": "resize",
                "parameters": {
                    "inputImageURI": "../../test_images/two_people.jpg",
                    "outputImageURI": "../../test_images/two_people_resize_output.jpg",
                    "width": 200,
                    "height": 200
                }
            }"""

resizeTool = ResizeTool()

if not resizeTool.onProcessStart(request, ResizeTool.microServiceID):
    print(resizeTool.onProcessError())
else:
    print(resizeTool.process())