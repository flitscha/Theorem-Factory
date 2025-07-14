import pygame

from machines.types.generator import Generator
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt

class MachineData:
    def __init__(self, id, name, size, sprite_path, cls, icon_path=None):
        self.id = id
        self.name = name
        self.size = size
        self.sprite_path = sprite_path
        self.icon_path = icon_path or sprite_path
        self.cls = cls
        self.image = None
        self.icon_image = None

    def load_image(self):
        self.image = pygame.image.load(self.sprite_path).convert_alpha()
        self.icon_image = pygame.image.load(self.icon_path).convert_alpha()


class MachineDatabase:
    def __init__(self):
        self.machines = {}

    def register_machine(self, machine_data):
        self.machines[machine_data.id] = machine_data

    def get(self, machine_id):
        return self.machines.get(machine_id)
    

# create the machine database
database = MachineDatabase()

# generator
database.register_machine(MachineData(
    id="generator",
    name="Generator",
    size=(3, 3),
    sprite_path="assets/sprites/generator.png",
    icon_path=None, # add later
    cls=Generator # class
))

# Conveyor Belt
database.register_machine(MachineData(
    id="conveyor",
    name="Conveyor Belt",
    size=(1, 1),
    sprite_path="assets/sprites/conveyor_belt_vertical.png",
    icon_path=None,
    cls=ConveyorBelt
))

# test machine
database.register_machine(MachineData(
    id="machine2",
    name="Machine2",
    size=(3, 2),
    sprite_path="assets/sprites/generator.png",
    icon_path=None,
    cls=Generator
))