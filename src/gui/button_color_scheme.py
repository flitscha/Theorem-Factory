class ButtonColorScheme:
    """color scheme for Buttons"""
    
    def __init__(self, 
                 normal=(80, 80, 80),
                 hover=(120, 120, 120),
                 pressed=(60, 60, 60),
                 selected=(100, 100, 255),
                 selected_hover=(120, 120, 255),
                 border=(200, 200, 200),
                 text=(255, 255, 255)):
        self.normal = normal
        self.hover = hover
        self.pressed = pressed
        self.selected = selected
        self.selected_hover = selected_hover
        self.border = border
        self.text = text

# predefined color schemes
DEFAULT_COLORS = ButtonColorScheme()
GREEN_COLORS = ButtonColorScheme(
    normal=(80, 80, 80),
    hover=(120, 120, 120),
    pressed=(60, 60, 60),
    selected=(110, 220, 110),
    selected_hover=(120, 235, 120),
)
RED_COLORS = ButtonColorScheme(
    normal=(120, 60, 60),
    hover=(150, 80, 80),
    pressed=(90, 40, 40),
    selected=(180, 60, 60),
    selected_hover=(200, 80, 80)
)
BLUE_COLORS = ButtonColorScheme(
    normal=(60, 80, 120),
    hover=(80, 100, 150),
    pressed=(40, 60, 90),
    selected=(60, 100, 180),
    selected_hover=(80, 120, 200)
)
