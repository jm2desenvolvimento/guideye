import cvlib as cv
from cvlib.object_detection import draw_bbox
import speech_recognition as sr
import cv2
import pyttsx3
import openai
import mediapipe as mp
import time
import wikipedia
import os
import numpy as np
from traducao import traducao_etiquetas
from funcoes import convertVoz, gerar_resposta, reconhecerVoz, buscarChatgpt, opcao_assistente, opcao_cenario, opcao_interacao
from webserver import capturarImagem
from FaceRecognition.model import prediction, extractor


# Inicialize a chave da API OpenAI
openai.api_key = "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"

rec = sr.Recognizer()
cont = 0

texto = ''
recognizer = prediction.RealTimeFaceRecognition(model_path=r"FaceRecognition\model\keras\facenet_keras.h5")

while True:
    texto = reconhecerVoz()
    print(texto)
    command = texto.lower()
   
    if command:
        match command:
            case command if "foto" in command:
                sistema = os.name
                if sistema == 'posix':  # Linux/Ubuntu
                    os.system("libcamera-still -t 500 -o cenario.jpg")
                    caminho_imagem = '/home/tutvision/Desktop/APLICATIVO/cenario.jpg'
                else: 
                    print(sistema)
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    if ret:
                        cv2.imwrite('cenario.jpg', frame)
                        cap.release()
                    caminho_imagem = 'cenario.jpg'
                    convertVoz("foto feita com sucesso")

            case command if "reconhecer" in command:
                convertVoz("Iniciando reconhecimento de rosto.")
                recognizer.recognize_from_camera()
                
            case command if "adicionar" in command:
                convertVoz("Iniciando adição de nova pessoa ao banco de dados.")
                recognizer.add_person_to_db()

            case command if 'leia' in command:
                convertVoz("Iniciando leitura.")
                ocr_processor = extractor.OCRProcessor(language='pt')
                text = ocr_processor.process()
                convertVoz(text)

            case command if "assistente" in command:
                texto = command.replace('assistente', '', 1)
                opcao_assistente("Responda a seguinte questão no máximo em 2 linhas: " + texto)

            case command if "cenário" in command:
                opcao_cenario()

            case command if "detalhar" in command:
                convertVoz("Você escolheu a opção detalhar")
               
                
                opcao_interacao(command.replace("detalhar",""))
            

            case _:
                pass
