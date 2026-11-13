# ChatVerso

Aplicação de chat em tempo real feita com Flask e Flask-SocketIO, com páginas HTML/CSS/JavaScript e um lançador de login opcional em Flet.

## Estrutura do repositório

```text
Chat-Verso/
├── app.py
├── chatverso.py
├── index.html
├── login.html
├── requirements.txt
├── static/
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```

`.venv/` é criado localmente durante a instalação e não é versionado.

## Instalação

Execute os comandos na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Em macOS/Linux, ative o ambiente com `source .venv/bin/activate` em vez do comando de ativação do PowerShell.
Se o Python estiver instalado via `uv` e o comando `python` não estiver no `PATH`, use `uv venv .venv --python 3.14` no lugar da primeira linha.

## Chave do Flask e execução local

O servidor exige `FLASK_SECRET_KEY` no ambiente; ele não tem uma chave padrão no código. Gere uma chave nova e mantenha-a fora do repositório. Como a chave anterior foi publicada, considere-a comprometida e não a reutilize.

No PowerShell, na mesma janela em que iniciará o servidor:

```powershell
$env:FLASK_SECRET_KEY = (& python -c "import secrets; print(secrets.token_urlsafe(32))")
$env:CHAT_SERVER_IP = "127.0.0.1"
python .\app.py
```

Em macOS/Linux:

```bash
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export CHAT_SERVER_IP=127.0.0.1
python app.py
```

O comando inicia o servidor Flask e Socket.IO, na porta `5000`. Acesse localmente em <http://127.0.0.1:5000>. A variável `FLASK_SECRET_KEY` só precisa ser definida no ambiente do servidor; não a coloque no código, no README ou em arquivos versionados.

## Lançador opcional em Flet

Com o servidor em execução, abra outro terminal na raiz do repositório, ative o mesmo ambiente virtual e inicie o lançador:

```powershell
$env:CHAT_SERVER_IP = "127.0.0.1"
python .\chatverso.py
```

Acesse <http://127.0.0.1:8550>. Por padrão, o lançador aceita conexões somente da própria máquina e abre o chat no servidor indicado por `CHAT_SERVER_IP`; localmente, o padrão é `127.0.0.1`.

## Acesso pela rede local

O servidor de chat escuta em todas as interfaces na porta `5000`. Em outro dispositivo na mesma rede, abra `http://<IP-DA-MAQUINA-DO-SERVIDOR>:5000`. Se necessário, permita a porta `5000` no firewall.

Para usar o lançador Flet a partir de outros dispositivos, configure o endereço do servidor no ambiente do processo Flet e permita a porta `8550`. No PowerShell:

```powershell
$env:CHAT_SERVER_IP = "<IP-DA-MAQUINA-DO-SERVIDOR>"
$env:FLET_HOST = "0.0.0.0"
python .\chatverso.py
```

Então, no outro dispositivo, acesse `http://<IP-DA-MAQUINA-DO-FLET>:8550`. Substitua os marcadores pelos endereços reais da rede. `CHAT_SERVER_IP` é o endereço usado pelo navegador para alcançar o servidor de chat; se o Flet for aberto em outro dispositivo, não use `127.0.0.1`, pois esse endereço apontaria para o próprio dispositivo cliente.
