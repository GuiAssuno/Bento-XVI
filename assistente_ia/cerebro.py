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

# --- Configuração do Modelo (Correção Lógica) ---
# Detecta onde estamos rodando APENAS UMA VEZ
if platform.machine() == 'x86_64': # Seu PC Intel
    MODELO_USADO = "tinyllama"
    print("⚠️ Usando modelo leve (TinyLlama) para desenvolvimento no PC.")
else: # Raspberry Pi (aarch64)
    MODELO_USADO = "llama3.2:3b"
    print("🚀 Usando modelo oficial (Llama 3.2) no Raspberry Pi.")

# --- Funções de Memória ---
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

# --- Funções do Arquivista ---
def processar_resumo():
    global BUFFER_CONVERSA
    
    if not BUFFER_CONVERSA:
        return

    print("\n[Sistema] 🕒 Iniciando resumo automático...")
    
    texto_para_resumir = "\n".join(BUFFER_CONVERSA)
    
    prompt_arquivista = f"""
    Analise a conversa abaixo e extraia um JSON com:
    1. 'resumo': Um resumo conciso.
    2. 'keywords': Lista de tópicos importantes.
    
    Conversa:
    {texto_para_resumir}
    """
    
    try:
        # CORREÇÃO: Usando a variável MODELO_USADO em vez de string fixa
        resposta = ollama.chat(model=MODELO_USADO, messages=[
            {'role': 'user', 'content': prompt_arquivista}
        ])
        
        dados_processados = resposta['message']['content']
        print(f"[Sistema] ✅ Memória consolidada (Simulação): {dados_processados[:30]}...")
        
        # Limpa o buffer
        BUFFER_CONVERSA = []
        
    except Exception as e:
        print(f"[Erro] Falha ao resumir: {e}")

def rodar_agendador():
    # Roda a cada 2 minutos para teste (mude para 10 depois)
    schedule.every(2).minutes.do(processar_resumo)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Inicia o Arquivista automaticamente quando este arquivo é importado
thread_arquivista = threading.Thread(target=rodar_agendador)
thread_arquivista.daemon = True 
thread_arquivista.start()

# --- Cérebro Principal ---
def perguntar_ia(pergunta_usuario):
    # Adiciona ao buffer para o futuro resumo
    BUFFER_CONVERSA.append(f"User: {pergunta_usuario}")
    
    memoria_atual = carregar_memoria()
    texto_memoria = f"O que você sabe sobre o usuário: {memoria_atual}"
    prompt_sistema = f"{PERSONALIDADE}\n{texto_memoria}"
    
    try:
        # CORREÇÃO: Usando a variável MODELO_USADO
        resposta = ollama.chat(model=MODELO_USADO, messages=[
            {'role': 'system', 'content': prompt_sistema},
            {'role': 'user', 'content': pergunta_usuario},
        ])
        
        conteudo_resposta = resposta['message']['content']
        BUFFER_CONVERSA.append(f"Lola: {conteudo_resposta}")
        return conteudo_resposta
        
    except Exception as e:
        return f"Erro no cérebro: {e}"

# --- ÁREA DE TESTE (Correção do Loop) ---
# O if __name__ == "__main__" garante que isso SÓ roda se você der play 
# direto neste arquivo. Se o main.py importar, isso é ignorado.
if __name__ == "__main__":
    print("🧪 Testando Cérebro isoladamente...")
    while True:
        txt = input("Você: ")
        print("Lola:", perguntar_ia(txt))