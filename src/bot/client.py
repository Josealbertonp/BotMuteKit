"""
Cliente Discord principal do bot
"""
import logging
import discord
from ..config.settings import BotSettings
from ..services.voice_monitor import VoiceMonitor

logger = logging.getLogger(__name__)

class BotMuteKitClient(discord.Client):
    """Cliente principal do bot BotMuteKit"""
    
    def __init__(self):
        intents = BotSettings.get_intents()
        super().__init__(intents=intents)
        
        self.voice_monitor = VoiceMonitor()
        
        logger.info("🤖 Cliente BotMuteKit inicializado")
    
    async def on_ready(self):
        """Evento disparado quando o bot se conecta com sucesso"""
        logger.info(f"✅ Bot conectado como {self.user}")
        logger.info(f"📊 Bot está em {len(self.guilds)} servidores")
        
        if BotSettings.MONITORED_CHANNELS:
            logger.info(f"🎯 Monitorando canais específicos: {', '.join(BotSettings.MONITORED_CHANNELS)}")
        else:
            logger.info(f"🌐 Monitorando TODOS os canais de voz")
        
        logger.info(f"🏠 Canal de destino: '{BotSettings.AFK_CHANNEL_NAME}'")
        logger.info(f"⏱️ Timeout para mute durante uso: {BotSettings.MUTE_TIMEOUT} segundos")
        logger.info(f"🚪 Timeout para entrar mutado: {BotSettings.JOIN_MUTED_TIMEOUT} segundos")
        
        await self._set_bot_presence()
        
        logger.info("🚀 Bot está pronto para monitorar canais de voz!")
    
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Evento disparado quando o estado de voz de um usuário muda
        
        Args:
            member: Membro cujo estado mudou
            before: Estado anterior
            after: Estado atual
        """
        await self.voice_monitor.handle_voice_state_update(member, before, after)
    
    async def on_error(self, event, *args, **kwargs):
        """Trata erros gerais do bot"""
        logger.error(f"❌ Erro no evento {event}: {args}, {kwargs}")
    
    async def on_disconnect(self):
        """Evento disparado quando o bot se desconecta"""
        logger.warning("⚠️ Bot desconectado do Discord")
    
    async def on_resumed(self):
        """Evento disparado quando o bot reconecta"""
        logger.info("🔄 Bot reconectou ao Discord")
    
    async def _set_bot_presence(self):
        """Define o status e atividade do bot"""
        try:
            await self.change_presence(
                status=discord.Status.online,
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="canais de voz"
                )
            )
            logger.debug("🎭 Status do bot definido")
        except Exception as e:
            logger.error(f"❌ Erro ao definir status do bot: {e}")
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do bot
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            "guilds": len(self.guilds),
            "voice_monitor": self.voice_monitor.get_stats()
        }
    
    async def shutdown(self):
        """Desliga o bot de forma limpa"""
        logger.info("🛑 Desligando bot...")
        
        self.voice_monitor.shutdown()
        
        await self.close()
        
        logger.info("✅ Bot desligado com sucesso")
