"""
Configurações centralizadas do bot
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class BotSettings:
    """Configurações do bot Discord"""
    
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    MUTE_TIMEOUT = int(os.getenv("MUTE_TIMEOUT", "20"))
    JOIN_MUTED_TIMEOUT = int(os.getenv("JOIN_MUTED_TIMEOUT", "5"))
    
    AFK_CHANNEL_NAME = os.getenv("AFK_CHANNEL_NAME", "ausente")
    
    MONITORED_CHANNELS = os.getenv("MONITORED_CHANNELS", "").split(",") if os.getenv("MONITORED_CHANNELS") else []
    MONITORED_CHANNELS = [channel.strip().lower() for channel in MONITORED_CHANNELS if channel.strip()]
    
    @classmethod
    def validate(cls) -> bool:
        """Valida se as configurações obrigatórias estão presentes"""
        if not cls.DISCORD_TOKEN:
            return False
        return True
    
    @classmethod
    def get_intents(cls):
        """Retorna as intents configuradas para o bot"""
        import discord
        
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.members = True
        intents.guilds = True
        intents.message_content = True
        
        return intents
