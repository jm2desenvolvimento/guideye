import io
import os
import time
import cv2
from gtts import gTTS
import pygame
import speech_recognition as sr
import openai
import google.generativeai as genai
from PIL import Image

# ===============================
# Gerenciamento de Voz (TTS)
# ===============================
class TTSManager:
    def __init__(self, lang="pt-br"):
        pygame.mixer.init()
        self.lang = lang 

    def say(self, text):
        try:
            f = io.BytesIO()
            tts = gTTS(text=text, lang=self.lang, slow=False)
            tts.write_to_fp(f)
            f.seek(0)
            sound = pygame.mixer.Sound(f)
            sound.play()
            # Aguarda o término da reprodução
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            f.close()
        except Exception as e:
            print(f"[TTS] Erro: {e}")

# ===============================
# Reconhecimento de Fala
# ===============================
class SpeechRecognizer:
    def __init__(self, tts_manager):
        self.recognizer = sr.Recognizer()
        self.tts = tts_manager
        self.initial_prompt_given = False

    def recognize(self, timeout=5):
        with sr.Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(mic)
            if not self.initial_prompt_given:
                self.initial_prompt_given = True
            try:
                audio = self.recognizer.listen(mic, timeout=timeout)
                text = self.recognizer.recognize_google(audio, language="pt-BR")
                print("[Fala reconhecida]:", text)
                return text
            except sr.WaitTimeoutError:
                print("[Fala] Tempo limite de espera atingido.")
                #self.tts.say("Não foi detectada fala no tempo esperado, por favor tente novamente.")
                return ""
            except sr.UnknownValueError:
                print("[Fala] Áudio não reconhecido.")
                #self.tts.say("Não consegui entender o que foi dito, tente novamente.")
                return ""
            except sr.RequestError as e:
                print(f"[Fala] Erro no serviço: {e}")
                self.tts.say("Erro ao processar o áudio, tente novamente mais tarde.")
                return ""

# ===============================
# Captura e Carregamento de Imagem
# ===============================
class ImageCapturer:
    def __init__(self):
        pass

    def capture(self, filename="cenario.jpg"):
        sistema = os.name
        if sistema == "posix":
            # Para Linux/Ubuntu usando libcamera
            os.system(f"libcamera-still -t 500 -o {filename}")
            if os.path.exists(filename):
                return filename
            else:
                print("[Imagem] Erro ao capturar imagem com libcamera.")
                return None
        else:
            # Para Windows (ou outros) usando OpenCV
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(filename, frame)
                return filename
            else:
                print("[Imagem] Erro ao capturar imagem com OpenCV.")
                return None

    def load_image(self, filename):
        try:
            return Image.open(filename)
        except Exception as e:
            print(f"[Imagem] Erro ao abrir {filename}: {e}")
            return None

# ===============================
# Cliente ChatGPT (OpenAI)
# ===============================
class ChatGPTClient:
    def __init__(self, api_key):
        openai.api_key = api_key

    def get_response(self, prompt, max_tokens=100):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.5
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[ChatGPT] Erro: {e}")
            return "Desculpe, não consegui obter uma resposta."

# ===============================
# Cliente Gemini
# ===============================
class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_response(self, prompt, image=None):

        try:
            inputs = [prompt]
            if image:
                inputs.append(image)
            print("gemini chamado")
            response = self.model.generate_content(inputs)
            print('gemini respondeu')
            return response.text.strip()
        except Exception as e:
            print(f"[Gemini] Erro: {e}")
            return "Desculpe, não consegui processar a imagem."

# ===============================
# Reconhecimento Facial
# ===============================
class FaceRecognizer:
    def __init__(self, model_path, tts):
        from FaceRecognition.model import prediction
        self.recognizer = prediction.RealTimeFaceRecognition(model_path=model_path)
        self.tts = tts

    def recognize(self):
        self.tts.say("Iniciando reconhecimento facial.")
        self.recognizer.recognize_from_camera()

    def add_person(self):
        self.tts.say("Iniciando adição de nova pessoa ao banco de dados.")
        self.recognizer.add_person_to_db()

# ===============================
# Handler de Comandos
# ===============================
def handle_command(command, tts, image_cap, face_recog, chat_client, gemini_client):
    """
    Interpreta o comando reconhecido e delega para a função correspondente.
    """
    if "foto" in command:
        filename = image_cap.capture("cenario.jpg")
        if filename:
            tts.say("Foto capturada com sucesso.")
        else:
            tts.say("Falha ao capturar a foto.")
    
    elif "reconhecer" in command:
        face_recog.recognize()
    
    elif "adicionar" in command:
        face_recog.add_person()
    
    elif "leia" in command:
        filename = image_cap.capture("leia.jpg")
        if filename:
            image = image_cap.load_image(filename)
            if image:
                response = gemini_client.get_response("Extraia o texto da imagem responda em portugês brasileiro.", image=image)
                print(response)
                tts.say(response)
            else:
                tts.say("Erro ao carregar a imagem para leitura.")
        else:
            tts.say("Falha ao capturar a imagem.")
    
    elif "assistente" in command:
        prompt = "Responda a seguinte questão em até 2 linhas: " + command.replace("assistente", "").strip()
        response = chat_client.get_response(prompt)
        tts.say(response)
    
    elif "cenário" in command:
        filename = image_cap.capture("cenario.jpg")
        if filename:
            image = image_cap.load_image(filename)
            if image:
                response = gemini_client.get_response("Descreva o que você vê nesta imagem de forma breve e curta fale apenas o necessário não cite o que foi pedido", image=image)
                print(response)
                tts.say(response)
            else:
                tts.say("Erro ao carregar a imagem do cenário.")
        else:
            tts.say("Falha ao capturar o cenário.")
    
    elif "detalhar" in command:
        prompt = "Seja breve e responda: " + command.replace("detalhar", "").strip()
        filename = "cenario.jpg"
        if os.path.exists(filename):
            image = image_cap.load_image(filename)
            if image:
                response = gemini_client.get_response(prompt, image=image)
                print(response)
                tts.say(response)
            else:
                tts.say("Erro ao carregar a imagem para detalhamento.")
        else:
            tts.say("Nenhuma imagem capturada anteriormente para detalhar.")
    
    else:
        tts.say("Comando não reconhecido.")
