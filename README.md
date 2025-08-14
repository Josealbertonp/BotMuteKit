# Discord Voice Mute Monitor Bot

Um bot Discord que move automaticamente usuários para um canal de "Ausente" quando desativam o áudio para escutar por mais de 5 segundos.

## 🚀 Funcionalidades

- ✅ Monitora automaticamente canais de voz
- 🔇 Move usuários que desativam o áudio para canal "Ausente" após 5 segundos (configurável)
- 🎤 Usuários que apenas mutam o microfone permanecem na sala
- 🏠 Cria automaticamente o canal "Ausente" se não existir
- 📝 Log detalhado de todas as ações
- 💬 Envia DM para usuários movidos (quando possível)
- 🤖 Funcionamento totalmente automático (sem comandos)
- 🔧 Configuração via variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta Discord e bot criado no Discord Developer Portal
- Permissões necessárias para o bot no servidor

## 🛠️ Instalação

1. Clone ou baixe este repositório

2. Instale as dependências necessárias:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Copie o arquivo `env.example` para `.env`:
   ```bash
   cp env.example .env
   ```

4. Configure o arquivo `.env` com seu token do bot:
   ```env
   DISCORD_TOKEN=seu_token_aqui
   MUTE_TIMEOUT=5
   AFK_CHANNEL_NAME=ausente
   MONITORED_CHANNELS=Geral,Conversa,Reunião
   ```

## ⚙️ Configurações Principais

Todas as configurações são feitas através do arquivo `.env`:

### 🎯 Canais Monitorados (`MONITORED_CHANNELS`)
- **Todos os canais**: Deixe vazio para monitorar todos os canais de voz
- **Canais específicos**: Liste os nomes separados por vírgula
  ```env
  MONITORED_CHANNELS=Geral,Conversa,Reunião,Estudo
  ```

### 🏠 Canal de Destino (`AFK_CHANNEL_NAME`)
- Define para onde os usuários serão movidos
  ```env
  AFK_CHANNEL_NAME=ausente
  ```
- Se o canal não existir, será criado automaticamente

### ⏱️ Tempos de Espera 
- **`MUTE_TIMEOUT`**: Para quem muta durante o uso da sala
  ```env
  MUTE_TIMEOUT=20
  ```
- **`JOIN_MUTED_TIMEOUT`**: Para quem entra na sala já mutado
  ```env
  JOIN_MUTED_TIMEOUT=5
  ```
- **`RETURN_MUTED_TIMEOUT`**: Para quem sai da sala e retorna mutado
  ```env
  RETURN_MUTED_TIMEOUT=20
  ```

### Exemplo de Configuração Completa:
```env
DISCORD_TOKEN=seu_token_aqui
MUTE_TIMEOUT=20
JOIN_MUTED_TIMEOUT=5
RETURN_MUTED_TIMEOUT=20
AFK_CHANNEL_NAME=ausente
MONITORED_CHANNELS=Geral,Conversa,Reunião
```

## 🎮 Como obter o Token do Bot

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao seu bot
3. Vá para a aba "Bot" no menu lateral
4. Clique em "Add Bot"
5. Copie o token gerado e cole no arquivo `.env`

## 🔐 Permissões Necessárias

O bot precisa das seguintes permissões no servidor Discord:

- ✅ View Channels (Ver Canais)
- ✅ Connect (Conectar)
- ✅ Move Members (Mover Membros)
- ✅ Send Messages (Enviar Mensagens)
- ✅ Use Slash Commands (Usar Comandos de Barra)

## 🚀 Executando o Bot

```bash
python3 main.py
```

## 🌐 Servidor Web (Termos de Serviço)

Para executar o servidor web que hospeda os termos de serviço:

```bash
cd web
python3 terms_server.py
```

O servidor estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
BotMuteKit/
├── src/                    # Código fonte principal
│   ├── bot/               # Cliente Discord
│   ├── services/          # Serviços de negócio
│   ├── config/            # Configurações
│   └── utils/             # Utilitários
├── web/                   # Servidor web e páginas HTML
├── logs/                  # Arquivos de log
├── main.py                # Ponto de entrada
└── requirements.txt       # Dependências
```
