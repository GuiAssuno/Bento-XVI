"""
Módulos da Assistente de Bordo
"""

from .voice_interface import VoiceInterface
from .vehicle_control import VehicleControl
from .knowledge_base import KnowledgeBase
from .computer_vision import ComputerVision
from .machine_learning import MachineLearningModule
from .data_processor import DataProcessor

__all__ = [
    'VoiceInterface',
    'VehicleControl',
    'KnowledgeBase',
    'ComputerVision',
    'MachineLearningModule',
    'DataProcessor'
]

