import cvlib as cv
import cv2
from matplotlib import pyplot as plt

# Carregue uma imagem de exemplo
imagem = cv2.imread('./marcos.png')

# Verifique se a imagem foi carregada corretamente
if imagem is not None:
    bbox, label, conf = cv.detect_common_objects(imagem)
    # Restante do código...
else:
    print('Erro ao carregar a imagem.')
