# Open Weather API Service

Este projeto é um serviço que coleta dados da API Open Weather e os armazena como JSON.

## Decisões Técnicas

### Flask[async]
Optei por utilizar Flask por conta de ser mais objetivo e ter o desenvolvimento mais rápido para realizar o teste, visto que não é algo muito robusto. Utilizei o async por conta do requisito assíncrono.

### requests
Para fazer as requisições à Open Weather API utilizando Python.

### pytest e pytest-cov
Escolhi pytest por ser uma das bibliotecas mais robustas e famosas para testes em Python, além de possuir recursos de coverage (cobertura de código).

### python-dotenv
Utilizei python-dotenv para carregar variáveis de ambiente a partir de um arquivo `.env` para dentro do Python, facilitando a gestão de configurações sensíveis como tokens de API.

## Como Executar o Projeto

### Pré-requisitos
- Docker instalado

### Passos para Instalar o Docker
Caso você não tenha o Docker instalado, siga as instruções nos links abaixo para fazer o download e a instalação:
- [Docker para Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker para Linux](https://docs.docker.com/desktop/install/linux-install/)

### Passos para Construir e Executar a Imagem Docker
1. Clone este repositório:
   ```bash
   git clone https://github.com/vinirafaelsch/open-weather-api.git
   cd open-weather-api
2. Construa a imagem Docker:
   ```bash
   docker build -t open-weather-api .
3. Execute o contêiner Docker:
   ```bash
   docker run -p 5000:5000 open-weather-api

## Como Executar o Teste
1. Na pasta raiz do projeto execute os testes utilizando pytest:
   ```bash
   pytest --cov=app tests/

## .env
Antes de executar o projeto é necessário a adição do arquivo **.env** contendo a variável de ambiente **OPENWEATHER_API_KEY** com a chave gerada pelo usuário no site da Open Weather API.
