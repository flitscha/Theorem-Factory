# this file contains functions to determine the shape of a conveyor belt based on neighboring machines and belts

from typing import List, Optional
from entities.port import Port, Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine


def determine_inputs_and_output(belt: ConveyorBelt, neighboring_machines: dict[Direction, Machine]) -> tuple:
    """Determine inputs and outputs of a belt based on neighboring machines."""
    inputs = [Direction.WEST]  # default input direction
    outputs = [Direction.EAST]  # default output direction

    return inputs, outputs


def determine_belt_sprite(inputs: List[Direction], outputs: List[Direction]) -> str:
    """Determine the sprite name based on inputs and outputs."""
    return "assets/sprites/conveyor_belt.png"


def update_neighboring_belt(neighbor: ConveyorBelt, direction: Direction, conveyor: ConveyorBelt) -> None:
    """when placing a new belt, update the neighboring belt's inputs and outputs."""
    print(f"Updating neighboring belt at {neighbor.origin} with direction {direction}")
    neighbor.inputs.append(direction)
    pass

def update_neighboring_belt_when_removing(neighbor: ConveyorBelt, removed_machine: Machine) -> None:
    """Update neighboring belts when a block is removed."""
    pass