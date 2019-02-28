import cc_gui as ui

import pygame as pg
from pygame import draw
from pygame import gfxdraw as gfx


class TestWidget(ui.Widget):
    """
            Just a simple custom widget to test some things...
        Controls:
    - Click : the color becomes blue
    - Mouse Hover : the color becomes light red
    - Right Click : the color becomes white
    - Focus : we see a green overlay
    - Space (when focused) : the color becomes magenta
    """

    def __init__(self, x, y):
        super(TestWidget, self).__init__(x, y, 100, 100)

        self.mouse_on = False

        # Red
        self.color = (255, 0, 0)

    def paint(self, s):
        # Background
        draw.rect(s, (255, 100, 100) if self.mouse_on and self.color == (255, 0, 0) else self.color, self.get_hitbox())

        # Overlay if focused
        if self.focused:
            gfx.rectangle(s, self.get_hitbox(), (0, 255, 0))


    def mouse_click(self, x, y):
        # Blue
        self.color = (0, 0, 255)

        # We must repaint the widget (don't call directly paint)
        self.repaint()

    def mouse_release(self, x, y):
        # Red
        self.color = (255, 0, 0)

        # We must repaint the widget (don't call directly paint)
        self.repaint()

    def mouse_right_click(self, x, y):
        # White
        self.color = (255, 255, 255)

        # We must repaint the widget (don't call directly paint)
        self.repaint()

    def mouse_enter(self, x, y):
        self.mouse_on = True
        self.repaint()

    def mouse_leave(self, x, y):
        self.mouse_on = False
        self.repaint()

    def key_down(self, k):
        if k == pg.K_SPACE:
            # Magenta
            self.color = (255, 0, 255)
 
        self.repaint()

    def key_up(self, k):
        if k == pg.K_SPACE:
            # Red
            self.color = (255, 0, 0)

        self.repaint()



# Create the app #
# 400px for width
# 600px for height
# The title of the window is "My App"
# We set also the icon with the image's path
app = ui.App(400, 600, "My App", "res/img/icon.bmp")

# Add some widgets #
# Custom widget
app.add_widget(TestWidget(10, 10))
app.add_widget(TestWidget(120, 10))
app.add_widget(TestWidget(220, 10))

# Start the app #
app.launch()
