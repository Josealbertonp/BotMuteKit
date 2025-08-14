"""
Serviço para gerenciar usuários mutados e suas tarefas de timeout
"""
import asyncio
import logging
from typing import Dict, Optional
import discord
from ..config.settings import BotSettings

logger = logging.getLogger(__name__)

class UserManager:
    """Gerencia usuários mutados e suas tarefas de timeout"""
    
    def __init__(self):
        self.muted_users: Dict[int, asyncio.Task] = {}
    
    def add_muted_user(self, user_id: int, task: asyncio.Task) -> None:
        """
        Adiciona um usuário mutado ao gerenciamento
        
        Args:
            user_id: ID do usuário
            task: Tarefa de timeout associada
        """
        if user_id in self.muted_users:
            self.muted_users[user_id].cancel()
        
        self.muted_users[user_id] = task
        logger.debug(f"Usuário {user_id} adicionado ao gerenciamento de mute")
    
    def remove_muted_user(self, user_id: int) -> None:
        """
        Remove um usuário mutado do gerenciamento
        
        Args:
            user_id: ID do usuário
        """
        if user_id in self.muted_users:
            if not self.muted_users[user_id].done():
                self.muted_users[user_id].cancel()
            
            del self.muted_users[user_id]
            logger.debug(f"Usuário {user_id} removido do gerenciamento de mute")
    
    def cancel_user_task(self, user_id: int) -> None:
        """
        Cancela a tarefa de um usuário específico
        
        Args:
            user_id: ID do usuário
        """
        if user_id in self.muted_users:
            if not self.muted_users[user_id].done():
                self.muted_users[user_id].cancel()
            logger.debug(f"Tarefa do usuário {user_id} cancelada")
    
    def is_user_muted(self, user_id: int) -> bool:
        """
        Verifica se um usuário está sendo gerenciado como mutado
        
        Args:
            user_id: ID do usuário
        
        Returns:
            True se o usuário está sendo gerenciado, False caso contrário
        """
        return user_id in self.muted_users
    
    def get_user_count(self) -> int:
        """
        Retorna o número de usuários sendo gerenciados
        
        Returns:
            Número de usuários mutados
        """
        return len(self.muted_users)
    
    def cleanup_completed_tasks(self) -> None:
        """Remove tarefas concluídas do dicionário"""
        completed_users = [
            user_id for user_id, task in self.muted_users.items()
            if task.done()
        ]
        
        for user_id in completed_users:
            del self.muted_users[user_id]
        
        if completed_users:
            logger.debug(f"Removidas {len(completed_users)} tarefas concluídas")
    
    def shutdown(self) -> None:
        """Cancela todas as tarefas pendentes"""
        for user_id, task in self.muted_users.items():
            if not task.done():
                task.cancel()
        
        self.muted_users.clear()
        logger.info("Todas as tarefas de usuários foram canceladas")
