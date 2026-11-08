
import cv2
import numpy as np
import time
import sys

from pathlib import Path
from deepface import DeepFace
from urllib.request import urlretrieve


# ==========================================
# CONFIGURAÇÕES
# ==========================================

if getattr(sys, "frozen", False):
    PASTA_PROJETO = Path(sys.executable).resolve().parent
else:
    PASTA_PROJETO = Path(__file__).resolve().parent

PASTA_PESSOAS = PASTA_PROJETO / "pessoas"
PASTA_PESSOAS.mkdir(parents=True, exist_ok=True)

MODELO = "Facenet512"
LIMITE_DISTANCIA = 0.30

QUANTIDADE_FOTOS = 5


# ==========================================
# DETECTOR FACIAL
# ==========================================

PASTA_PESOS = (
    Path.home()
    / ".deepface"
    / "weights"
)

PASTA_PESOS.mkdir(
    parents=True,
    exist_ok=True
)

CAMINHO_DETECTOR = (
    PASTA_PESOS
    / "haarcascade_frontalface_default.xml"
)

URL_DETECTOR = (
    "https://github.com/opencv/opencv/raw/"
    "4.9.0/data/haarcascades/"
    "haarcascade_frontalface_default.xml"
)

# Baixa o classificador caso não exista
if not CAMINHO_DETECTOR.exists():

    print("Baixando classificador facial...")

    urlretrieve(
        URL_DETECTOR,
        str(CAMINHO_DETECTOR)
    )

detector = cv2.CascadeClassifier(
    str(CAMINHO_DETECTOR)
)

if detector.empty():

    raise RuntimeError(
        "Não foi possível carregar o detector facial!"
    )


# ==========================================
# CÁLCULO DE DISTÂNCIA
# ==========================================

def calcular_distancia(vetor1, vetor2):

    vetor1 = np.array(vetor1)
    vetor2 = np.array(vetor2)

    denominador = (
        np.linalg.norm(vetor1) *
        np.linalg.norm(vetor2)
    )

    if denominador == 0:
        return float("inf")

    return 1 - np.dot(vetor1, vetor2) / denominador


# ==========================================
# CARREGAMENTO DAS PESSOAS CADASTRADAS
# ==========================================

def carregar_pessoas():

    pessoas = {}

    if not PASTA_PESSOAS.exists():

        print("Pasta de pessoas não encontrada!")
        return pessoas

    for pasta in PASTA_PESSOAS.iterdir():

        if not pasta.is_dir():
            continue

        nome = pasta.name
        pessoas[nome] = []

        for arquivo in pasta.iterdir():

            if arquivo.suffix.lower() not in [
                ".jpg", ".jpeg", ".png"
            ]:
                continue

            try:

                resultado = DeepFace.represent(
                    img_path=str(arquivo),
                    model_name=MODELO,
                    detector_backend="opencv"
                )

                for rosto in resultado:

                    pessoas[nome].append(
                        rosto["embedding"]
                    )

                print(f"Imagem carregada: {arquivo}")

            except Exception as erro:

                print(
                    f"Erro ao carregar {arquivo}: {erro}"
                )

        if not pessoas[nome]:

            print(
                f"Nenhuma imagem válida para {nome}."
            )

    return pessoas


# ==========================================
# IDENTIFICAÇÃO FACIAL
# ==========================================

def identificar_rosto(imagem, pessoas):

    try:

        resultado = DeepFace.represent(
            img_path=imagem,
            model_name=MODELO,
            detector_backend="skip",
            enforce_detection=False
        )

        vetor = resultado[0]["embedding"]

        melhor_nome = "Desconhecido"
        menor_distancia = float("inf")

        for nome, embeddings in pessoas.items():

            for referencia in embeddings:

                distancia = calcular_distancia(
                    vetor,
                    referencia
                )

                if distancia < menor_distancia:

                    menor_distancia = distancia
                    melhor_nome = nome

        if menor_distancia <= LIMITE_DISTANCIA:

            return melhor_nome

        return "Desconhecido"

    except Exception as erro:

        print("Erro no reconhecimento:", erro)
        return "Desconhecido"


# ==========================================
# CADASTRO DE PESSOAS
# ==========================================

