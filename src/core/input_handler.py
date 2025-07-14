import pygame

class InputHandler:
    def __init__(self):
        # Continuous states (can be checked anytime)
        self.mouse_wheel_dir = 0
        self.is_dragging = False
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        
        # Event flags (reset each frame)
        self.events_this_frame = {}
        
    def update(self, events):
        """Process all pygame events and update input state"""
        self.mouse_wheel_dir = 0  # Reset each frame
        self.events_this_frame = {}  # Clear events from last frame
        
        # Update continuous mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.events_this_frame['quit'] = True
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.events_this_frame[f'key_down_{event.key}'] = True
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                self.events_this_frame[f'key_up_{event.key}'] = True
                    
            elif event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_dir = event.y
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.events_this_frame[f'mouse_down_{event.button}'] = True
                self.events_this_frame[f'mouse_down_{event.button}_pos'] = event.pos
                
                if event.button == 3:  # Right mouse - start dragging
                    self.is_dragging = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.events_this_frame[f'mouse_up_{event.button}'] = True
                
                if event.button == 3:  # Right mouse - stop dragging
                    self.is_dragging = False
                    
    def was_key_pressed(self, key):
        """Check if key was pressed this frame (flank detection)"""
        return self.events_this_frame.get(f'key_down_{key}', False)
        
    def is_key_held(self, key):
        """Check if key is currently held down (continuous)"""
        return key in self.keys_pressed
        
    def was_mouse_pressed(self, button):
        """Check if mouse button was pressed this frame (flank detection)"""
        return self.events_this_frame.get(f'mouse_down_{button}', False)
        
    def get_mouse_press_pos(self, button):
        """Get position where mouse button was pressed this frame"""
        return self.events_this_frame.get(f'mouse_down_{button}_pos')
        
    def should_quit(self):
        """Check if quit was requested this frame"""
        return self.events_this_frame.get('quit', False)