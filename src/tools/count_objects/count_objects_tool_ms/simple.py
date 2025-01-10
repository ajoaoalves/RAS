import cv2
from ultralytics import YOLO


def contar_objectos(imagem_path):
    # Carregar o modelo pré-treinado YOLO
    modelo = YOLO('yolov8n.pt')  # Modelo YOLOv8

    # Carregar a imagem
    imagem = cv2.imread(imagem_path)
    if imagem is None:
        raise FileNotFoundError("Imagem não encontrada.")

    # Fazer previsões
    resultados = modelo(imagem)

    # Filtrar detecções de objectos
    deteccoes = resultados[0].boxes  # Obter as caixas delimitadoras
    objectos = [
        box for box in deteccoes 
        if int(box.cls) in modelo.names and modelo.names[int(box.cls)] == 'objects'
    ]

    # Retornar o número de objects
    return len(objectos), imagem

# Exemplo de uso
if __name__ == "__main__":
    imagem_path = r"../../../../test_images/pedalar-1.jpg"
    try:
        num_objects, imagem = contar_objectos(imagem_path)
        print(f"Objectos detectados: {num_objects}")
    except Exception as e:
        print(f"Erro: {e}")
