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

    # Initialize a dictionary to store counts
    counts = {}

        # Iterate over all detections
    detections = resultados[0].boxes
    for box in detections:
        class_id = int(box.cls)
        class_name = modelo.names[class_id]
        # Increment the count for the detected class
        counts[class_name] = counts.get(class_name, 0) + 1
    

    # Retornar o número de objects
    return counts, imagem

# Exemplo de uso
if __name__ == "__main__":
    imagem_path = r"../../../../test_images/pedalar-1.jpg"
    try:
        num_objects, imagem = contar_objectos(imagem_path)
        print(f"Objectos detectados: {num_objects}")
    except Exception as e:
        print(f"Erro: {e}")
