import easyocr
import io
from PIL import Image as Img
import cv2
import numpy as np


class Image:
    """
    Classe para abrir imagens em formato PIL a partir de bytes.
    """

    def __init__(self, image_bytes=None, cv2_frame=None) -> None:
        self.image_bytes = image_bytes
        self.cv2_frame = cv2_frame

    def open(self) -> Img:
        try:
            if self.image_bytes:
                image_pil = Img.open(io.BytesIO(self.image_bytes))
            elif self.cv2_frame is not None:
                image_rgb = cv2.cvtColor(self.cv2_frame, cv2.COLOR_BGR2RGB)
                image_pil = Img.fromarray(image_rgb)
            else:
                raise ValueError("Nenhum dado de imagem foi fornecido")
            return image_pil
        except Exception as e:
            print(f"Erro ao abrir a imagem: {e}")
            return None


class DocumentInfoExtractor:
    """
    Classe para extrair texto de uma imagem usando EasyOCR.
    """

    def __init__(self, image: Img, language='pt'):
        self.reader = easyocr.Reader([language])
        self.image = image
        self.text = self.extract_text()

    def extract_text(self):
        try:
            # Converte a imagem PIL para array do NumPy
            image_np = np.array(self.image)
            result = self.reader.readtext(image_np, detail=0)
            return " ".join(result)
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
            return ""


class CameraCapture:
    """
    Classe para capturar imagens da câmera usando OpenCV.
    """

    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)

    def capture_frame(self):
        status, frame = self.camera.read()
        if status:
            return frame
        else:
            print("Erro ao acessar a câmera")
            return None

    def release(self):
        self.camera.release()


class OCRProcessor:
    """
    Classe principal para processar OCR a partir de imagens capturadas pela câmera.
    """

    def __init__(self, language='pt'):
        self.language = language
        self.camera = CameraCapture()

    def process(self):
        frame = self.camera.capture_frame()
        if frame is not None:
            image = Image(cv2_frame=frame).open()
            if image:
                #cv2.imshow('Imagem Capturada - OpenCV', frame)
                #image.show()

                extractor = DocumentInfoExtractor(image, language=self.language)
                print(extractor.extract_text())
                return extractor.extract_text()

        self.camera.release()

