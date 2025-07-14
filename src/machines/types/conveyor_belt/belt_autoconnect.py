# this file contains functions to determine the shape of a conveyor belt based on neighboring machines and belts

from typing import List, Optional
from entities.port import Port, Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine


def update_inputs_and_output(belt: ConveyorBelt, neighboring_machines: dict[Direction, Optional[Machine]]) -> None:
    """Determine inputs and outputs of a belt based on neighboring machines."""
    inputs = []
    outputs = []

    for direction, neighbor in neighboring_machines.items():
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


def determine_belt_sprite(inputs: List[Direction], outputs: List[Direction]) -> str:
    """Determine the sprite name based on inputs and outputs."""
    return "assets/sprites/conveyor_belt.png"


def update_neighboring_belt(neighbor: ConveyorBelt, direction: Direction, conveyor: ConveyorBelt) -> None:
    """when placing a new belt, update the neighboring belt's inputs and outputs."""

    # set the ports based on the new inputs and outputs
    neighbor.init_ports()
    neighbor.rotate_ports()

def update_neighboring_belt_when_removing(neighbor: ConveyorBelt, removed_machine: Machine) -> None:
    """Update neighboring belts when a block is removed."""
    pass