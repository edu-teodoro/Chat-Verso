# =====================================================================================
# Copyright 2025 DuduTri
# Contato: est.teodoro@gmail.com
# Todos os direitos reservados.
# FUNÇÃO: Lançador de login para uso em rede local.
# DESCRIÇÃO: Este script cria uma página de login simples usando a biblioteca Flet.
#            Ele captura o nome do usuário e o redireciona para o servidor de chat
#            principal (app.py), automatizando a criação da URL de acesso.
# =====================================================================================
import flet as ft
import os
import urllib.parse

# --- Configurações ---
APP_HOST = os.environ.get("FLET_HOST", "127.0.0.1")
APP_PORT = 8550       # Porta para esta aplicação de login
CHAT_SERVER_IP = os.environ.get("CHAT_SERVER_IP", "127.0.0.1").strip()
if not CHAT_SERVER_IP:
    raise RuntimeError("CHAT_SERVER_IP não pode ser vazio.")
CHAT_SERVER_PORT = 5000  # Porta do servidor de chat principal (app.py)
# ---------------------


def main(pagina):
    """Função principal que constrói e gerencia a interface do Flet."""

    pagina.title = "ChatVerso"
    # Centraliza todo o conteúdo da página
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Título da aplicação
    titulo = ft.Text("ChatVerso", size=30)
    
    # Define os componentes da interface: um pop-up de login e um botão para abri-lo.
    caixa_nome = ft.TextField(label="Digite seu User", autofocus=True)
    botao_popup = ft.Button("Acessar Chat")
    
    popup = ft.AlertDialog(
        title=ft.Text("Seja bem-vindo ao ChatVerso"),
        content=caixa_nome,
        actions=[botao_popup]
    )
    
    botao = ft.Button("Iniciar conversa")
    
    async def entrar_chat(evento):
        # COMO FUNCIONA: Esta função é chamada quando o usuário clica em "Acessar Chat".
        # A verificação `if caixa_nome.value and caixa_nome.value.strip()` garante que o valor não é None nem uma string vazia/com espaços.
        if caixa_nome.value and caixa_nome.value.strip():
            username = caixa_nome.value.strip() # Pega o valor já validado e remove espaços.
            # POR QUÊ `urllib.parse.quote`? Garante que caracteres especiais no nome de
            # usuário (como espaços) sejam formatados corretamente para uso em uma URL.
            encoded_username = urllib.parse.quote(username)
            # Fecha o popup
            popup.open = False
            
            # Abre a URL do chat web no navegador padrão
            # POR QUÊ? Em vez de o usuário montar a URL manualmente, este script
            #          faz isso por ele, obtendo o IP do servidor de chat e
            #          adicionando o nome de usuário como parâmetro.
            await pagina.launch_url(f"http://{CHAT_SERVER_IP}:{CHAT_SERVER_PORT}/chat?username={encoded_username}")
            
            # Limpa a tela do Flet e exibe uma mensagem de confirmação
            # para informar ao usuário que a ação foi bem-sucedida.
            pagina.clean()
            pagina.add(ft.Text(f"Chat aberto no seu navegador! Você pode fechar esta janela.", size=16))
            pagina.update()
    
    botao_popup.on_click = entrar_chat
    caixa_nome.on_submit = entrar_chat
    
    async def abrir_popup(evento):
        # Simplesmente abre o diálogo de login quando o botão inicial é clicado.
        popup.open = True
        pagina.update()
        await caixa_nome.focus()
    
    botao.on_click = abrir_popup

    # adicionar elementos na pagina
    # Adiciona o diálogo à sobreposição da página. Isso é necessário para que ele possa ser aberto.
    # POR QUÊ? Em Flet, diálogos e outros elementos flutuantes devem ser
    #          adicionados à camada `overlay` antes de serem exibidos.
    pagina.overlay.append(popup)

    pagina.add(titulo, botao)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Lançador do ChatVerso iniciado!")
    print(f"Acesso local: http://127.0.0.1:{APP_PORT}")
    if APP_HOST == "0.0.0.0":
        print(f"Acesso pela rede: use o IP desta máquina na porta {APP_PORT}")
    print("="*50 + "\n")

    ft.run(main, host=APP_HOST, port=APP_PORT, view=ft.AppView.WEB_BROWSER)