import pygame
from game.game_state import GameState
from game.tools.placement_tool import PlacementTool
from game.tools.eraser_tool import EraserTool
from game.tools.empty_tool import EmptyTool
from core.utils import mouse_in_machine_selection_menu

# idea: game-class as input
class InputProcessor:
    def __init__(self, input_handler, placement_preview, machine_selection_bar, machine_manager, camera, game_state):
        self.input_handler = input_handler
        self.placement_preview = placement_preview
        self.machine_selection_bar = machine_selection_bar
        self.machine_manager = machine_manager
        self.camera = camera
        self.game_state = game_state

        # The camera is only dragged, if the right mouse button was pressed down OUTSIDE a menu
        self.camera_dragging = False

        # Tools
        self.placement_tool = PlacementTool(machine_manager, placement_preview, machine_selection_bar, game_state)
        self.eraser_tool = EraserTool(machine_manager, placement_preview, machine_selection_bar, game_state)
        self.empty_tool = EmptyTool(machine_manager, placement_preview, machine_selection_bar, game_state)
        self.current_tool = self.empty_tool

        # Shift-Handling
        self.shift_active = False
        self.prev_selected_id = None

    def process_input(self, screen, events, pause_menu):
        # Quit
        if self.input_handler.should_quit():
            return {"quit": True}

        self._pass_events_to_camera(events)

        # Pause-Handling
        if self.game_state.current_state == GameState.PAUSED and not pause_menu.is_open:
            self.game_state.resume_game()

        if self.input_handler.was_key_pressed(pygame.K_ESCAPE):
            if self.game_state.is_menu_open():
                self.game_state.close_menu()
            elif pause_menu.is_open and pause_menu.active_submenu is None:
                self.game_state.resume_game()
            elif not pause_menu.is_open:
                self.game_state.pause_game()
                pause_menu.open()

        if self.input_handler.was_key_pressed(pygame.K_e):
            if self.game_state.is_menu_open():
                self.game_state.close_menu()

        # pause menu, and machine menu
        if self.game_state.is_paused():
            return {}
        if self.game_state.is_menu_open():
            self.game_state.active_menu.handle_events(events)
            if self.game_state.active_menu.closed:
                self.game_state.close_menu()
            return {}

        # left mouse button: select tools / machines
        if self.input_handler.was_mouse_pressed(1):
            self._handle_left_mouse_button()

        # shift: temporary select delete-tool
        if self.input_handler.was_key_pressed(pygame.K_LSHIFT):
            self._handle_shift_down()
        if self.input_handler.was_key_released(pygame.K_LSHIFT):
            self._handle_shift_up()

        # q: switch to empty-tool
        if self.input_handler.was_key_pressed(pygame.K_q):
            self._handle_q_down()

        # pass events to current tool
        self.current_tool.handle_inputs(self.input_handler, screen)
        self.current_tool.update(self.input_handler)

        return {}

    
    def _pass_events_to_camera(self, events):
        if self.game_state.is_paused():
            return

        menu = self.game_state.active_menu
        if (not menu or not menu.is_mouse_inside_menu()) and not mouse_in_machine_selection_menu():
            self.camera.handle_mouse_wheel(zoom_dir=self.input_handler.mouse_wheel_dir)
            if "mouse_down_3" in self.input_handler.events_this_frame:
                self.camera_dragging = True
            
        elif "mouse_down_3" in self.input_handler.events_this_frame:
            self.camera_dragging = False

        if "mouse_up_3" in self.input_handler.events_this_frame:
            self.camera_dragging = False

        self.camera.handle_dragging(self.camera_dragging)
        self.camera.handle_wasd(keys=self.input_handler.keys_pressed)


    def _handle_left_mouse_button(self):
        # click in GUI-Bar -> change selected tool
        mouse_pos = pygame.mouse.get_pos()
        if mouse_in_machine_selection_menu(mouse_pos):
            selected = self.machine_selection_bar.handle_click(mouse_pos)

            # change tool + preview
            match selected:
                case None:
                    # dont reset the active preview
                    pass
                case "None": # tool to navigate, open machine menus, ...
                    self.placement_preview.active_preview = None
                    self.current_tool = self.empty_tool
                case "eraser":
                    self.placement_preview.active_preview = None
                    self.current_tool = self.eraser_tool
                case _:
                    self.placement_preview.start_preview(selected)
                    self.current_tool = self.placement_tool


    def _handle_shift_down(self):
        if not self.shift_active:
            self.shift_active = True
            self.prev_selected_id = self.machine_selection_bar.selected_machine_id
            self.machine_selection_bar.selected_machine_id = "eraser"
            self.placement_preview.active_preview = None
            self.current_tool = self.eraser_tool
    

    def _handle_shift_up(self):
        if self.shift_active:
            self.shift_active = False
            self.machine_selection_bar.selected_machine_id = self.prev_selected_id
            if self.prev_selected_id == "eraser":
                self.current_tool = self.eraser_tool
            elif self.prev_selected_id == "None":
                self.current_tool = self.empty_tool
            elif self.prev_selected_id:
                self.placement_preview.start_preview(self.prev_selected_id)
                self.current_tool = self.placement_tool
    

    def _handle_q_down(self):
        """
        select the machine, that is under the mouse.
        No machine under mouse -> empyt_tool
        Already in placement_tool -> empty tool
        """
        machine = self.machine_manager.get_machine_at_mouse()

        if machine is None:
            # no machine -> empty tool
            self.placement_preview.stop_preview()
            self.machine_selection_bar.set_tool("None")
            self.current_tool = self.empty_tool
            return


        machine_id = machine.data.id

        # if the same machine is already selected -> empty tool
        if self.machine_selection_bar.selected_machine_id != "None":
            self.placement_preview.stop_preview()
            self.machine_selection_bar.set_tool("None")
            self.current_tool = self.empty_tool
        elif machine_id != "hub":
            # select new machine, and adopt the rotation
            self.machine_selection_bar.set_tool(machine_id)
            self.placement_preview.start_preview(machine_id)
            self.placement_preview.set_rotation(machine.rotation)
            self.current_tool = self.placement_tool

