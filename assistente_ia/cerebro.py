import ollama

def perguntar_ia(texto_usuario):
    print("🧠 Pensando...")
    try:
        resposta = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': texto_usuario},
        ])
        return resposta['message']['content']
    except Exception as e:
        return f"Erro ao conectar com o cérebro: {e}"