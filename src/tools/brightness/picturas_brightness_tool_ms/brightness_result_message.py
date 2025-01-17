from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .brightness_request_message import BrightnessRequestMessage


class BrightnessResultOutput(BaseModel):
    type: str
    imageURI: str



class BrightnessResultMessage(ResultMessage[BrightnessResultOutput]):

    def __init__(self, request: BrightnessRequestMessage, tool_result: Any, exception: Exception, *args):
        """
        Inicializa a mensagem de resultado para a mudanca de brilho.

        Args:
            request (BrightnessRequestMessage): Mensagem de solicitação com os parâmetros da imagem.
            tool_result (Any): Resultado da execução da ferramenta, incluindo o número de pessoas detectadas.
            exception (Exception): Exceção, caso ocorra algum erro durante o processamento.
        """
        super().__init__(request, tool_result, exception, *args)
        
        if exception is None:
            # Criar a resposta com o número de pessoas detectadas
            self.output = BrightnessResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
