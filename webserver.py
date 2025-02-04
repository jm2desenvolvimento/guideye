import requests


def capturarImagem():
    # Endereço IP da ESP32
    # esp32_ip = "192.168.0.56"  # 156
    # esp32_ip = "192.168.0.156"  # 156
    esp32_ip = "192.168.0.104"  # 156
    # esp32_ip = "192.168.0.164"  # 156
    # esp32_ip = "192.168.0.xxxx"  # 156

    # URL da imagem
    url = f"http://{esp32_ip}"

    try:
        # Realiza a solicitação HTTP GET para baixar a imagem
        response = requests.get(url)

        # Verifica se a solicitação foi bem-sucedida (código de resposta 200)
        if response.status_code == 200:
            # Nome do arquivo onde a imagem será salva localmente
            nome_arquivo = "photo.jpg"

            # Abre o arquivo em modo binário e escreve os dados da imagem nele
            with open(nome_arquivo, 'wb') as arquivo:
                arquivo.write(response.content)
            print(f"Foto baixada com sucesso como {nome_arquivo}")
        else:
            print(
                f"Erro ao baixar a foto. Código de resposta: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação HTTP: {e}")

    if not nome_arquivo:
        convertVoz("Não detectou nada!")
    else:
        return nome_arquivo
