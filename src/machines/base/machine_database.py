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
from machines.types.not_introduction import NotIntroduction
from machines.types.false_introduction import FalseIntroduction
from machines.types.or_elimination import OrElimination
from machines.types.double_not_elimination import DoubleNotElimination

class MachineData:
    def __init__(self, id, name, size, sprite_path, cls, icon_path=None, description=""):
        self.id = id
        self.name = name
        self.size = size
        self.sprite_path = sprite_path
        self.icon_path = icon_path or sprite_path
        self.cls = cls
        self.description = description
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
    cls=Generator, # class
    description="Choose which letter should be generated"
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
    cls=Negator,
    description=(
        "Machine to negate a formula \n"
        "the input must be a formula (Not a Theorem!)"
    )
))

# Binary connectives
database.register_machine(MachineData(
    id="binary_connective",
    name="Binary Connective",
    size=(2, 3),
    sprite_path="assets/sprites/binary_connective.png",
    icon_path=None,
    cls=BinaryConnective,
    description=(
        "Machine to connect two formulas \n"
        "both inputs must be formulas (Not Theorems)"
    )
))

# or introduction
# maybe it will be the general introduction, and you can select the connective in a menu
database.register_machine(MachineData(
    id="or_intro",
    name="Or Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/or_intro.png",
    icon_path=None,
    cls=OrIntroduction,
    description=(
        "Machine to prove a Or-Statement \n"
        "One of the two inputs must be a theorem. \n"
        "The other input can be a formula or theorem. \n"
        "The output will be the or-connection of the two inputs as a Theorem."
    )
))

# and introduction
database.register_machine(MachineData(
    id="and_intro",
    name="And Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/and_intro.png",
    icon_path=None,
    cls=AndIntroduction,
    description=(
        "Machine to prova a And-Statement \n"
        "Both inputs must be theorems. \n"
        "The output will be the And-connection of the two inputs."
    )
))

# and elimination
database.register_machine(MachineData(
    id="and_elim",
    name="And Elimination",
    size=(3, 3),
    sprite_path="assets/sprites/and_elim.png",
    icon_path=None,
    cls=AndElimination,
    description=(
        "Machine to extract information of an And-Theorem \n"
        "The input must be a theorem of the form 'A and B'.\n"
        "You can select the output: Either 'A' or 'B'."
    )
))

# assumption machine
database.register_machine(MachineData(
    id="assumption",
    name="Assumption Machine",
    size=(2, 3),
    sprite_path="assets/sprites/assumption.png",
    icon_path=None,
    cls=Assumption,
    description=(
        "Machine to make assumptions. \n"
        "The input must be a formula (not a theorem). \n"
        "The output will be the same thing, but as Theorem that relies on its own assumption."
    )
))

# implication introduction
database.register_machine(MachineData(
    id="implication_intro",
    name="Implication Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/implication_intro.png",
    icon_path=None,
    cls=ImplicationIntroduction,
    description=(
        "Machine to prove an Implication-Theorem. \n"
        "The premise-input must be a formula. \n"
        "The conclusion-input must be a theorem that has the premise in its assumptions. \n"
        "The output will be 'premise implies conclusion'"
    )
))

# implication elimination
database.register_machine(MachineData(
    id="implication_elim",
    name="Implication Elimination",
    size=(3, 3),
    sprite_path="assets/sprites/implication_elim.png",
    icon_path=None,
    cls=ImplicationElimination,
    description=(
        "Machine to extract information from an Implication-Theorem. \n"
        "The implication-input must be a implication-theorem. \n"
        "The premise-input must be the premise of the implication (As theorem) \n"
        "The output will be the conclusion of the implication."
    )
))

# not introduction
database.register_machine(MachineData(
    id="not_intro",
    name="Not Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/not_intro.png",
    icon_path=None,
    cls=NotIntroduction,
    description=(
        "Machine to prove a Not-Theorem. \n"
        "The Assumption-input 'A' must be a formula (not a theorem). \n"
        "The False-Input must be 'False' as theorem with 'A' in its assumptions. \n"
        "The output will be the theorem 'not A'"
    )
))

# false introduction
database.register_machine(MachineData(
    id="false_intro",
    name="False Introduction",
    size=(3, 3),
    sprite_path="assets/sprites/false_intro.png",
    icon_path=None,
    cls=FalseIntroduction,
    description=(
        "Machine to prove the Theorem 'False'. \n"
        "The inputs must be theorems that contradict each other, \n"
        "meaning input1 = 'A'; input2 = 'not A'. \n"
        "The output will be 'False' as theorem."
    )
))

# or elimination
database.register_machine(MachineData(
    id="or_elimination",
    name="Or Elimination",
    size=(3, 5),
    sprite_path="assets/sprites/or_elim.png",
    icon_path=None,
    cls=OrElimination,
    description=(
        "Machine to extract information from an or-theorem. \n"
        "The middle input must be a theorem of the form 'A or B'. \n"
        "The input above must be a theorem of the form 'A -> C'. \n"
        "The input below must be a theorem of the form 'B -> C'. \n"
        "The output will be the theorem 'C'."
    )
))

# double not elimination
database.register_machine(MachineData(
    id="double_not_elimination",
    name="Double-Not-Elimination",
    size=(3, 3),
    sprite_path="assets/sprites/double_not_elim.png",
    icon_path=None,
    cls=DoubleNotElimination,
    description=(
        "Machine to get rid of double negations. \n"
        "The input must be a theorem of the form 'not not A'. \n"
        "The output will be the theorem 'A'."
    )
))
