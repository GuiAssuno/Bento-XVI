import flet as ft
from main import processar_comando  # Importa sua lógica

def main(page: ft.Page):
    page.title = "Assistente IA"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.DARK # Fica mais bonito e gasta menos energia
    
    # Função que roda quando clica no botão enviar
    def enviar_mensagem(e):
        if campo_texto.value == "":
            return
        
        pergunta = campo_texto.value
        chat_log.controls.append(ft.Text(f"Você: {pergunta}", color="blue"))
        page.update()
        
        # Chama seu cérebro (vai travar a tela um pouco, depois arrumamos isso)
        resposta = processar_comando(pergunta)
        
        chat_log.controls.append(ft.Text(f"IA: {resposta}", color="green", weight="bold"))
        campo_texto.value = ""
        page.update()

    # Elementos da Tela
    chat_log = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    campo_texto = ft.TextField(hint_text="Fale ou digite algo...", expand=True, on_submit=enviar_mensagem)
    # Usando string direta (funciona sempre)
    botao_enviar = ft.IconButton(icon="send", on_click=enviar_mensagem)

    # Layout (Uma coluna com o chat em cima e a entrada embaixo)
    page.add(
        ft.Container(
            content=chat_log,
            expand=True, # Ocupa todo o espaço disponível
            padding=10
        ),
        ft.Row(
            controls=[campo_texto, botao_enviar],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)


#LIBGL_ALWAYS_SOFTWARE=1 /home/lola/VScode/.libs/bin/python /home/lola/VScode/Bento-XVI/assistente_ia/interface.py