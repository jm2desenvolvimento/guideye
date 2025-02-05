import os
import time
import cv2
from funcoes import (
    TTSManager,
    SpeechRecognizer,
    ImageCapturer,
    ChatGPTClient,
    GeminiClient,
    FaceRecognizer,
    handle_command
)

def main():
    # Inicializa os módulos e recursos
    tts = TTSManager()
    speech_recognizer = SpeechRecognizer(tts)
    image_capturer = ImageCapturer()
    chat_client = ChatGPTClient(api_key="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")
    gemini_client = GeminiClient(api_key="AIzaSyB6rCSWCUmEtQFJT0CtwY_jvWl2oiYObVo")
    face_recog = FaceRecognizer(model_path=r"FaceRecognition/model/keras/facenet_keras.h5", tts=tts)

    # Mensagem inicial (falada apenas uma vez)
    tts.say("Por favor, diga um comando: Assistente, Cenário, Foto, Reconhecer, Adicionar, Detalhar ou Leia.")

    while True:
        command = speech_recognizer.recognize().lower()
        if command:
            print("Comando:", command)
            handle_command(command, tts, image_capturer, face_recog, chat_client, gemini_client)
        #time.sleep(0.5)

if __name__ == "__main__":
    main()
