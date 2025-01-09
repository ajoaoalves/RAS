from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .count_people_request_message import CountPeopleRequestMessage


class CountPeopleResultOutput(BaseModel):
    type: str
    count: int


class CountPeopleResultMessage(ResultMessage[CountPeopleResultOutput]):

    def __init__(self, request: CountPeopleRequestMessage, tool_result: Any, exception: Exception, *args):
        """
        Inicializa a mensagem de resultado para a contagem de pessoas.

        Args:
            request (CountPeopleRequestMessage): Mensagem de solicitação com os parâmetros da imagem.
            tool_result (Any): Resultado da execução da ferramenta, incluindo o número de pessoas detectadas.
            exception (Exception): Exceção, caso ocorra algum erro durante o processamento.
        """
        super().__init__(request, tool_result, exception, *args)
        
        if exception is None:
            # Criar a resposta com o número de pessoas detectadas
            self.output = CountPeopleResultOutput(
                type="int",
                count=tool_result
            )
