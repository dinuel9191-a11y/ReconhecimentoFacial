
# Sistema de Reconhecimento Facial

Sistema de reconhecimento facial desenvolvido em Python, utilizando OpenCV, DeepFace e o modelo FaceNet512.

O projeto permite cadastrar pessoas por meio de uma webcam, armazenar fotografias localmente e realizar o reconhecimento facial através da comparação de características biométricas.

## Funcionalidades

- Detecção de rostos utilizando OpenCV e Haar Cascade.
- Cadastro de pessoas diretamente pela webcam.
- Captura automática de cinco fotografias por cadastro.
- Extração de características faciais utilizando FaceNet512.
- Comparação de rostos por distância de cosseno.
- Identificação de pessoas cadastradas.
- Identificação de rostos não cadastrados como "Desconhecido".

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python 3.12 | Linguagem de programação |
| OpenCV | Captura de imagens e detecção facial |
| DeepFace | Framework de reconhecimento facial |
| FaceNet512 | Modelo de representação facial |
| NumPy | Operações matemáticas e vetoriais |

## Estrutura do projeto

```text
ReconhecimentoFacial/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── pessoas/
    └── .gitkeep
```

## Requisitos

Antes de executar o projeto, é necessário possuir:

- Windows 10 ou Windows 11 de 64 bits.
- Python 3.12 de 64 bits.
- Webcam funcional.
- Conexão com a internet para baixar os modelos na primeira execução.

O projeto não utiliza executável `.exe`. A execução é feita diretamente pelo Python.

## Instalação

### 1. Instalar o Python

Baixe o Python 3.12 pelo site oficial:

https://www.python.org/downloads/release/python-3120/

Durante a instalação no Windows, habilite a opção:

`Add Python to PATH`

Verifique a instalação pelo terminal:

```powershell
python --version
```

O resultado esperado é semelhante a:

```text
Python 3.12.x
```

### 2. Baixar o projeto

No GitHub:

1. Acesse o repositório.
2. Clique no botão Code.
3. Selecione Download ZIP.
4. Extraia os arquivos para uma pasta do computador.

Outra possibilidade é utilizar o Git:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

Entre na pasta do projeto:

```bash
cd SEU-REPOSITORIO
```

Substitua a URL pelo endereço real do repositório.

### 3. Criar um ambiente virtual

Dentro da pasta do projeto, execute:

```powershell
python -m venv venv
```

O ambiente virtual mantém as bibliotecas do projeto isoladas de outras instalações Python.

### 4. Ativar o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Caso o Windows bloqueie a execução do script, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, tente ativar novamente:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install --upgrade pip
```

Em seguida:

```powershell
python -m pip install -r requirements.txt
```

A instalação do DeepFace e de suas dependências pode levar alguns minutos.

### 6. Executar o programa

Após a instalação, execute:

```powershell
python main.py
```

O sistema apresentará o menu principal.

## Como utilizar

Ao executar o programa, será apresentado o seguinte menu:

```text
================================
 SISTEMA DE RECONHECIMENTO FACIAL
================================
1 - Reconhecer pessoas
2 - Cadastrar pessoa
0 - Sair

Escolha uma opção:
```

### Cadastro de pessoas

1. Escolha a opção `2`.
2. Digite o nome da pessoa.
3. Posicione o rosto diante da webcam.
4. Pressione `S` para capturar uma fotografia.
5. Repita o procedimento até completar cinco fotografias.
6. O cadastro será armazenado automaticamente.

É recomendado variar ligeiramente a posição e o ângulo do rosto entre as capturas.

### Reconhecimento facial

1. Escolha a opção `1`.
2. Aguarde o carregamento das fotografias cadastradas.
3. Posicione o rosto diante da webcam.
4. O sistema realizará a comparação com as pessoas cadastradas.
5. Caso encontre uma correspondência dentro do limite configurado, exibirá o nome da pessoa.
6. Caso contrário, exibirá `Desconhecido`.

Pressione `Q` na janela da webcam para sair do reconhecimento.

## Modelos de inteligência artificial

O projeto utiliza o modelo FaceNet512 por meio do DeepFace.

O FaceNet512 transforma uma imagem facial em um vetor numérico de 512 dimensões, chamado embedding.

Esses vetores são utilizados para comparar as características dos rostos.

Na primeira execução, o DeepFace poderá baixar automaticamente os pesos do modelo.

Os arquivos são armazenados normalmente em:

```text
C:\Users\SEU_USUARIO\.deepface\weights\
```

O classificador Haar Cascade também é baixado automaticamente pelo programa quando não está disponível.

Portanto, a primeira execução exige conexão com a internet.

## Configurações

As principais configurações estão no início de `main.py`:

```python
MODELO = "Facenet512"
LIMITE_DISTANCIA = 0.30
QUANTIDADE_FOTOS = 5
```

| Configuração | Descrição |
|---|---|
| MODELO | Modelo utilizado para gerar os embeddings faciais. |
| LIMITE_DISTANCIA | Distância máxima experimental para aceitar uma identificação. |
| QUANTIDADE_FOTOS | Quantidade de fotografias capturadas durante o cadastro. |

O limite de distância deve ser avaliado por meio de testes com diferentes pessoas e condições de iluminação.

Um limite menor tende a ser mais restritivo, mas não garante ausência de erros.

## Solução de problemas

### A webcam não abre

- Verifique se a câmera está conectada.
- Confira as permissões de câmera do Windows.
- Feche outros programas que estejam utilizando a webcam.
- Se houver mais de uma câmera, teste outro índice em `cv2.VideoCapture(0)`.

### Erro durante a instalação

Confira a versão do Python:

```powershell
python --version
```

Atualize o pip:

```powershell
python -m pip install --upgrade pip
```

Verifique se o ambiente virtual está ativado e tente instalar novamente:

```powershell
python -m pip install -r requirements.txt
```

### O sistema não reconhece uma pessoa cadastrada

- Verifique se as fotografias estão na pasta correta.
- Utilize imagens nítidas e com boa iluminação.
- Evite fotografias com o rosto parcialmente escondido.
- Confira as mensagens de erro exibidas durante o carregamento das imagens.
- Avalie o limite de distância utilizado.

### O programa demora para iniciar o reconhecimento

O DeepFace precisa carregar o modelo e processar as fotografias cadastradas. Quanto maior a quantidade de imagens, maior poderá ser o tempo de inicialização.

## Privacidade e segurança

Fotografias faciais e embeddings utilizados para identificar pessoas podem constituir dados biométricos sensíveis, conforme a Lei Geral de Proteção de Dados (LGPD).

Por isso:

- Cadastre pessoas somente com autorização e finalidade legítima.
- Não publique fotografias pessoais no repositório.
- Não compartilhe embeddings ou outros dados biométricos.
- Proteja a pasta de cadastros.
- Limite o acesso aos dados armazenados.
- Não utilize o reconhecimento como única base para decisões importantes.

O sistema é experimental e pode apresentar falsos reconhecimentos ou deixar de identificar pessoas cadastradas.

## Autor

Desenvolvido como projeto acadêmico utilizando Python e tecnologias de visão computacional.

## Licença

A licença do projeto ainda não foi definida.
