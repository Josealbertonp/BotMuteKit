"""
Funções auxiliares reutilizáveis
"""
from typing import List
import discord

def should_monitor_channel(channel: discord.VoiceChannel, monitored_channels: List[str]) -> bool:
    """
    Verifica se um canal deve ser monitorado baseado na configuração
    
    Args:
        channel: Canal de voz a ser verificado
        monitored_channels: Lista de canais monitorados
    
    Returns:
        True se o canal deve ser monitorado, False caso contrário
    """
    if not monitored_channels:
        return True
    
    return channel.name.lower() in monitored_channels

def format_duration(seconds: int) -> str:
    """
    Formata duração em segundos para formato legível
    
    Args:
        seconds: Duração em segundos
    
    Returns:
        String formatada (ex: "2 minutos 30 segundos")
    """
    if seconds < 60:
        return f"{seconds} segundos"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes} minutos"
        else:
            return f"{minutes} minutos {remaining_seconds} segundos"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        if remaining_minutes == 0:
            return f"{hours} horas"
        else:
            return f"{hours} horas {remaining_minutes} minutos"

def sanitize_channel_name(name: str) -> str:
    """
    Sanitiza o nome de um canal para uso seguro
    
    Args:
        name: Nome do canal
    
    Returns:
        Nome sanitizado
    """
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    sanitized = name
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '')
    
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized.strip()
