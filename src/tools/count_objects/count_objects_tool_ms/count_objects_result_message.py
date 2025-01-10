from typing import Dict
from typing import Any


from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .count_objects_request_message import CountObjectsRequestMessage


class CountObjectsResultOutput(BaseModel):
    type: str
    counts: Dict[str, int]  


class CountObjectsResultMessage(ResultMessage[CountObjectsResultOutput]):

    def __init__(self, request: CountObjectsRequestMessage, tool_result: Any, exception: Exception, *args):
        """
        Inicializa a mensagem de resultado para a contagem de pessoas.

        Args:
            request (CountObjectsRequestMessage): Mensagem de solicitação com os parâmetros da imagem.
            tool_result (Any): Resultado da execução da ferramenta, incluindo o número de pessoas detectadas.
            exception (Exception): Exceção, caso ocorra algum erro durante o processamento.
        """
        super().__init__(request, tool_result, exception, *args)
        
        if exception is None:
            # Criar a resposta com o número de pessoas detectadas
            self.output = CountObjectsResultOutput(
                type="dict",
                count=tool_result
            )
