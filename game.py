import arcade
import os

# Initial window size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Sabacc - Resizable Background"

# Path to assets
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "background.png")
CARD_IMAGE = os.path.join(ASSETS_DIR, "cards", "+1 Circle.png")
CARD_BACK_IMAGE = os.path.join(ASSETS_DIR, "cards", "Back.png")
SYLOP_IMAGE = os.path.join(ASSETS_DIR, "cards", "0 Sylop.png")

CARD_SCALE = 0.33  # Try 0.33 for about 1/3 smaller


def overlap_area(sprite1, sprite2):
    # Calculate the overlap area between two sprites (axis-aligned bounding boxes)
    left = max(sprite1.left, sprite2.left)
    right = min(sprite1.right, sprite2.right)
    bottom = max(sprite1.bottom, sprite2.bottom)
    top = min(sprite1.top, sprite2.top)
    if right > left and top > bottom:
        return (right - left) * (top - bottom)
    return 0


class SabaccGame(arcade.Window):
    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            resizable=True
        )
        self.set_min_size(600, 400)
        self.set_max_size(1920, 1080)
        self.background_sprite = None
        self.bg_texture = None

        # Card size options
        self.card_scales = [0.2, 0.33, 0.5]  # Small, Medium, Large
        self.card_scale_names = ["Small", "Medium", "Large"]
        self.current_scale_index = 1  # Start at Medium

        # Card variables
        self.movable_card = None
        self.movable_card_image = CARD_IMAGE
        self.movable_card_face_up = True

        self.draw_pile_card = None
        self.draw_pile_image = SYLOP_IMAGE

        self.held_card = None
        self.held_card_offset_x = 0
        self.held_card_offset_y = 0

        self.draw_pile_highlight = False

    def setup(self):
        # Load background as a sprite
        self.background_sprite = arcade.Sprite(BACKGROUND_IMAGE)
        self.bg_texture = self.background_sprite.texture
        self._resize_background(self.width, self.height)

        # Movable card (starts face up, center)
        scale = self.card_scales[self.current_scale_index]
        self.movable_card = arcade.Sprite(self.movable_card_image)
        self.movable_card.scale = scale
        self.movable_card.center_x = self.width // 2
        self.movable_card.center_y = self.height // 2
        self.movable_card_face_up = True
        self.movable_card.texture = arcade.load_texture(self.movable_card_image)

        # Draw pile card (fixed, Sylop, face down, bottom center)
        self.draw_pile_card = arcade.Sprite(self.draw_pile_image)
        self.draw_pile_card.scale = scale
        self._position_draw_pile()
        self.draw_pile_card.texture = arcade.load_texture(CARD_BACK_IMAGE)

        self.draw_pile_highlight = False

    def update_card_scales(self):
        scale = self.card_scales[self.current_scale_index]
        self.movable_card.scale = scale
        self.draw_pile_card.scale = scale
        self._position_draw_pile()

    def _resize_background(self, width, height):
        scale_x = width / self.bg_texture.width
        scale_y = height / self.bg_texture.height
        scale = max(scale_x, scale_y)
        self.background_sprite.scale = scale
        self.background_sprite.center_x = width // 2
        self.background_sprite.center_y = height // 2
        self._position_draw_pile()

    def _position_draw_pile(self):
        if self.draw_pile_card:
            self.draw_pile_card.center_x = self.width // 2
            self.draw_pile_card.center_y = 60 + self.draw_pile_card.height // 2

    def on_draw(self):
        arcade.start_render()
        if self.background_sprite:
            self.background_sprite.draw()
        # Draw highlight if needed
        if self.draw_pile_highlight and self.draw_pile_card:
            arcade.draw_rectangle_outline(
                self.draw_pile_card.center_x,
                self.draw_pile_card.center_y,
                self.draw_pile_card.width + 10,
                self.draw_pile_card.height + 10,
                arcade.color.YELLOW,
                border_width=4
            )
        if self.draw_pile_card:
            self.draw_pile_card.draw()
        if self.movable_card:
            self.movable_card.draw()
        arcade.draw_text(f"{self.width} x {self.height}", 20, 20, arcade.color.WHITE, 24)
        # Show current card size
        arcade.draw_text(
            f"Card size: {self.card_scale_names[self.current_scale_index]} (press I to change)",
            20, 50, arcade.color.YELLOW, 18
        )

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if self.background_sprite:
            self._resize_background(width, height)

    def on_mouse_press(self, x, y, button, modifiers):
        # Only allow dragging the movable card
        if self.movable_card and self.movable_card.collides_with_point((x, y)):
            self.held_card = self.movable_card
            self.held_card_offset_x = self.movable_card.center_x - x
            self.held_card_offset_y = self.movable_card.center_y - y

    def on_mouse_release(self, x, y, button, modifiers):
        if self.held_card:
            # Check for >50% overlap with draw pile
            if self.draw_pile_card:
                overlap = overlap_area(self.movable_card, self.draw_pile_card)
                movable_area = self.movable_card.width * self.movable_card.height
                if overlap > 0.5 * movable_area:
                    # Swap image paths
                    self.movable_card_image, self.draw_pile_image = self.draw_pile_image, self.movable_card_image

                    # Movable card always face up after swap
                    self.movable_card.texture = arcade.load_texture(self.movable_card_image)
                    self.movable_card_face_up = True

                    # Draw pile always face down after swap
                    self.draw_pile_card.texture = arcade.load_texture(CARD_BACK_IMAGE)

                    # Snap movable card just above the draw pile (no overlap)
                    self.movable_card.center_x = self.draw_pile_card.center_x
                    self.movable_card.center_y = (
                        self.draw_pile_card.center_y
                        + (self.draw_pile_card.height + self.movable_card.height) // 2
                        + 10
                    )

            self.held_card = None
            self.draw_pile_highlight = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.held_card:
            self.held_card.center_x = x + self.held_card_offset_x
            self.held_card.center_y = y + self.held_card_offset_y
            # Highlight draw pile if >50% overlap
            if self.draw_pile_card:
                overlap = overlap_area(self.movable_card, self.draw_pile_card)
                movable_area = self.movable_card.width * self.movable_card.height
                self.draw_pile_highlight = overlap > 0.5 * movable_area
            else:
                self.draw_pile_highlight = False

    def on_mouse_motion(self, x, y, dx, dy):
        # Remove highlight if not dragging
        if not self.held_card:
            self.draw_pile_highlight = False

    def on_key_press(self, symbol, modifiers):
        # Flip the movable card with spacebar (can always flip)
        if symbol == arcade.key.SPACE and self.movable_card:
            if self.movable_card_face_up:
                self.movable_card.texture = arcade.load_texture(CARD_BACK_IMAGE)
                self.movable_card_face_up = False
            else:
                self.movable_card.texture = arcade.load_texture(self.movable_card_image)
                self.movable_card_face_up = True
        elif symbol == arcade.key.I:
            self.current_scale_index = (self.current_scale_index + 1) % len(self.card_scales)
            self.update_card_scales()


def main():
    game = SabaccGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
