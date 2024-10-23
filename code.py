from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB as _RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers as _Layers
from kmk.modules.macros import Macros
from kmk.modules.macros import Press, Release, Tap


import board

keyboard = KMKKeyboard()

# Define the row and column pins based on your setup
keyboard.row_pins = (board.GP3, board.GP4, board.GP5)  # Rows are on GP0, GP1, GP2
keyboard.col_pins = (board.GP0, board.GP1, board.GP2)  # Columns are on GP3, GP4, GP5

# Set the diode orientation to ROWS
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Define the custom coordinate mapping
keyboard.coord_mapping = [
    0, 1, 2,  # Mapping physical keys to logical positions 000, 003, 006
    3, 4, 5,  # Mapping physical keys to logical positions 001, 004, 007
    6, 7, 8,  # Mapping physical keys to logical positions 002, 005, 008
]

keyboard.modules.append(MediaKeys())

class RGB(_RGB):
    def __init__(self, layer_indication: bool = False, pixels_order: list = None, breathe_order: list = None, **kwargs):
        super().__init__(**kwargs)
        self.layer_indication = layer_indication
        self.pixels_order = pixels_order if pixels_order is not None else range(self.num_pixels)
        self.breathe_order = breathe_order if breathe_order is not None else self.pixels_order

    def indicate_layer(self):
        actual_layer = keyboard.active_layers[0]

        # Define hue values for each layer
        layer_hues = {
            1: 85,    # Green for layer 1
            2: 100,
            3: 115,
            4: 130,
            5: 145,
            6: 160,
            7: 175,
            8: 190,
            9: 205,
            10: 220,
            11: 235,
            12: 0,    # Red for layer 12
        }

        # Set all pixels to black initially (off)
        for i in range(self.num_pixels):
            self.set_hsv(0, 0, 0, i)  # Turn off all pixels

        # For layer 0, all pixels are off
        if actual_layer == 0:
            return

        # For other layers, set all pixels to the hue of the current layer
        if actual_layer in layer_hues:
            hue = layer_hues[actual_layer]
            for i in range(self.num_pixels):
                self.set_hsv(hue, self.sat, self.val, i)  # Light up all pixels with the corresponding hue

    def show(self):
        if self.layer_indication:
            self.indicate_layer()

        for pixels in self.pixels:
            pixels.show()

    def effect_static(self):
        super().effect_static()
        if self.layer_indication:
            self.animation_mode = AnimationModes.BREATHING

    def effect_breathe(self):
        self.increase_hue(self._step)
        for n, i in enumerate(self.breathe_order):
            self.set_hsv(0, 0, 0, i)

rgb = RGB(
    pixel_pin=board.GP28,
    num_pixels= 12,
    layer_indication=True,
    pixels_order=[1, 2, 3, 9, 10, 11, 7, 8, 9, 4, 5, 6],
    val_default=255,
    val_limit=255,
)
keyboard.extensions.append(rgb)

# Layers
class Layers(_Layers):
    def __init__(self, combo_layers=None):
        super().__init__(combo_layers)

    def _to_pressed(self, key, *args, **kwargs):
        """
        Activates layer and deactivates all other layers EXCEPT LAYER 0
        """
        self._active_combo = None
        keyboard.active_layers.clear()
        self.activate_layer(keyboard, 0)
        if not key.layer == 0:
            self.activate_layer(keyboard, key.layer)


layers = Layers()
keyboard.modules.append(layers)

# Macros
macros = Macros()
keyboard.modules.append(macros)

# First NeoPixel strip for RGB keys
rgb_keys = RGB(
    pixel_pin=board.GP29,  # Pin where the NeoPixel strip is connected
    num_pixels=9,          # Number of LEDs in the strip
    val_limit=255,         # Brightness limit (255 is full brightness)
    hue_default=0,         # Default hue (can be changed later)
    sat_default=255,       # Default saturation (can be changed later)
    val_default=128,       # Default brightness (can be changed later)
    animation_mode=AnimationModes.STATIC,  # Swirl animation
    animation_speed=1,
    knight_effect_length=1,
    refresh_rate=60,
)

keyboard.extensions.append(rgb_keys)

# Layer macros
def prev_layer(*_args):
    if len(keyboard.active_layers) == 1 and not keyboard.active_layers[0] == 0:
        prev = keyboard.active_layers[0] - 1
        keyboard.active_layers.clear()
        layers.activate_layer(keyboard, prev)
    else:
        layers.deactivate_layer(keyboard, keyboard.active_layers[0])


PREV = KC.MACRO(prev_layer)


def next_layer(*_args):
    print("true")
    if keyboard.active_layers[0] + 1 < len(keyboard.keymap):
        nxt = keyboard.active_layers[0] + 1
        layers.activate_layer(keyboard, nxt)


NEXT = KC.MACRO(next_layer)

SAVE = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.S),
    Release(KC.LCTL)
)

COPY = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.C),
    Release(KC.LCTL)
)

CUT = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.X),
    Release(KC.LCTL)
)

PASTE = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.V),
    Release(KC.LCTL)
)


# Define the keymap with layers
keyboard.keymap = [
    # Layer 0
    [
        PREV, NEXT, KC.LCMD,  # Prev Layer, Next Layer, Left Win Key
        KC.BRID, KC.MPLY, KC.BRIU,  # Brightness Down, Play/Pause, Brightness Up
        KC.MPRV, KC.MSTP, KC.MNXT,  # Previous Track, Stop, Next Track
    ],
    # Layer 1
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        SAVE, COPY, CUT,    # Function Key F15, Function Key F16, Function Key F17
        PASTE, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 2
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 3
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 4
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 5
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 6
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 7
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 8
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 9
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 10
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 11
    [
        KC.TRNS, KC.TRNS, KC.F14,  # Transparent (no action), Transparent (no action), Function Key F14
        KC.F15, KC.F16, KC.F17,    # Function Key F15, Function Key F16, Function Key F17
        KC.F18, KC.F19, KC.F20,    # Function Key F18, Function Key F19, Function Key F20
    ],
    # Layer 12
    [
        KC.TRNS, KC.TRNS, KC.RGB_MODE_SWIRL,  # Transparent (no action), Transparent (no action), RGB Mode Swirl
        KC.RGB_MODE_PLAIN, KC.RGB_MODE_RAINBOW, KC.RGB_MODE_KNIGHT,  # RGB Mode Rainbow, RGB Mode Breathe Rainbow, RGB Mode Knight
        KC.RGB_MODE_BREATHE, KC.RGB_HUD, KC.RGB_HUI,  # RGB Mode Breathe, Decrease HUE, Increase HUE
    ],
]

# Add EncoderHandler for Rotary Encoder support
encoder_handler = EncoderHandler()
encoder_handler.pins = (
    (board.GP7, board.GP8, board.GP6),  # CLK, DT, and SW (button) pins
)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.VOLD, KC.VOLU, KC.MUTE),),  # Rotate left: Volume Down, Rotate right: Volume Up, Press: Mute
    ((KC.RGB_AND, KC.RGB_ANI, KC.RGB_TOG),),  # Rotate left: RGB Animation Speed Down, Rotate right: RGB Animation Speed Up, Press: RGB TOGGLE
]
keyboard.modules.append(encoder_handler)

if __name__ == '__main__':
    keyboard.go()
