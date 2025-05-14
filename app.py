import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import threading
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuração da conexão com Supabase PostgreSQL
DB_HOST = "aws-0-sa-east-1.pooler.supabase.com"  
DB_NAME = "postgres"
DB_USER = "postgres.uixayvgstkfnpvdszrmt"
DB_PASS = "#FQPxrjAJS5wh9Q5"
DB_PORT = "6543"

# Função para conectar ao banco
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

# Variáveis para armazenar os dados recebidos
valor_temp = None
valor_umid = None

# Callback MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT com código:", rc)
    client.subscribe("FIT/PUB_Temperatura")
    client.subscribe("FIT/PUB_Umidade")

def on_message(client, userdata, msg):
    global valor_temp, valor_umid
    try:
        valor = float(msg.payload.decode())

        if msg.topic == "FIT/PUB_Temperatura":
            valor_temp = valor
        elif msg.topic == "FIT/PUB_Umidade":
            valor_umid = valor

        # Se ambos os valores foram recebidos, insere no banco
        if valor_temp is not None and valor_umid is not None:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                insert_query = sql.SQL("""
                    INSERT INTO leituras (temperatura, umidade)
                    VALUES (%s, %s)
                """)
                cur.execute(insert_query, (valor_temp, valor_umid))
                conn.commit()
                cur.close()
                conn.close()
                print(f"📥 Inserido: {valor_temp}°C | {valor_umid}%")
                valor_temp = None
                valor_umid = None
    except Exception as e:
        print("Erro ao processar mensagem:", e)

# Iniciar o cliente MQTT numa thread separada
def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar ao mqtt.cool (porta 1883 para conexão básica TCP)
    client.username_pw_set("testuser", "testpassword")  # se necessário
    client.connect("broker.hivemq.com", 1883, 60)  # ou mqtt.cool se suportado sem TLS
    client.loop_forever()

# Inicia a thread MQTT
mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# STREAMLIT
st.set_page_config("Dashboard ESP32", layout="centered")
st.title("📊 Dashboard ESP32 com Supabase + MQTT")
st.write("Conectado ao broker `mqtt.cool: broker.hivemq.com` e armazenando dados no Supabase.")

# Mostrar gráfico
conn = get_db_connection()
if conn:

    df = pd.read_sql("SELECT * FROM leituras ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()

    if not df.empty:
        # Corrige horário do gráfico (força UTC-3 manualmente)

        # Tabela formatada
        df['timestamp_formatado'] = df['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')

        # Gráfico
        st.subheader("Gráfico de Temperatura e Umidade")
        df['timestamp'] = pd.to_datetime(df['timestamp']) + pd.Timedelta(hours=3)
        st.line_chart(df.set_index("timestamp")[["temperatura", "umidade"]])

        # Tabela
        st.subheader("Últimas Leituras")
        st.dataframe(df[["temperatura", "umidade", "timestamp_formatado"]].sort_values("timestamp_formatado", ascending=False), use_container_width=True)

    else:
        st.warning("Nenhum dado disponível ainda.")
else:
    st.error("Não foi possível conectar ao banco de dados.")
