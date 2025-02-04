import pyttsx3
import speech_recognition as sr
import openai
import cv2
import wikipedia
import os
import io
from gtts import gTTS
import time
import google.generativeai as genai
from PIL import Image


'''def convertVoz(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()
    print(texto)'''
    
    
'''def convertVoz(texto, lang='pt-br', speed=10):
    print('pass')
    tts = gTTS(text=texto, lang=lang, slow=True) 
    tts.speed = speed
    tts.save('saida.mp3')
    os.system("ffmpeg -y -i saida.mp3 -acodec pcm_s16le -ar 44100 -ac 2 saida.wav")
    os.system('aplay saida.wav')
'''
import pygame
def convertVoz(texto, lang='pt-br'):
    
    pygame.mixer.init()
    
    f = io.BytesIO()  # Create the file-like object
    try:
        tts = gTTS(text=texto, lang=lang, slow=False)
        tts.write_to_fp(f)
        f.seek(0)

        sound = pygame.mixer.Sound(f)
        sound.play()
    except Exception as e: 
        convertVoz("não encontrei nenhum texto")
    finally:
        f.close()  
    print('end func')

def gerar_resposta(messages):
    print('api openai')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


def buscarChatgpt(messages):
    print('buscarChatgpt')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

count = 0
def reconhecerVoz():
    global count 
    if count == 0:
        convertVoz("Por favor, fale Assistente, Cenário, foto,reconhecer ou adicionar,detalhar ou leia.")
        count += 1
    
    rec = sr.Recognizer()

    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        texto = ""
        while True:
            try:

                audio = rec.listen(mic)
                texto = new_func(rec, audio)
                print("Texto reconhecido:", texto)
                break
            except sr.UnknownValueError:
                print("Não foi possível reconhecer o áudio.")
                # convertVoz("Não foi possível reconhecer o áudio.")
                continue

    return texto




def new_func(rec, audio):
    return rec.recognize_google(audio, language="pt-BR")


def opcao_assistente(msg):
    while True:
        # convertVoz("Fale")
        # try:
        #    texto_gpt = reconhecerVoz()
        # except sr.UnknownValueError:
        #    print("Não foi possível reconhecer o áudio.")
        #    convertVoz("Não foi possível reconhecer o áudio.")

        variavel = f"{msg}"
        mensagens = [
            {"role": "system", "content": variavel}]
        wiki = [
            {"role": "system", "content": "Extraia duas palavras-chave deste texto: "}]

        mensagens.append({"role": "user", "content": str(variavel)})
        answer = gerar_resposta(mensagens)
        print("ChatGPT:", answer[0])
        convertVoz(answer[0])
        # convertVoz("Completando a resposta")
        # try:
        #     wikipedia.set_lang('pt')
        #     wiki.append({"role": "user", "content": str(variavel)})
        #     texto_gpt = buscarChatgpt(wiki)
        #     resultado = wikipedia.summary(variavel[0], 2)
        #     convertVoz(resultado)
        # except:
        #     convertVoz("Sem complemento")

        break


def inicializar_gemini():
    """Inicializa e configura o modelo Gemini"""
    genai.configure(api_key='AIzaSyB6rCSWCUmEtQFJT0CtwY_jvWl2oiYObVo')
    return genai.GenerativeModel('gemini-1.5-flash')

def opcao_cenario():
    # Detecta o sistema operacional
    sistema = os.name

    # Captura a imagem de acordo com o sistema operacional
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

    # Usar o modelo Gemini inicializado
    model = inicializar_gemini()
    
    # Carregar a imagem usando PIL
    imagem = Image.open(caminho_imagem)
    
    # Fazer a pergunta ao Gemini
    prompt = """
    fale o que você vê nesta imagem. 
    
    """
    
    response = model.generate_content([prompt, imagem])
    objetos_detectados = response.text
    

    

    convertVoz(objetos_detectados)

def opcao_leia():
    # Detecta o sistema operacional
    sistema = os.name

    # Captura a imagem de acordo com o sistema operacional
    if sistema == 'posix':  # Linux/Ubuntu
        os.system("libcamera-still -t 500 -o leia.jpg")
        caminho_imagem = '/home/tutvision/Desktop/APLICATIVO/leia.jpg'
    else: 
        print(sistema)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('leia.jpg', frame)
            cap.release()
        caminho_imagem = 'leia.jpg'

    # Usar o modelo Gemini inicializado
    model = inicializar_gemini()
    
    # Carregar a imagem usando PIL
    imagem = Image.open(caminho_imagem)
    
    # Fazer a pergunta ao Gemini
    prompt = """
    retorne o texto da imagem 
    
    """
    
    response = model.generate_content([prompt, imagem])
    objetos_detectados = response.text
    

    

    convertVoz(objetos_detectados)
    


def opcao_interacao(msg):
    print("opcao_interacao")
    # Detecta o sistema operacional
    sistema = os.name
    
    # Define o caminho da imagem baseado no sistema operacional
    if sistema == 'posix':  # Linux/Ubuntu
        caminho_imagem = '/home/tutvision/Desktop/APLICATIVO/cenario.jpg'
    else:  # Windows
        caminho_imagem = 'cenario.jpg'
    
    try:
        # Carregar a imagem usando PIL
        imagem = Image.open(caminho_imagem)
        
        # Inicializar o modelo Gemini
        model = inicializar_gemini()
        
        # Configurar prompt para o Gemini
        prompt = f"""
        Analise esta imagem e responda duvidas e perguntas do usuário sobre.
        seja o mais direto e breve póssível.
        duvida ou msg do usuário: {msg}
    
        """
        
        # Gerar resposta do Gemini
        response = model.generate_content([prompt, imagem])
        sugestoes = response.text
        
        print("Sugestões de interação:", sugestoes)
        convertVoz(sugestoes)
        
    except FileNotFoundError:
        erro = "Desculpe, não foi possível encontrar a imagem capturada anteriormente."
        print(erro)
        convertVoz(erro)
    except Exception as e:
        erro = f"Desculpe, ocorreu um erro ao analisar a imagem: {str(e)}"
        print(erro)
        convertVoz(erro)