def cadastrar_pessoa():

    print("\n========== CADASTRO FACIAL ==========")

    nome = input(
        "Digite o nome da pessoa: "
    ).strip()

    # Remove caracteres inválidos do nome da pasta
    nome_pasta = "".join(
        caractere
        for caractere in nome
        if caractere.isalnum() or caractere in " _-"
    ).strip()

    if not nome_pasta:

        print("Nome inválido!")
        return

    pasta_pessoa = PASTA_PESSOAS / nome_pasta

    pasta_pessoa.mkdir(
        parents=True,
        exist_ok=True
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("Não foi possível acessar a webcam.")
        return

    contador = 0

    # Evita sobrescrever fotografias existentes
    numero_foto = (
        len(list(pasta_pessoa.glob("foto_*.jpg"))) + 1
    )

    print("\nCadastro iniciado!")
    print("Posicione o rosto diante da câmera.")
    print("Pressione S para capturar uma foto.")
    print("Pressione Q para cancelar.")

    while contador < QUANTIDADE_FOTOS:

        ret, frame = camera.read()

        if not ret:

            print("Erro ao capturar imagem.")
            break

        cinza = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        rostos = detector.detectMultiScale(
            cinza,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        # Desenha os rostos detectados
        for (x, y, w, h) in rostos:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        # Exibe a quantidade de fotografias
        cv2.putText(
            frame,
            f"Fotos: {contador}/{QUANTIDADE_FOTOS}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        if len(rostos) == 1:

            mensagem = "Pressione S para fotografar"

        elif len(rostos) == 0:

            mensagem = "Nenhum rosto detectado"

        else:

            mensagem = "Deixe apenas uma pessoa na imagem"

        cv2.putText(
            frame,
            mensagem,
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Cadastro Facial",
            frame
        )

        tecla = cv2.waitKey(1) & 0xFF

        # Captura somente quando existe exatamente um rosto
        if tecla == ord("s") and len(rostos) == 1:

            caminho_foto = (
                pasta_pessoa
                / f"foto_{numero_foto:02d}.jpg"
            )

            sucesso = cv2.imwrite(
                str(caminho_foto),
                frame
            )

            if sucesso:

                contador += 1
                numero_foto += 1

                print(
                    f"Fotografia {contador}/"
                    f"{QUANTIDADE_FOTOS} salva!"
                )

        elif tecla == ord("q"):

            print("Cadastro cancelado.")
            break

    camera.release()
    cv2.destroyAllWindows()

    if contador == QUANTIDADE_FOTOS:

        print(
            f"\nPessoa {nome_pasta} cadastrada com sucesso!"
        )

    else:

        print(
            f"\nCadastro incompleto: {contador} "
            f"de {QUANTIDADE_FOTOS} fotografias."
        )


# ==========================================
# RECONHECIMENTO FACIAL
# ==========================================

def reconhecer_pessoas():

    print("\nCarregando pessoas cadastradas...")

    pessoas = carregar_pessoas()

    if not any(pessoas.values()):

        print("Nenhuma fotografia válida encontrada!")
        return

    print(
        "Pessoas carregadas:",
        list(pessoas.keys())
    )

    # Inicializa a webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("Não foi possível acessar a webcam.")
        return

    ultimo_reconhecimento = 0
    resultados = []

    print("\nReconhecimento facial iniciado!")
    print("Pressione Q para sair.")

    try:

        while True:

            ret, frame = camera.read()

            if not ret:
                break

            agora = time.time()

            # Converte para escala de cinza
            cinza = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # Detecta os rostos
            rostos = detector.detectMultiScale(
                cinza,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            # Atualiza o reconhecimento a cada segundo
            if agora - ultimo_reconhecimento >= 1:

                resultados = []

                for (x, y, w, h) in rostos:

                    recorte = frame[y:y+h, x:x+w]

                    nome = identificar_rosto(
                        recorte,
                        pessoas
                    )

                    resultados.append(
                        (x, y, w, h, nome)
                    )

                ultimo_reconhecimento = agora

            # Desenha os resultados
            for x, y, w, h, nome in resultados:

                if nome != "Desconhecido":

                    cor = (0, 255, 0)

                else:

                    cor = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    cor,
                    2
                )

                cv2.putText(
                    frame,
                    nome,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    cor,
                    2
                )

            cv2.imshow(
                "Sistema de Reconhecimento Facial",
                frame
            )

            # Pressione Q para encerrar
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()
        cv2.destroyAllWindows()


# ==========================================
# MENU PRINCIPAL
# ==========================================

def main():

    while True:

        print("\n================================")
        print(" SISTEMA DE RECONHECIMENTO FACIAL")
        print("================================")

        print("1 - Reconhecer pessoas")
        print("2 - Cadastrar pessoa")
        print("0 - Sair")

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "1":

            reconhecer_pessoas()

        elif opcao == "2":

            cadastrar_pessoa()

        elif opcao == "0":

            print("Encerrando o sistema...")
            break

        else:

            print("Opção inválida!")


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":

    main()
