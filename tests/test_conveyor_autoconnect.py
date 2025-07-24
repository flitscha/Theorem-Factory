import pygame
import pytest

# important: dont import it with src.path, because it would not be compatible with the imports in the src folder
from entities.port import Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.types.conveyor_belt.belt_autoconnect import ConveyorBeltAutoConnector
from grid.grid_manager import GridManager
from grid.connection_system import ConnectionSystem
from machines.base.machine_database import MachineData


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

# setup for tests
@pytest.fixture
def grid_and_connection():
    grid = GridManager()
    connection = ConnectionSystem(grid)
    return grid, connection

# ----------------------------------------------------------------------------
# We will now test the _update_io method of ConveyorBeltAutoConnector
# We always place a conveyor belt with default rotation (from west to east)
# We test the resulting inputs and outputs of the belt after calling _update_io with different neighbors
# ----------------------------------------------------------------------------


# ------------ no neighbors ------------
def test_update_io_no_neighbors(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    
    ConveyorBeltAutoConnector._update_io(belt, {})
    
    # expected: inputs = [Direction.WEST], outputs = [Direction.EAST]
    assert belt.inputs == [Direction.WEST]
    assert belt.outputs == [Direction.EAST]


# ------------ one neighbor ------------
# neighbor (WEST) provides output to the east. (n->)(->)
def test_update_io_with_neighbor_output(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor = create_belt(rotation=0, inputs=[Direction.WEST], outputs=[Direction.EAST])
    
    neighbors = {
        Direction.WEST: neighbor,
        Direction.EAST: None,
        Direction.NORTH: None,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.WEST], outputs = [Direction.EAST]
    assert belt.inputs == [Direction.WEST]
    assert belt.outputs == [Direction.EAST]


# neighbor (EAST) provides output to the west. (->)(<-n)
def test_update_io_with_output_facing_to_output(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor = create_belt(rotation=0, inputs=[Direction.EAST], outputs=[Direction.WEST])
    
    neighbors = {
        Direction.WEST: None,
        Direction.EAST: neighbor,
        Direction.NORTH: None,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.WEST], outputs = [Direction.EAST] (the input should not move to the east)
    assert belt.inputs == [Direction.WEST]
    assert belt.outputs == [Direction.EAST]


# neighbor (WEST) provides input to the east. (<-n)(->)
def test_update_io_with_input_facing_to_input(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor = create_belt(rotation=0, inputs=[Direction.EAST], outputs=[Direction.WEST])
    
    neighbors = {
        Direction.WEST: neighbor,
        Direction.EAST: None,
        Direction.NORTH: None,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.WEST], outputs = [Direction.EAST]. (here again, nothing should connect)
    assert belt.inputs == [Direction.WEST]
    assert belt.outputs == [Direction.EAST]


# neighbor (NORTH) provides output to the south. (↳)
def test_update_io_with_curve1(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor = create_belt(rotation=0, inputs=[Direction.NORTH], outputs=[Direction.SOUTH])
    
    neighbors = {
        Direction.WEST: None,
        Direction.EAST: None,
        Direction.NORTH: neighbor,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.NORTH], outputs = [Direction.EAST] (a curve from north the east)
    assert belt.inputs == [Direction.NORTH]
    assert belt.outputs == [Direction.EAST]


# neighbor (SOUTH) provides output to the north. (↱)
def test_update_io_with_curve2(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor = create_belt(rotation=0, inputs=[Direction.SOUTH], outputs=[Direction.NORTH])
    
    neighbors = {
        Direction.WEST: None,
        Direction.EAST: None,
        Direction.NORTH: None,
        Direction.SOUTH: neighbor
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.SOUTH], outputs = [Direction.EAST] (a curve from south to east)
    assert belt.inputs == [Direction.SOUTH]
    assert belt.outputs == [Direction.EAST]



# ------------ 2 neighbors ------------
# neighbor (WEST) privides output to the east, neighbor (NORTH) provides output to the south.
def test_update_io_with_two_neighbors1(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor_west = create_belt(rotation=0, inputs=[Direction.WEST], outputs=[Direction.EAST])
    neighbor_north = create_belt(rotation=0, inputs=[Direction.NORTH], outputs=[Direction.SOUTH])
    
    neighbors = {
        Direction.WEST: neighbor_west,
        Direction.EAST: None,
        Direction.NORTH: neighbor_north,
        Direction.SOUTH: None
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [Direction.WEST, Direction.NORTH], outputs = [Direction.EAST]
    assert set(belt.inputs) == set([Direction.WEST, Direction.NORTH])
    assert belt.outputs == [Direction.EAST]


# ----------- 4 neighbors ------------
# 4 neighbors, all providing outputs to the direction of the belt
def test_update_io_with_four_neighbors_outputs(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor_west = create_belt(rotation=0, inputs=[Direction.WEST], outputs=[Direction.EAST])
    neighbor_east = create_belt(rotation=0, inputs=[Direction.EAST], outputs=[Direction.WEST])
    neighbor_north = create_belt(rotation=0, inputs=[Direction.NORTH], outputs=[Direction.SOUTH])
    neighbor_south = create_belt(rotation=0, inputs=[Direction.SOUTH], outputs=[Direction.NORTH])
    
    neighbors = {
        Direction.WEST: neighbor_west,
        Direction.EAST: neighbor_east,
        Direction.NORTH: neighbor_north,
        Direction.SOUTH: neighbor_south
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [WEST, NORTH, SOUTH], outputs = [Direction.EAST]
    assert set(belt.inputs) == set([Direction.WEST, Direction.NORTH, Direction.SOUTH])
    assert belt.outputs == [Direction.EAST]


# 4 neighbors, all prividing inputs to the direction of the belt
def test_update_io_with_four_neighbors_inputs(grid_and_connection):
    grid, connection = grid_and_connection
    belt = create_belt()
    neighbor_west = create_belt(rotation=0, inputs=[Direction.EAST], outputs=[Direction.WEST])
    neighbor_east = create_belt(rotation=0, inputs=[Direction.WEST], outputs=[Direction.EAST])
    neighbor_north = create_belt(rotation=0, inputs=[Direction.SOUTH], outputs=[Direction.NORTH])
    neighbor_south = create_belt(rotation=0, inputs=[Direction.NORTH], outputs=[Direction.SOUTH])
    
    neighbors = {
        Direction.WEST: neighbor_west,
        Direction.EAST: neighbor_east,
        Direction.NORTH: neighbor_north,
        Direction.SOUTH: neighbor_south
    }

    ConveyorBeltAutoConnector._update_io(belt, neighbors)

    # Expected: inputs = [WEST], outputs = [NORTH, SOUTH, EAST]
    assert set(belt.inputs) == set([Direction.WEST])
    assert set(belt.outputs) == set([Direction.NORTH, Direction.SOUTH, Direction.EAST])