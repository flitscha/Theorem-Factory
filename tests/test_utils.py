import pygame

from machines.base.machine_database import MachineData
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.types.generator import Generator


def initialize_pygame():
    """Initialize pygame and create main window"""
    pygame.init()
    pygame.display.set_mode((1, 1))


# helper function to create a conveyor belt with given rotation and inputs/outputs
def create_belt(rotation=0, inputs=None, outputs=None):
    # Dummy MachineData
    data = MachineData(
        id="conveyor",
        name="Conveyor Belt",
        size=(1, 1),
        sprite_path="dummy.png",
        cls=ConveyorBelt
    )
    # Dummy Belt
    belt = ConveyorBelt(data, rotation=rotation)
    if inputs is not None:
        belt.inputs = inputs
    if outputs is not None:
        belt.outputs = outputs
    belt.init_ports()
    belt.rotate_ports()
    return belt


def create_generator(rotation=0):
    # Dummy MachineData for a generator
    data = MachineData(
        id="generator",
        name="Generator",
        size=(3, 3),
        sprite_path="dummy.png",
        cls=Generator
    )
    generator = Generator(data, rotation=rotation)
    generator.init_ports()
    generator.rotate_ports()
    return generator