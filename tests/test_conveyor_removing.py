import pytest

from grid.grid_coordinator import GridCoordinator
from entities.port import Direction

from tests.test_utils import create_belt, initialize_pygame

# setup for tests
@pytest.fixture
def grid():
    initialize_pygame()
    grid = GridCoordinator()
    #connection = ConnectionSystem(grid.grid_manager)
    return grid


# in this file we test the removal of a conveyor belt and ensure that the connections are updated correctly.
# We do integration tests, so we also test the grid-system and the connection system.


def test_create_and_remove_conveyor_belt(grid):
    """Test creating and removing a conveyor belt"""
    # create the conveyor belt
    belt = create_belt() # standard direction: (->)
    grid.add_block(0, 0, belt)

    assert grid.get_block(0, 0) is belt
    assert grid.get_block(1, 0) is None  # next tile should be empty

    # remove the belt
    removed_belt = grid.remove_block(0, 0)
    assert removed_belt is belt
    assert grid.get_block(0, 0) is None

    # ensure that the occupied tiles are cleared
    assert (0, 0) not in grid.grid_manager.occupied_tiles


def test_remove_conveyor_belt_updates_neighbors1(grid):
    """
    Test that removing a conveyor belt updates neighboring belts
    We create the following setup: (->)(↴).
    Wen we remove the first belt, the secon belt should no longer be a curve, but a straight belt (from north to south).
    """
    # create two conveyor belts next to each other
    belt1 = create_belt(rotation=0)  # (->)
    belt2 = create_belt(rotation=1)  # (↴)

    grid.add_block(0, 0, belt1)
    grid.add_block(1, 0, belt2) # right of the first belt

    assert grid.get_block(0, 0) is belt1
    assert grid.get_block(1, 0) is belt2

    # check, if belt2 is a curve
    assert belt2.inputs == [Direction.SOUTH]
    assert belt2.outputs == [Direction.EAST]

    # check if the belts are connected
    assert belt1.output_ports[0].connected_port is belt2.input_ports[0]
    assert belt2.input_ports[0].connected_port is belt1.output_ports[0]

    # remove the first belt
    removed_belt = grid.remove_block(0, 0)
    assert removed_belt is belt1
    assert grid.get_block(0, 0) is None

    # check if belt2 is now a straight belt
    assert belt2.inputs == [Direction.WEST]
    assert belt2.outputs == [Direction.EAST]

    # check, if the connection is away
    assert belt2.input_ports[0].connected_port is None
    assert belt2.output_ports[0].connected_port is None


def test_remove_conveyor_belt_updates_neighbors2(grid):
    """
    More complicated situation: (->)(↑)(<-)
    First, the center belt should be an intersection (with also the bottom input)
    When we remove the right belt, the center belt should become a curve. (the center input should disappear)
    """
    # create three conveyor belts in a T-shape
    belt1 = create_belt(rotation=0)  # (->)
    belt2 = create_belt(rotation=3)  # (↑)
    belt3 = create_belt(rotation=2)  # (<-)

    grid.add_block(0, 0, belt1)
    grid.add_block(1, 0, belt2)
    grid.add_block(2, 0, belt3)

    assert grid.get_block(0, 0) is belt1
    assert grid.get_block(1, 0) is belt2
    assert grid.get_block(2, 0) is belt3

    # check if the center belt is an intersection
    assert set(belt2.inputs) == set([Direction.WEST, Direction.NORTH, Direction.SOUTH])
    assert belt2.outputs == [Direction.EAST]

    # check if the belts are connected
    assert belt1.output_ports[0].connected_port in belt2.input_ports
    assert belt3.output_ports[0].connected_port in belt2.input_ports
    assert belt1.input_ports[0].connected_port is None # no input from the left

    # remove the right belt
    removed_belt = grid.remove_block(2, 0)
    assert removed_belt is belt3
    assert grid.get_block(2, 0) is None

    # check if the center belt is now a curve
    assert belt2.inputs == [Direction.NORTH]
    assert belt2.outputs == [Direction.EAST]




