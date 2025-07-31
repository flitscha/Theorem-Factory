from abc import ABC, abstractmethod # ABC = Abstract Base classes
from typing import Optional, Tuple, List
from entities.item import Item
from entities.port import Port

class IUpdatable(ABC):
    """Interface for objects that can be updated each frame"""
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the object."""
        pass

class IProvider(ABC):
    """Interface for objects that can provide items (machines, etc.)"""
    output_ports: List[Port] # List of output ports for providing items

    @abstractmethod
    def provide_item_from_port(self, port):
        """Called when an output port is asked for an item"""
        pass

    @abstractmethod
    def handle_backpressure(self, item: Item, port: Port):
        """Handle backpressure when output is blocked"""
        pass

class IReceiver(ABC):
    """Interface for objects that can receive items (machines, etc.)"""
    input_ports: List[Port] # List of input ports for receiving items

    @abstractmethod
    def receive_item_at_port(self, item, port) -> bool:
        """Called when an input port receives an item"""
        pass