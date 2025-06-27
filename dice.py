import arcade
import os
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dice Test"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "background.png")
DICE_IMAGE_DIR = os.path.join(ASSETS_DIR, "dice")
DICE_IMAGES = [
    os.path.join(DICE_IMAGE_DIR, f"Spike Die {i+1} Holo.png") for i in range(6)
]

def roll_dice():
    """Return a tuple of two random dice rolls (1-6, 1-6)."""
    return random.randint(1, 6), random.randint(1, 6)

class DiceTestWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.background = arcade.load_texture(BACKGROUND_IMAGE) if os.path.exists(BACKGROUND_IMAGE) else None
        self.dice = [None, None]  # Start with no dice showing
        self.dice_size = 120
        self.roll_button_w = 220
        self.roll_button_h = 70
        self.roll_button_color = arcade.color.DARK_GREEN
        self.rolling = False
        self.roll_start_time = 0
        self.roll_duration = 1.2  # seconds
        self.roll_end_result = [1, 1]
        self.roll_intervals = [0.04, 0.04]  # ms between dice updates
        self.roll_next_update = [0, 0]
        self.dice_visible = False  # Track if dice are visible

    def on_draw(self):
        arcade.start_render()
        # Draw background
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)

        # Draw dice in the center if visible
        if self.dice_visible:
            center_x = self.width // 2
            center_y = self.height // 2
            offset = 80
            for i, die in enumerate(self.dice):
                if die is not None and 1 <= die <= 6:
                    dx = center_x + (i * 2 - 1) * offset
                    arcade.draw_texture_rectangle(
                        dx, center_y, self.dice_size, self.dice_size,
                        arcade.load_texture(DICE_IMAGES[die - 1])
                    )

            # --- Show "Doubles - Sabacc Shift" if both dice match and not rolling, but only after first roll ---
            if (
                not self.rolling
                and self.dice[0] is not None
                and self.dice[0] == self.dice[1]
                and hasattr(self, "has_rolled") and self.has_rolled
            ):
                msg = "Sabacc Shift"
                msg_w = 420
                msg_h = 70
                msg_x = self.width // 2
                msg_y = self.height // 2 + 120
                # Translucent background
                arcade.draw_rectangle_filled(
                    msg_x, msg_y, msg_w, msg_h, (30, 30, 30, 180)
                )
                arcade.draw_text(
                    msg,
                    msg_x - msg_w // 2 + 10, msg_y - 28,
                    arcade.color.GOLD,
                    38,
                    width=msg_w - 20,
                    align="center",
                    bold=True,
                    font_name="Arial"
                )

        # Draw roll button
        btn_x = self.width // 2
        btn_y = 100
        arcade.draw_rectangle_filled(btn_x, btn_y, self.roll_button_w, self.roll_button_h, self.roll_button_color)
        arcade.draw_text(
            "Roll Dice" if self.dice_visible else "Show Dice",
            btn_x - 70, btn_y - 20,
            arcade.color.WHITE, 32
        )

    def on_mouse_press(self, x, y, button, modifiers):
        btn_x = self.width // 2
        btn_y = 100
        if (
            btn_x - self.roll_button_w // 2 < x < btn_x + self.roll_button_w // 2 and
            btn_y - self.roll_button_h // 2 < y < btn_y + self.roll_button_h // 2
        ):
            if not self.dice_visible:
                # First press: show dice, but don't roll yet
                self.dice_visible = True
                self.dice = [1, 1]
                self.has_rolled = False
            elif not self.rolling:
                # Second press: roll dice
                self.start_roll_animation()

    def start_roll_animation(self):
        if self.rolling:
            return
        self.rolling = True
        self.roll_start_time = time.time()
        self.roll_duration = random.uniform(1.0, 1.7)
        self.roll_end_result = roll_dice()
        # Each die can have a slightly different stop time for realism
        self.roll_stop_times = [
            self.roll_start_time + self.roll_duration + random.uniform(0, 0.2),
            self.roll_start_time + self.roll_duration + random.uniform(0, 0.2)
        ]
        self.roll_intervals = [0.04, 0.04]
        self.roll_next_update = [self.roll_start_time, self.roll_start_time]
        self.has_rolled = True

    def on_update(self, delta_time):
        if self.rolling:
            now = time.time()
            for i in range(2):
                # Accelerate: increase interval as time passes
                elapsed = now - self.roll_start_time
                total = self.roll_stop_times[i] - self.roll_start_time
                # Ease out: interval grows as we approach stop time
                t = min(max(elapsed / total, 0), 1)
                self.roll_intervals[i] = 0.04 + t * 0.18 * random.uniform(0.9, 1.1)
                if now >= self.roll_stop_times[i]:
                    self.dice[i] = self.roll_end_result[i]
                elif now >= self.roll_next_update[i]:
                    self.dice[i] = random.randint(1, 6)
                    self.roll_next_update[i] = now + self.roll_intervals[i]
            if now >= max(self.roll_stop_times):
                self.rolling = False

def main():
    window = DiceTestWindow()
    arcade.run()

if __name__ == "__main__":
    main()