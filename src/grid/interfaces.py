from abc import ABC, abstractmethod # ABC = Abstract Base classes
from typing import Optional, Tuple, List
from entities.item import Item

class IUpdatable(ABC):
    """Interface for objects that can be updated each frame"""
    @abstractmethod
    def update(self, dt: float) -> Optional[Item]:
        """Update the object. Return item if it needs to be handled by grid"""
        pass

class IConveyorNode(ABC):
    """Interface for objects that can transport items (conveyor belts)"""
    @abstractmethod
    def try_accept_item(self, item: Item) -> bool:
        """Try to accept an item. Return True if accepted"""
        pass
    
    @abstractmethod
    def try_output_item(self) -> Optional[Item]:
        """Try to output an item. Return item if available"""
        pass
    
    @abstractmethod
    def get_output_position(self) -> Tuple[int, int]:
        """Get the grid position where this node outputs items"""
        pass
    
    @abstractmethod
    def is_ready_to_output(self) -> bool:
        """Check if this node has an item ready to output"""
        pass

class IItemAcceptor(ABC):
    """Interface for machines that can accept items (machines, etc.)"""
    @abstractmethod
    def try_accept_item(self, item: Item) -> bool:
        """Try to accept an item. Return True if accepted"""
        pass

class IItemProducer(ABC):
    """Interface for machines that can produce items (generators, etc.)"""
    @abstractmethod
    def try_produce_item(self) -> Optional[Item]:
        """Try to produce an item. Return item if produced"""
        pass