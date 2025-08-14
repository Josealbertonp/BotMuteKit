"""
Serviço principal para monitorar mudanças de estado de voz dos usuários
"""
import asyncio
import logging
from typing import Optional
import discord
from ..config.settings import BotSettings
from ..utils.helpers import should_monitor_channel
from .user_manager import UserManager
from .channel_manager import ChannelManager

logger = logging.getLogger(__name__)

class VoiceMonitor:
    """Monitora mudanças de estado de voz e gerencia timeouts"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.channel_manager = ChannelManager()
        self.mute_timeout = BotSettings.MUTE_TIMEOUT
        self.join_muted_timeout = BotSettings.JOIN_MUTED_TIMEOUT
        self.monitored_channels = BotSettings.MONITORED_CHANNELS
    
    async def handle_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        """
        Processa mudanças de estado de voz
        
        Args:
            member: Membro cujo estado mudou
            before: Estado anterior
            after: Estado atual
        """
        try:
            if after.self_deaf and not before.self_deaf and after.channel:
                await self._handle_audio_deactivated(member, after.channel)
            
            elif not after.self_deaf and before.self_deaf:
                await self._handle_audio_activated(member)
            
            elif (after.channel and before.channel and 
                  after.channel != before.channel and 
                  after.self_deaf):
                await self._handle_channel_change_muted(member, after.channel)
            
            elif (after.channel and not before.channel and 
                  after.self_deaf):
                await self._handle_join_muted(member, after.channel)
            
            elif not after.channel and before.channel:
                await self._handle_leave_channel(member)
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar mudança de estado de voz para {member.name}: {e}")
    
    async def _handle_audio_deactivated(self, member: discord.Member, channel: discord.VoiceChannel) -> None:
        """Processa quando um usuário desativa o áudio"""
        if not should_monitor_channel(channel, self.monitored_channels):
            logger.debug(f"⏭️ Canal {channel.name} não está sendo monitorado")
            return
        
        logger.info(f"🔇 {member.name} desativou o áudio no canal {channel.name}")
        
        task = asyncio.create_task(self._check_mute_timeout(member))
        self.user_manager.add_muted_user(member.id, task)
    
    async def _handle_audio_activated(self, member: discord.Member) -> None:
        """Processa quando um usuário ativa o áudio"""
        logger.info(f"🔊 {member.name} ativou o áudio")
        self.user_manager.remove_muted_user(member.id)
    
    async def _handle_channel_change_muted(self, member: discord.Member, new_channel: discord.VoiceChannel) -> None:
        """Processa quando um usuário muda de canal com áudio desativado"""
        if should_monitor_channel(new_channel, self.monitored_channels):
            logger.info(f"🔄 {member.name} mudou para {new_channel.name} com áudio desativado")
            
            task = asyncio.create_task(self._check_mute_timeout(member))
            self.user_manager.add_muted_user(member.id, task)
        else:
            self.user_manager.remove_muted_user(member.id)
            logger.debug(f"⏭️ {member.name} mudou para canal não monitorado: {new_channel.name}")
    
    async def _handle_join_muted(self, member: discord.Member, channel: discord.VoiceChannel) -> None:
        """Processa quando um usuário entra em um canal já com áudio desativado"""
        if should_monitor_channel(channel, self.monitored_channels):
            logger.info(f"🚪 {member.name} entrou no canal {channel.name} com áudio já desativado")
            
            task = asyncio.create_task(
                self._check_mute_timeout(member, self.join_muted_timeout, "join_muted")
            )
            self.user_manager.add_muted_user(member.id, task)
        else:
            logger.debug(f"⏭️ Canal {channel.name} não está sendo monitorado")
    
    async def _handle_leave_channel(self, member: discord.Member) -> None:
        """Processa quando um usuário sai do canal de voz"""
        self.user_manager.remove_muted_user(member.id)
    
    async def _check_mute_timeout(self, member: discord.Member, timeout_duration: Optional[int] = None, join_type: str = "normal") -> None:
        """
        Verifica se o usuário ainda está mutado após o timeout
        
        Args:
            member: Membro a ser verificado
            timeout_duration: Duração do timeout (None para usar o padrão)
            join_type: Tipo de entrada ("normal" ou "join_muted")
        """
        try:
            if timeout_duration is None:
                timeout_duration = self.mute_timeout
            
            await asyncio.sleep(timeout_duration)
            
            if (member.voice and 
                member.voice.channel and 
                member.voice.self_deaf):
                
                original_channel = member.voice.channel
                
                await self.channel_manager.move_user_to_afk(member, original_channel)
                
                if join_type == "join_muted":
                    logger.info(f"🚪 {member.name} foi movido por entrar mutado e ficar {timeout_duration} segundos")
                else:
                    logger.info(f"🔄 {member.name} foi movido por ficar com áudio desativado por {timeout_duration} segundos")
            
            self.user_manager.remove_muted_user(member.id)
            
        except asyncio.CancelledError:
            self.user_manager.remove_muted_user(member.id)
        except Exception as e:
            logger.error(f"❌ Erro ao verificar timeout para {member.name}: {e}")
            self.user_manager.remove_muted_user(member.id)
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do monitoramento
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            "monitored_users": self.user_manager.get_user_count(),
            "mute_timeout": self.mute_timeout,
            "join_muted_timeout": self.join_muted_timeout,
            "monitored_channels": self.monitored_channels if self.monitored_channels else "Todos"
        }
    
    def shutdown(self) -> None:
        """Desliga o monitoramento e cancela todas as tarefas"""
        self.user_manager.shutdown()
        logger.info("Monitor de voz desligado")
