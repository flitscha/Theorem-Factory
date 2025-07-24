from typing import List, Optional
from entities.port import Port, Direction
from machines.types.conveyor_belt.conveyor_belt import ConveyorBelt
from machines.base.machine import Machine


class ConveyorBeltAutoConnector:
    """Handles automatic connection and configuration of conveyor belts based on neighboring machines."""

    @staticmethod
    def configure(belt: ConveyorBelt, neighbors: dict, connection_system):
        ConveyorBeltAutoConnector._update_io(belt, neighbors)
        ConveyorBeltAutoConnector._update_port_connections(belt, connection_system)
        #ConveyorBeltAutoConnector.update_sprite(belt)
    
    @staticmethod
    def _update_io(belt: ConveyorBelt, neighbors: dict[Direction, Optional[Machine]]) -> None:
        """Determine inputs and outputs of a belt based on neighboring machines."""
        inputs = belt.inputs
        outputs = belt.outputs

        for direction, neighbor in neighbors.items():
            # at the moment, we only care about neighboring conveyor belts
            if isinstance(neighbor, ConveyorBelt):
                # rotate the direction to match the belt's rotation
                rotated_direction = direction.rotate(-belt.rotation) # position relative to the base-image of the belt. (goes from left to right)
                rotated_neighbor_outputs = [output.rotate(neighbor.rotation - belt.rotation) for output in neighbor.outputs]
                rotated_neighbor_inputs = [input.rotate(neighbor.rotation - belt.rotation) for input in neighbor.inputs]

                # define some useful variables
                neighbor_wants_to_output_here = rotated_direction.opposite() in rotated_neighbor_outputs
                neighbor_wants_to_input_here = rotated_direction.opposite() in rotated_neighbor_inputs
                # note: we cant do the same for THIS belt, because the inputs and outputs may not be set yet

                # avoid special cases where both belts want to output to each other
                if neighbor_wants_to_output_here and rotated_direction == Direction.EAST: # EAST is the default output direction (base image without rotation)
                    continue

                # avoid special cases where both belts want to input from each other
                if neighbor_wants_to_input_here and rotated_direction == Direction.WEST:
                    continue

                # append inputs and outputs based on the neighbor's inputs and outputs
                if rotated_direction.opposite() in rotated_neighbor_outputs:
                    inputs.append(rotated_direction)
                if rotated_direction.opposite() in rotated_neighbor_inputs:
                    outputs.append(rotated_direction)
                

        # If no inputs or outputs are found, use default values
        if not inputs:
            inputs = [Direction.WEST]
        
        # at east, we always have an output
        if Direction.EAST not in outputs:
            outputs.append(Direction.EAST)
        
        # remove duplicates
        inputs = list(set(inputs))
        outputs = list(set(outputs))

        # set inputs, outputs and ports
        belt.inputs = inputs
        belt.outputs = outputs
        belt.init_ports()
        belt.rotate_ports()

    @staticmethod
    def _update_port_connections(belt: ConveyorBelt, connection_system):
        connection_system.update_connections_at(*belt.origin)

    
    @staticmethod
    def update_sprite(belt: ConveyorBelt):
        """Update the sprite based on inputs and outputs."""
        # belt.rotation (0, 1, 2, 3) determines the orientation of the belt
        # belt.inputs and belt.outputs
        # belt.ports 
        ports = belt.ports # list of ports
        input_ports = belt.input_ports # list of input ports
        output_ports = belt.output_ports # list of output ports

        # port.direction
        # port.port_type

        # port.connected_port
        # if port.connected_port:
        #     belt is connected. -> use a different sprite

        sprite_path = None
        horizontal_mirror = False
        vertical_mirror = False

        # 1 INPUT AND 1 OUTPUT - REFACTORED
        if len(input_ports) == 1 and len(output_ports) == 1:
            input_dir = input_ports[0].direction
            output_dir = output_ports[0].direction

            """STRAIGHT BELTS"""
            # Horizontal belts
            if input_dir == Direction.WEST and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/normal/horizontal.png"
            
            elif input_dir == Direction.EAST and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/normal/horizontal.png"
                vertical_mirror = True
            
            # Vertical belts
            elif input_dir == Direction.NORTH and output_dir == Direction.SOUTH:
                sprite_path = "assets/sprites/conveyorbelts/normal/vertical.png"
            
            elif input_dir == Direction.SOUTH and output_dir == Direction.NORTH:
                sprite_path = "assets/sprites/conveyorbelts/normal/vertical.png"
                vertical_mirror = True

            """CURVED BELTS"""
            # Left curves
            if input_dir == Direction.WEST and output_dir == Direction.SOUTH:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_left_bottom.png"
            
            elif input_dir == Direction.WEST and output_dir == Direction.NORTH:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_left_top.png"
            
            # Right curves
            elif input_dir == Direction.EAST and output_dir == Direction.SOUTH:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_right_bottom.png"
            
            elif input_dir == Direction.EAST and output_dir == Direction.NORTH:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_right_top.png"
            
            # Bottom curves
            elif input_dir == Direction.SOUTH and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_bottom_left.png"
            
            elif input_dir == Direction.SOUTH and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_bottom_right.png"
            
            # Top curves
            elif input_dir == Direction.NORTH and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_top_left.png"
            
            elif input_dir == Direction.NORTH and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/curve/curve_top_right.png"


        """INTERSECTION BELTS"""

        # 2 INPUTS AND 1 OUTPUT
        if len(input_ports) == 2 and len(output_ports) == 1:
            input_dirs = {port.direction for port in input_ports}  # Set comprehension
            output_dir = output_ports[0].direction

            # Left-bottom to right (WEST+SOUTH → EAST)
            if input_dirs == {Direction.WEST, Direction.SOUTH} and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_bottom_to_right.png"
            
            # Mirrored case (EAST+SOUTH → WEST)
            elif input_dirs == {Direction.EAST, Direction.SOUTH} and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_bottom_to_right.png"
                vertical_mirror = True

            # Left-top to right (WEST+NORTH → EAST)
            elif input_dirs == {Direction.WEST, Direction.NORTH} and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_top_to_right.png"
            
            # Mirrored case (EAST+NORTH → WEST)
            elif input_dirs == {Direction.EAST, Direction.NORTH} and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_top_to_right.png"
                vertical_mirror = True

        # 1 INPUT AND 2 OUTPUTS
        elif len(input_ports) == 1 and len(output_ports) == 2:
            input_dir = input_ports[0].direction
            output_dirs = {port.direction for port in sorted(output_ports, key=lambda p: p.direction.value)}

            # Left to bottom-right (WEST → SOUTH+EAST)
            if input_dir == Direction.WEST and output_dirs == {Direction.SOUTH, Direction.EAST}:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_to_bottom_right.png"
            
            # Mirrored case (EAST → SOUTH+WEST)
            elif input_dir == Direction.EAST and output_dirs == {Direction.SOUTH, Direction.WEST}:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_to_bottom_right.png"
                vertical_mirror = True
            
            # Left to top-right (WEST → NORTH+EAST)
            elif input_dir == Direction.WEST and output_dirs == {Direction.NORTH, Direction.EAST}:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_to_top_right.png"
            
            # Mirrored case (EAST → NORTH+WEST)
            elif input_dir == Direction.EAST and output_dirs == {Direction.NORTH, Direction.WEST}:
                sprite_path = "assets/sprites/conveyorbelts/intersections/horizontal/left_to_top_right.png"
                vertical_mirror = True
        
        """CROSSSECTION BELTS"""
        
        # 1 INPUT AND 3 OUTPUTS
        if len(input_ports) == 1 and len(output_ports) == 3:
            input_dir = input_ports[0].direction
            output_dirs = {port.direction for port in output_ports}  # Set comprehension

            # Base case (WEST → NORTH+EAST+SOUTH)
            if input_dir == Direction.WEST and output_dirs == {Direction.NORTH, Direction.EAST, Direction.SOUTH}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_to_top_right_bottom.png"

            # Mirrored case (EAST → NORTH+WEST+SOUTH)
            elif input_dir == Direction.EAST and output_dirs == {Direction.NORTH, Direction.WEST, Direction.SOUTH}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_to_top_right_bottom.png"
                vertical_mirror = True

        # 3 INPUTS AND 1 OUTPUT
        if len(input_ports) == 3 and len(output_ports) == 1:
            input_dirs = {port.direction for port in input_ports}  # Set comprehension
            output_dir = output_ports[0].direction

            # Base case (WEST+NORTH+SOUTH → EAST)
            if input_dirs == {Direction.WEST, Direction.NORTH, Direction.SOUTH} and output_dir == Direction.EAST:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_top_bottom_to_right.png"

            # Mirrored case (EAST+NORTH+SOUTH → WEST)
            elif input_dirs == {Direction.EAST, Direction.NORTH, Direction.SOUTH} and output_dir == Direction.WEST:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_top_bottom_to_right.png"
                vertical_mirror = True
        
        # 2 INPUTS AND 2 OUTPUTS
        if len(input_ports) == 2 and len(output_ports) == 2:
            input_dirs = {port.direction for port in input_ports}  # Set comprehension
            output_dirs = {port.direction for port in output_ports}

            # Left-bottom to right-top (WEST+SOUTH → NORTH+EAST)
            if input_dirs == {Direction.WEST, Direction.SOUTH} and output_dirs == {Direction.NORTH, Direction.EAST}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_bottom_to_right_top.png"

            # Mirrored case (EAST+SOUTH → NORTH+WEST)
            elif input_dirs == {Direction.EAST, Direction.SOUTH} and output_dirs == {Direction.NORTH, Direction.WEST}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_bottom_to_right_top.png"
                vertical_mirror = True

            # Left-top to right-bottom (WEST+NORTH → SOUTH+EAST)
            elif input_dirs == {Direction.WEST, Direction.NORTH} and output_dirs == {Direction.SOUTH, Direction.EAST}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_top_to_bottom_right.png"

            # Mirrored case (EAST+NORTH → SOUTH+WEST)
            elif input_dirs == {Direction.EAST, Direction.NORTH} and output_dirs == {Direction.SOUTH, Direction.WEST}:
                sprite_path = "assets/sprites/conveyorbelts/crosssections/horizontal/left_top_to_bottom_right.png"
                vertical_mirror = True



        #for port in input_ports:
        #    if port.direction

        # example:
        #sprite_path = "assets/sprites/conveyor_belt_vertical_curve.png"
        if sprite_path == None:
            sprite_path = "assets/sprites/conveyorbelts/normal/horizontal.png"
        #horizontal_mirror = False
        #vertical_mirror = False
        
        belt.update_sprite(sprite_path, horizontal_mirror, vertical_mirror)

    
    @staticmethod
    def configure_neighbor_when_removing(neighbor: ConveyorBelt, direction, removed_machine, connection_system) -> None:
        """Update a specific neighboring belt when a block is removed."""

        # most important case: the removed machine is a conveyor belt
        if isinstance(removed_machine, ConveyorBelt):
            # remove the input/output of the neighbor, that is connected to the removed machine
            for port in neighbor.ports:
                rotated_direction = port.direction.rotate(-neighbor.rotation)

                if port.connected_port and port.connected_port.machine == removed_machine:
                    if port.port_type == "input":
                        neighbor.inputs.remove(rotated_direction)
                    elif port.port_type == "output":
                        neighbor.outputs.remove(rotated_direction)
                    break
            
        # update the inputs and outputs of the neighbor (maybe we have to add a new input/output)
        ConveyorBeltAutoConnector._update_io(neighbor, {})
        
        # update the ports and sprite of the neighbor
        ConveyorBeltAutoConnector._update_port_connections(neighbor, connection_system)
        ConveyorBeltAutoConnector.update_sprite(neighbor)


    @staticmethod
    def configure_neighbor_when_placing(neighbor: ConveyorBelt, direction, placed_machine, connection_system):
        """Update a specific neighboring belt when a block is placed."""
        # 1) remove unused inputs and outputs of the neighbor
        for port in neighbor.ports:
            if not port.connected_port:
                rotated_direction = port.direction.rotate(-neighbor.rotation)
                if port.port_type == "input":
                    neighbor.inputs.remove(rotated_direction)
                elif port.port_type == "output":
                    neighbor.outputs.remove(rotated_direction)

        # 2) update the inputs and outputs of the neighbor
        opposite_direction = direction.opposite()
        ConveyorBeltAutoConnector._update_io(neighbor, {opposite_direction: placed_machine})
        ConveyorBeltAutoConnector._update_port_connections(neighbor, connection_system)
        ConveyorBeltAutoConnector.update_sprite(neighbor)