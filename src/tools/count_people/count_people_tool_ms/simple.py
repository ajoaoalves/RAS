import cv2
from ultralytics import YOLO


def contar_pessoas(imagem_path):
    # Carregar o modelo pré-treinado YOLO
    modelo = YOLO('yolov8n.pt')  # Modelo YOLOv8

    # Carregar a imagem
    imagem = cv2.imread(imagem_path)
    if imagem is None:
        raise FileNotFoundError("Imagem não encontrada.")

    # Fazer previsões
    resultados = modelo(imagem)

    # Filtrar detecções de pessoas
    deteccoes = resultados[0].boxes  # Obter as caixas delimitadoras
    pessoas = [
        box for box in deteccoes 
        if int(box.cls) in modelo.names and modelo.names[int(box.cls)] == 'person'
    ]

    # Retornar o número de pessoas
    return len(pessoas), imagem

# Exemplo de uso
if __name__ == "__main__":
    imagem_path = r"C:\Users\super\OneDrive\Ambiente de Trabalho\Uni\Mestrado\RAS\picturas-watermark-tool-ms\usage_example\images\src\image-7.jpg"
    try:
        num_pessoas, imagem = contar_pessoas(imagem_path)
        print(f"Número de pessoas detectadas: {num_pessoas}")
    except Exception as e:
        print(f"Erro: {e}")
