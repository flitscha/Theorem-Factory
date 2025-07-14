# this file contains functions to determine the shape of a conveyor belt based on neighboring machines and belts

from typing import List, Optional
from entities.port import Port, Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine


def update_inputs_and_output(belt: ConveyorBelt, neighboring_machines: dict[Direction, Optional[Machine]]) -> None:
    """Determine inputs and outputs of a belt based on neighboring machines."""
    inputs = [Direction.WEST]  # default input direction
    outputs = [Direction.EAST]  # default output direction

    machine_north = neighboring_machines.get(Direction.NORTH)
    machine_south = neighboring_machines.get(Direction.SOUTH)
    machine_west = neighboring_machines.get(Direction.WEST)
    machine_east = neighboring_machines.get(Direction.EAST)

    

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