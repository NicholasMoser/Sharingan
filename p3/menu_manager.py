import math

import p3.pad

class MenuManager:
    def __init__(self):
        self.selected_itachi = False

    def pick_itachi(self, state, pad):
        if self.selected_itachi:
            # Release buttons
            pad.release_button(p3.pad.Button.A)
        else:
            # Go to itachi and press A
            target_x = -23.5
            target_y = 11.5
            dx = target_x - state.players[2].cursor_x
            dy = target_y - state.players[2].cursor_y
            mag = math.sqrt(dx * dx + dy * dy)
            if mag < 0.3:
                pad.press_button(p3.pad.Button.A)
                self.selected_itachi = True
            else:
                pad.tilt_stick(p3.pad.Stick.MAIN, 0.5 * (dx / mag) + 0.5, 0.5 * (dy / mag) + 0.5)

    def press_a_lots(self, state, pad):
        if state.frame % 2 == 0:
            pad.press_button(p3.pad.Button.A)
        else:
            pad.release_button(p3.pad.Button.A)
