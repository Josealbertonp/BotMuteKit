"""
Serviço para gerenciar canais de voz e operações relacionadas
"""
import logging
from typing import Optional
import discord
from ..config.settings import BotSettings
from ..utils.helpers import sanitize_channel_name

logger = logging.getLogger(__name__)

class ChannelManager:
    """Gerencia operações relacionadas a canais de voz"""
    
    def __init__(self):
        self.afk_channel_name = BotSettings.AFK_CHANNEL_NAME
    
    async def find_or_create_afk_channel(self, guild: discord.Guild) -> Optional[discord.VoiceChannel]:
        """
        Encontra ou cria o canal AFK se não existir
        
        Args:
            guild: Servidor Discord
        
        Returns:
            Canal AFK ou None se não for possível criar
        """
        afk_channel = self._find_afk_channel(guild)
        
        if afk_channel:
            return afk_channel
        
        try:
            afk_channel = await self._create_afk_channel(guild)
            return afk_channel
        except discord.Forbidden:
            logger.error(f"❌ Sem permissão para criar canal '{self.afk_channel_name}'")
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao criar canal AFK: {e}")
            return None
    
    def _find_afk_channel(self, guild: discord.Guild) -> Optional[discord.VoiceChannel]:
        """
        Encontra o canal AFK no servidor
        
        Args:
            guild: Servidor Discord
        
        Returns:
            Canal AFK ou None se não encontrado
        """
        for channel in guild.voice_channels:
            if channel.name.lower() == self.afk_channel_name.lower():
                return channel
        return None
    
    async def _create_afk_channel(self, guild: discord.Guild) -> discord.VoiceChannel:
        """
        Cria o canal AFK
        
        Args:
            guild: Servidor Discord
        
        Returns:
            Canal AFK criado
        """
        sanitized_name = sanitize_channel_name(self.afk_channel_name)
        
        afk_channel = await guild.create_voice_channel(
            name=sanitized_name,
            reason="Canal criado automaticamente pelo bot para usuários ausentes"
        )
        
        logger.info(f"📝 Canal '{sanitized_name}' foi criado automaticamente")
        return afk_channel
    
    async def move_user_to_afk(self, member: discord.Member, original_channel: discord.VoiceChannel) -> bool:
        """
        Move um usuário para o canal AFK
        
        Args:
            member: Membro a ser movido
            original_channel: Canal original do usuário
        
        Returns:
            True se o usuário foi movido com sucesso, False caso contrário
        """
        try:
            guild = member.guild
            afk_channel = await self.find_or_create_afk_channel(guild)
            
            if not afk_channel:
                await member.move_to(None)
                logger.info(f"🚪 {member.name} foi removido do canal '{original_channel.name}' por ficar com áudio desativado")
                return True
            
            if afk_channel != original_channel:
                await member.move_to(afk_channel)
                logger.info(f"🔄 {member.name} foi movido de '{original_channel.name}' para '{afk_channel.name}' por ficar com áudio desativado")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao mover usuário {member.name} para canal AFK: {e}")
            return False
    
    def is_afk_channel(self, channel: discord.VoiceChannel) -> bool:
        """
        Verifica se um canal é o canal AFK
        
        Args:
            channel: Canal a ser verificado
        
        Returns:
            True se for o canal AFK, False caso contrário
        """
        return channel.name.lower() == self.afk_channel_name.lower()
