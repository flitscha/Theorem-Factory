import pytest

from grid.grid_coordinator import GridCoordinator
from machines.types.conveyor_belt.belt_autoconnect import ConveyorBeltAutoConnector
from entities.port import Direction

from tests.test_utils import create_belt, initialize_pygame, create_generator


# setup for tests
@pytest.fixture
def grid():
    initialize_pygame()
    grid = GridCoordinator()
    return grid


# ----------- simple unit tests for generator-belt connections -----------

# neighbor (NORTH) is a generator, providing output to the south.
def test_update_io_with_generator1():
    belt = create_belt()
    belt.origin = (0, 0)
    belt.init_ports()
    belt.rotate_ports()
    neighbor = create_generator(rotation=0)
    neighbor.origin = (-1, -3)
    neighbor.init_ports()
    neighbor.rotate_ports()
    
    neighbors = {
        Direction.WEST: None,
        Direction.EAST: None,
        Direction.NORTH: neighbor,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [NORTH], outputs = [EAST]
    assert belt.inputs == [Direction.NORTH]
    assert belt.outputs == [Direction.EAST]


# neighbor (WEST) is a generator, providing output to the EAST. (belt is rotated from south to north)
def test_update_io_with_generator2():
    belt = create_belt(rotation=3)
    belt.init_ports()
    belt.rotate_ports()
    neighbor = create_generator(rotation=3)
    neighbor.origin = (-3, -1)
    neighbor.init_ports()
    neighbor.rotate_ports()
    
    neighbors = {
        Direction.WEST: neighbor,
        Direction.EAST: None,
        Direction.NORTH: None,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [NORTH], outputs = [EAST]
    assert belt.inputs == [Direction.NORTH] # directions are not affected by rotation
    assert belt.outputs == [Direction.EAST]


# ----------- Integration tests -------------

def test_update_neighboring_belts_when_placing1(grid):
    """Test that placing a generator updates neighboring belts"""
    belt = create_belt(rotation=0)
    grid.add_block(0, 0, belt)
    assert grid.get_block(0, 0) is belt

    # create a generator to the north
    generator = create_generator(rotation=0)
    grid.add_block(-1, -3, generator)
    assert grid.get_block(-1, -3) is generator # check the corners. (generator is 3x3 tiles)
    assert grid.get_block(1, -3) is generator
    assert grid.get_block(-1, -1) is generator
    assert grid.get_block(1, -1) is generator

    # test, if the belt got updated: the belt should be a curve now: (↳)
    assert belt.inputs == [Direction.NORTH]
    assert belt.outputs == [Direction.EAST]


def test_update_neighboring_belts_when_placing2(grid):
    """
    Similar test, but involving multiple belts. Only one belt should get a new input.
    We create 3 belts, that go from NORTH to SOUTH. At the middle-left we place a generator.
    """
    belt1 = create_belt(rotation=1)
    belt2 = create_belt(rotation=1)
    belt3 = create_belt(rotation=1)
    generator = create_generator(rotation=3)

    # add the blocks to the grid
    grid.add_block(0, 0, belt1)
    grid.add_block(0, -1, belt2)
    grid.add_block(0, -2, belt3)
    grid.add_block(-3, -2, generator)

    # check the inputs and outputs of the belts
    assert belt1.inputs == [Direction.WEST]
    assert belt1.outputs == [Direction.EAST]
    assert set(belt2.inputs) == set([Direction.WEST, Direction.SOUTH])
    assert belt2.outputs == [Direction.EAST]
    assert belt3.inputs == [Direction.WEST]
    assert belt3.outputs == [Direction.EAST]


def test_update_neighboring_belts_when_removing1(grid):
    """
    We create the situation, where at the top of a belt is a generator. The belt turns into a curve.
    When removing the generator, the belt should get straight again.
    """
    belt = create_belt(rotation=2)
    grid.add_block(0, 0, belt)
    generator = create_generator(rotation=0)
    grid.add_block(-1, -3, generator)

    # check, if the belt is a curve
    assert belt.inputs == [Direction.SOUTH]
    assert belt.outputs == [Direction.EAST]

    # remove the generator
    grid.remove_block(-1, -3)
    assert grid.get_block(-1, -3) is None
    assert grid.get_block(1, 1) is None
    assert (-1, -3) not in grid.grid_manager.occupied_tiles
    assert (0, 1) not in grid.grid_manager.occupied_tiles

    # check, if the belt is straight
    assert belt.inputs == [Direction.WEST]
    assert belt.outputs == [Direction.EAST]


def test_update_neighboring_belts_when_removing2(grid):
    """
    Similar test, but involving multiple belts.
    We create 3 belts, that go from SOUTH to NORTH. At the middle-right we place a generator.
    Then we remove the generator.
    """
    belt1 = create_belt(rotation=3)
    belt2 = create_belt(rotation=3)
    belt3 = create_belt(rotation=3)
    generator = create_generator(rotation=3)

    # add the blocks to the grid
    grid.add_block(0, 0, belt1)
    grid.add_block(0, -1, belt2)
    grid.add_block(0, -2, belt3)
    grid.add_block(-3, -2, generator)

    # check the inputs and outputs of the belts
    assert belt1.inputs == [Direction.WEST]
    assert belt1.outputs == [Direction.EAST]
    assert set(belt2.inputs) == set([Direction.WEST, Direction.NORTH])
    assert belt2.outputs == [Direction.EAST]
    assert belt3.inputs == [Direction.WEST]
    assert belt3.outputs == [Direction.EAST]

    # remove the generator
    grid.remove_block(-2, 0) # the tile (-2, 0) is part of the generator
    assert grid.get_block(-3, -2) is None

    # check, if the middle belt updated
    assert belt2.inputs == [Direction.WEST]
    assert belt2.outputs == [Direction.EAST]

