#!/usr/bin/env python3
"""
BotMuteKit - Bot Discord para monitoramento automático de canais de voz
Ponto de entrada principal da aplicação
"""

import asyncio
import signal
import sys
from src.config.logging import setup_logging
from src.config.settings import BotSettings
from src.bot.client import BotMuteKitClient

# Configura logging
logger = setup_logging()

class BotRunner:
    """Gerencia o ciclo de vida do bot"""
    
    def __init__(self):
        self.bot = None
        self.shutdown_event = asyncio.Event()
    
    async def start_bot(self):
        """Inicia o bot"""
        try:
            # Valida configurações
            if not BotSettings.validate():
                logger.error("❌ DISCORD_TOKEN não encontrado nas variáveis de ambiente!")
                logger.error("💡 Crie um arquivo .env com DISCORD_TOKEN=seu_token_aqui")
                return False
            
            # Cria e inicia o bot
            self.bot = BotMuteKitClient()
            
            # Configura handlers de sinal para shutdown limpo
            self._setup_signal_handlers()
            
            logger.info("🚀 Iniciando o bot...")
            
            # Executa o bot
            await self.bot.start(BotSettings.DISCORD_TOKEN)
            
            return True
            
        except discord.LoginFailure:
            logger.error("❌ Falha na autenticação. Verifique o token do bot.")
            return False
        except Exception as e:
            logger.error(f"❌ Erro crítico: {e}")
            return False
    
    async def shutdown_bot(self):
        """Desliga o bot de forma limpa"""
        if self.bot:
            await self.bot.shutdown()
    
    def _setup_signal_handlers(self):
        """Configura handlers para sinais do sistema"""
        def signal_handler(signum, frame):
            logger.info(f"📡 Sinal {signum} recebido, iniciando shutdown...")
            self.shutdown_event.set()
        
        # Registra handlers para SIGINT (Ctrl+C) e SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def run(self):
        """Executa o bot com gerenciamento de ciclo de vida"""
        try:
            # Inicia o bot em background
            bot_task = asyncio.create_task(self.start_bot())
            
            # Aguarda pelo evento de shutdown
            await self.shutdown_event.wait()
            
            logger.info("🛑 Iniciando shutdown...")
            
            # Desliga o bot
            await self.shutdown_bot()
            
            # Cancela a tarefa do bot
            bot_task.cancel()
            
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
            
            logger.info("✅ Shutdown concluído")
            
        except Exception as e:
            logger.error(f"❌ Erro durante execução: {e}")
            await self.shutdown_bot()

async def main():
    """Função principal"""
    runner = BotRunner()
    await runner.run()

if __name__ == "__main__":
    try:
        # Executa o bot
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)
