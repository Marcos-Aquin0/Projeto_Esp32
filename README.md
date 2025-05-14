# Projeto ESP32
Interface Gráfica desenvolvida para o projeto de monitoramento com ESP32 - Unifesp/SJC - 2025/1

Este projeto conecta um ESP32 via MQTT para coletar dados de temperatura e umidade, armazena-os em um banco de dados Supabase PostgreSQL e exibe os dados em um dashboard Streamlit.

## Funcionalidades

- Conexão com broker MQTT (HiveMQ)
- Coleta de dados de temperatura e umidade em tempo real
- Armazenamento de dados no banco PostgreSQL (Supabase)
- Dashboard interativo com gráficos e tabelas

## Instalando Dependências com Conda

1. **Instale todas as dependências:**
    ```sh
    pip install streamlit psycopg2 pandas paho-mqtt
    ```

## Configuração do Banco de Dados

O projeto utiliza um banco de dados PostgreSQL hospedado no Supabase. A tabela principal `leituras` armazena:
- temperatura
- umidade
- timestamp

## Configuração MQTT

O projeto se conecta ao broker HiveMQ (broker.hivemq.com) via mqtt.cool e assina os seguintes tópicos:
- FIT/PUB_Temperatura
- FIT/PUB_Umidade

## Executando app.py com Streamlit

Para executar o `app.py` usando Streamlit, siga estes passos:

1. **Navegue até o diretório que contém `app.py`:**
    ```sh
    cd ./Projeto_esp32
    ```

2. **Execute o aplicativo Streamlit:**
    ```sh
    streamlit run app.py
    ```

3. **Abra a URL fornecida no seu navegador web:**

    Após executar o comando, o Streamlit fornecerá uma URL local (geralmente `http://localhost:8501`). Abra essa URL no seu navegador web para visualizar e interagir com o aplicativo.
    Ou utilize o deploy do app: `https://`.
