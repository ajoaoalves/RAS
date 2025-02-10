from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .remove_background_request_message import RemoveBackgroundRequestMessage


class RemoveBackgroundResultOutput(BaseModel):
    type: str
    imageURI: str



class RemoveBackgroundResultMessage(ResultMessage[RemoveBackgroundResultOutput]):

    def __init__(self, request: RemoveBackgroundRequestMessage, tool_result: Any, exception: Exception, *args):
        """
        Inicializa a mensagem de resultado.

        Args:
            request (RemoveBackgroundRequestMessage): Mensagem de solicitação com os parâmetros da imagem.
            tool_result (Any): Resultado da execução da ferramenta.
            exception (Exception): Exceção, caso ocorra algum erro durante o processamento.
        """
        super().__init__(request, tool_result, exception, *args)
        
        if exception is None:
            # Criar a resposta
            self.output = RemoveBackgroundResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
