import ollama
import platform

# Detecta onde estamos rodando
if platform.machine() == 'x86_64': # Seu PC Intel
    MODELO_USADO = "tinyllama"
    print("⚠️ Usando modelo leve (TinyLlama) para desenvolvimento no PC.")
else: # Raspberry Pi (aarch64)
    MODELO_USADO = "llama3.2:3b"
    print("🚀 Usando modelo oficial (Llama 3.2) no Raspberry Pi.")

def perguntar_ia(texto_usuario):
    print("🧠 Pensando...")
    try:
        resposta = ollama.chat(model=MODELO_USADO, messages=[
            {'role': 'user', 'content': texto_usuario},
        ])
        return resposta['message']['content']
    except Exception as e:
        return f"Erro no cérebro: {e}"