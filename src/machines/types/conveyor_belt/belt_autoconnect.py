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
                #neighbor_wants_to_input_here = rotated_direction.opposite() in rotated_neighbor_inputs
                # note: we cant do the same for THIS belt, because the inputs and outputs may not be set yet

                # avoid special cases where both belts want to output to each other
                if neighbor_wants_to_output_here and rotated_direction == Direction.EAST: # EAST is the default output direction (base image without rotation)
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

        # case 1: 1 input and 1 output
        if len(input_ports) == 1 and len(output_ports) == 1:
            input_port = input_ports[0]
            output_port = output_ports[0]

            """NORMAL BELTS"""

            # case 1.1: horizontal from left to right
            if input_port.direction == Direction.WEST and output_port.direction == Direction.EAST:
                
                # case 1.1.1: output is not connected, and input is is connected
                if not output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_end_1.png"
                # case 1.1.2: output is connected, and input is not
                if output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/2/horizontal_end_2.png"
                    horizontal_mirror = True
                # case 1.1.3: output is not connected, and input is not
                if not output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_1.png"
                # case 1.1.4: output is connected, and input is connected
                if output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_straight_1.png"
            
            # case 1.2: horizontal from right to left
            if input_port.direction == Direction.EAST and output_port.direction == Direction.WEST:
                
                vertical_mirror = True
                # case 1.2.1: output is not connected, and input is connected
                if not output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_end_1.png"
                # case 1.2.2: output is connected, and input is not
                if output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/2/horizontal_end_2.png"
                    horizontal_mirror = True
                # case 1.2.3: output is not connected, and input is not
                if not output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_1.png"
                # case 1.2.4: output is connected, and input is connected
                if output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_straight_1.png"
            
            # case 1.3: vertical from top to bottom
            if input_port.direction == Direction.NORTH and output_port.direction == Direction.SOUTH:
                
                # case 1.3.1: output is not connected, and input is connected
                if not output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_end_1.png"
                # case 1.3.2: output is connected, and input is not
                if output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/2/vertical_end_2.png"
                    horizontal_mirror = True
                # case 1.3.3: output is not connected, and input is not
                if not output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_1.png"
                # case 1.3.4: output is connected, and input is connected
                if output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_straight_1.png"
            
            # case 1.4: vertical from bottom to top
            if input_port.direction == Direction.SOUTH and output_port.direction == Direction.NORTH:
                
                vertical_mirror = True
                # case 1.4.1: output is not connected, and input is connected
                if not output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_end_1.png"
                # case 1.4.2: output is connected, and input is not
                if output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/2/vertical_end_2.png"
                    horizontal_mirror = True
                # case 1.4.3: output is not connected, and input is not
                if not output_port.connected_port and not input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_1.png"
                # case 1.4.4: output is connected, and input is connected
                if output_port.connected_port and input_port.connected_port:
                    sprite_path = "assets/sprites/conveyorbelts/vertical/1/vertical_straight_1.png"

            """CURVED BELTS"""
            
            # case 1.5: from left to bottom
            if input_port.direction == Direction.WEST and output_port.direction == Direction.SOUTH:
                # case 1.5.1: output is not connected, and input is connected AND case 1.5.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_left_bottom.png"
            
            # case 1.6: from left to top
            if input_port.direction == Direction.WEST and output_port.direction == Direction.NORTH:
                # case 1.6.1: output is not connected, and input is connected AND case 1.6.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_left_top.png"
            
            # case 1.7: from right to bottom
            if input_port.direction == Direction.EAST and output_port.direction == Direction.SOUTH:
                # case 1.7.1: output is not connected, and input is connected AND case 1.7.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_right_bottom.png"
            
             # case 1.8: from right to top
            if input_port.direction == Direction.EAST and output_port.direction == Direction.NORTH:
                # case 1.8.1: output is not connected, and input is connected AND case 1.8.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_right_top.png"
            


            # case 1.9: from bottom to left
            if input_port.direction == Direction.SOUTH and output_port.direction == Direction.WEST:
                # case 1.9.1: output is not connected, and input is connected AND case 1.9.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_bottom_left.png"
            
            # case 1.10: from top to left
            if input_port.direction == Direction.NORTH and output_port.direction == Direction.WEST:
                # case 1.10.1: output is not connected, and input is connected AND case 1.10.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_top_left.png"
            
            # case 1.11: from bottom to right
            if input_port.direction == Direction.SOUTH and output_port.direction == Direction.EAST:
                # case 1.11.1: output is not connected, and input is connected AND case 1.11.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_bottom_right.png"
            
             # case 1.12: from top to right
            if input_port.direction == Direction.NORTH and output_port.direction == Direction.EAST:
                # case 1.12.1: output is not connected, and input is connected AND case 1.12.2: output is connected, and input is connected
                if (not output_port.connected_port and input_port.connected_port) or (output_port.connected_port and input_port.connected_port):
                    sprite_path = "assets/sprites/conveyorbelts/curve/curve_top_right.png"
            


        #for port in input_ports:
        #    if port.direction

        # example:
        #sprite_path = "assets/sprites/conveyor_belt_vertical_curve.png"
        if sprite_path == None:
            sprite_path = "assets/sprites/conveyorbelts/horizontal/1/horizontal_1.png"
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