import cc_gui as ui
from pygame import draw
from pygame import gfxdraw as gfx


class TestWidget(ui.Widget):
    def __init__(self, x, y):
        super(TestWidget, self).__init__(x, y, 100, 100)

        # Red
        self.color = (255, 0, 0)

    def paint(self, s):
        # Background
        draw.rect(s, self.color, self.get_hitbox())

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

# Start the app #
app.launch()
