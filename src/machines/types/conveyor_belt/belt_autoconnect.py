from typing import List, Optional
from entities.port import Port, Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine


class ConveyorBeltAutoConnector:
    """Handles automatic connection and configuration of conveyor belts based on neighboring machines."""

    @staticmethod
    def configure(belt: ConveyorBelt, neighbors: dict):
        ConveyorBeltAutoConnector._update_io(belt, neighbors)
        ConveyorBeltAutoConnector._update_sprite(belt)
    
    @staticmethod
    def _update_io(belt: ConveyorBelt, neighbors: dict[Direction, Optional[Machine]]) -> None:
        """Determine inputs and outputs of a belt based on neighboring machines."""
        inputs = []
        outputs = []

        for direction, neighbor in neighbors.items():
            # at the moment, we only care about neighboring conveyor belts
            if isinstance(neighbor, ConveyorBelt):
                # rotate the direction to match the belt's rotation
                rotated_direction = direction.rotate(-belt.rotation)
                rotated_neighbor_outputs = [output.rotate(neighbor.rotation - belt.rotation) for output in neighbor.outputs]
                rotated_neighbor_inputs = [input.rotate(neighbor.rotation - belt.rotation) for input in neighbor.inputs]

                # append inputs and outputs based on the neighbor's inputs and outputs
                if rotated_direction.opposite() in rotated_neighbor_outputs:
                    inputs.append(rotated_direction)
                if rotated_direction.opposite() in rotated_neighbor_inputs:
                    outputs.append(rotated_direction)

        # If no inputs or outputs are found, use default values
        if not inputs:
            inputs = [Direction.WEST]
        if not outputs:
            outputs = [Direction.EAST]
        
        # set inputs, outputs and ports
        belt.inputs = inputs
        belt.outputs = outputs
        belt.init_ports()
        belt.rotate_ports()

    
    @staticmethod
    def _update_sprite(belt: ConveyorBelt):
        """Update the sprite based on inputs and outputs."""
        
        # belt.rotation (0, 1, 2, 3) determines the orientation of the belt
        # belt.inputs and belt.outputs
        # belt.ports 
        ports = belt.ports # list of ports
        input_ports = belt.input_ports # list of input ports
        output_ports = belt.output_ports # list of output ports

        # port.direction
        # port.port_type

        # port.connected_port
        # if port.connected_port:
        #     belt is connected. -> use a different sprite


        # example:
        sprite_path = "assets/sprites/conveyor_belt_vertical_curve.png"
        horizontal_morror = True
        vertical_mirror = False
        
        belt.update_sprite(sprite_path, horizontal_morror, vertical_mirror)
    
    @staticmethod
    def configure_neighbor_when_removing(neighbor: ConveyorBelt, removed_machine: Machine) -> None:
        """Update a specific neighboring belt when a block is removed."""
        pass

    @staticmethod
    def configure_neighbor_when_placing(neighbor: ConveyorBelt, neighbors: dict, placed_machine: Machine):
        pass