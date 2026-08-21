import ollama
import platform
import json
import os
import threading
import time
import schedule

from config import PERSONALIDADE

ARQUIVO_MEMORIA = "memoria_lola.json"
BUFFER_CONVERSA = [] 


if platform.machine() == 'x86_64': # Estudar arquitetura do hailo-8l
    MODELO_USADO = "tinyllama"  # testar R4
else: 
    MODELO_USADO = "llama3.2:3b"

if not os.path.exists(ARQUIVO_MEMORIA):
    with open(ARQUIVO_MEMORIA, "w") as f:
        json.dump({}, f)

def carregar_memoria():
    try:
        with open(ARQUIVO_MEMORIA, "r") as f:
            return json.load(f)
    except:
        return {}

def salvar_memoria(chave, valor):
    dados = carregar_memoria()
    dados[chave] = valor
    with open(ARQUIVO_MEMORIA, "w") as f:
        json.dump(dados, f, indent=4)

def processar_resumo():
    global BUFFER_CONVERSA
    
    if not BUFFER_CONVERSA:
        return

    texto_para_resumir = "\n".join(BUFFER_CONVERSA)
    
    prompt_arquivista = f"""
    Analise a conversa abaixo e extraia um JSON com:
    1. 'resumo': um resumo conciso.
    2. 'keywords': Lista de tópicos importantes.
    
    Conversa:
    {texto_para_resumir}
    """
    
    try:
        resposta = ollama.chat(model=MODELO_USADO, messages=[
            {'role': 'user', 'content': prompt_arquivista}
        ])
        
        dados_processados = resposta['message']['content']
        
        BUFFER_CONVERSA = []
        
    except Exception as e:
        print(f"[Erro] Falha ao resumir: {e}")

def rodar_agendador():
    schedule.every(2).minutes.do(processar_resumo)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

thread_arquivista = threading.Thread(target=rodar_agendador)
thread_arquivista.daemon = True 
thread_arquivista.start()

def perguntar_ia(pergunta_usuario):
    BUFFER_CONVERSA.append(f"User: {pergunta_usuario}")
    
    memoria_atual = carregar_memoria()
    texto_memoria = f"O que você sabe sobre o: {memoria_atual}"
    prompt_sistema = f"{PERSONALIDADE}\n{texto_memoria}"
    
    try:
        resposta = ollama.chat(model=MODELO_USADO, messages=[
            {'role': 'system', 'content': prompt_sistema},
            {'role': 'user', 'content': pergunta_usuario},
        ])
        
        conteudo_resposta = resposta['message']['content']
        BUFFER_CONVERSA.append(f"Lola: {conteudo_resposta}")
        return conteudo_resposta
        
    except Exception as e:
        return f"Erro no: {e}"

if __name__ == "__main__":
    while True:
        txt = input("Você: ")
        print("Lola:", perguntar_ia(txt))
