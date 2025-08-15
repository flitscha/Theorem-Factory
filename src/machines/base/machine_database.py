import pygame

from machines.types.generator import Generator
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.types.negator import Negator
from machines.types.binary_connective import BinaryConnective
from machines.types.or_introduction import OrIntroduction
from machines.types.and_introduction import AndIntroduction
from machines.types.and_elimination import AndElimination
from machines.types.assumption import Assumption
from machines.types.implication_introduction import ImplicationIntroduction
from machines.types.implication_elimination import ImplicationElimination

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
    sprite_path="assets/sprites/conveyorbelts/normal/horizontal.png",
    icon_path=None,
    cls=ConveyorBelt
))

# Negator
database.register_machine(MachineData(
    id="negator",
    name="Negator",
    size=(2, 2),
    sprite_path="assets/sprites/negator.png",
    icon_path=None,
    cls=Negator
))

# Binary connectives
database.register_machine(MachineData(
    id="binary_connective",
    name="Binary Connective",
    size=(2, 3),
    sprite_path="assets/sprites/binary_connective.png",
    icon_path=None,
    cls=BinaryConnective
))

# or introduction
# maybe it will be the general introduction, and you can select the connective in a menu
database.register_machine(MachineData(
    id="or_intro",
    name="Or Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/or_intro.png",
    icon_path=None,
    cls=OrIntroduction
))

# and introduction
database.register_machine(MachineData(
    id="and_intro",
    name="And Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/and_intro.png",
    icon_path=None,
    cls=AndIntroduction
))

# and elimination
database.register_machine(MachineData(
    id="and_elim",
    name="And Elimination",
    size=(3, 3),
    sprite_path="assets/sprites/and_elim.png",
    icon_path=None,
    cls=AndElimination
))

# assumption machine
database.register_machine(MachineData(
    id="assumption",
    name="Assumption Machine",
    size=(2, 3),
    sprite_path="assets/sprites/assumption.png",
    icon_path=None,
    cls=Assumption
))

# implication introduction
database.register_machine(MachineData(
    id="implication_intro",
    name="Implication Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/implication_intro.png",
    icon_path=None,
    cls=ImplicationIntroduction
))

# implication elimination
database.register_machine(MachineData(
    id="implication_elim",
    name="Implication Elimination",
    size=(3, 3),
    sprite_path="assets/sprites/implication_elim.png",
    icon_path=None,
    cls=ImplicationElimination
))
