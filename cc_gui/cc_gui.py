import pygame as pg


class App:
    """
        The App handles window, widgets and events.
    """
    def __init__(self, width, height, title="Hello World", icon_path=""):
        # Pygame init
        pg.init()

        # Window init
        self.window = Window(width, height, title, icon_path)

        # Children widgets init
        # a list of widgets
        self.children = []

        # The most important widget, the widget targeted by the user
        self.focused_child = None

        # The last widget which has been hovered by the mouse
        self.last_widget_mouse_hover = None

    ################ Methods ################
    def launch(self):
        """ Launch the app, open the window and start the event management """
        # Open the window
        self.window.open()

        # Paint for the first time the widgets
        self.paint()

        # If False, we must leave the main loop and exit
        running = True
        while running:
            # Event management
            for event in pg.event.get():
                ######## Life Cycle ########
                if event.type == pg.QUIT:
                    # For children
                    self.destroy()

                    # Pygame exit
                    pg.quit()

                    # Loop exit
                    running = False
                    break

                ######## Mouse ########
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Left click first
                    if pg.mouse.get_pressed()[0]:
                        self.raw_mouse_event(self._send_mouse_click)

                    # Right click if not left click
                    elif pg.mouse.get_pressed()[2]:
                        self.raw_mouse_event(self._send_mouse_right_click)

                elif event.type == pg.MOUSEBUTTONUP:
                    # The mouse_release event is dispatched by the last clicked (focused) widget
                    if self.focused_child is not None:
                        self.focused_child.mouse_release(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

                elif event.type == pg.MOUSEMOTION:
                    self._send_mouse_motion(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

                ######## Keyboard ########
                elif event.type == pg.KEYDOWN:
                    if self.focused_child is not None:
                        self.focused_child.key_down(event.key)

                elif event.type == pg.KEYUP:
                    if self.focused_child is not None:
                        self.focused_child.key_up(event.key)

    def add_widget(self, widget):
        """
            Add a child widget
        - widget, Widget : The child to add to children widgets
        """
        widget.parent = self
        self.children.append(widget)

    ################ Events ################
    ######## Life Cycle ########
    def paint(self):
        """ Paint children widgets """
        # Draw children
        for child in self.children:
            child.paint(self.window.window_handle)

        # Update display
        pg.display.update()

    def destroy(self):
        """ Free or save memory for children """
        for child in self.children:
            child.destroy()

    ######## Mouse ########
    def raw_mouse_event(self, event):
        """
            mouse_event with mouse coordinates 
        - event, function(widget, x, y) : The function which is called when a widget is clicked
        """
        self.mouse_event(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], event)

    def mouse_event(self, x, y, event):
        """
            Dispatch a mouse event for targeted child widget
        - x & y : Position of the mouse event
        - event, function(widget, x, y) : The function which is called when a widget is clicked
        """
        # We search the target widget
        target = self.widget_pointed(x, y)

        # No target, we can't dispatch the event
        if target is None:
            return

        # Event dispatcher
        event(target, x, y)

    ######## Keyboard ########

    ######## Intern ########
    def _send_mouse_click(self, widget, x, y):
        """ When we must send MOUSEBUTTONDOWN to the widget in the event loop """
        # Focus
        self.focus_child(widget)

        # Event dispatcher
        widget.mouse_click(x, y)

    def _send_mouse_right_click(self, widget, x, y):
        """ When we must send MOUSEBUTTONDOWN to the widget in the event loop """
        # Focus
        self.focus_child(widget)

        # Event dispatcher
        widget.mouse_right_click(x, y)

    def _send_mouse_motion(self, x, y):
        """
            To send all the events relative to mouse motion:
        - mouse_move
        - mouse_enter
        - mouse_leave
        """
        # We search the target widget
        target = self.widget_pointed(x, y)

        # No target, we can't dispatch the event
        if target is None:
            # The mouse leaves the old widget if it covered a widget
            if self.last_widget_mouse_hover is not None:
                # We can send the mouse_enter event
                self.last_widget_mouse_hover.mouse_leave(x, y)

                # The mouse cover no widgets so it's None
                self.last_widget_mouse_hover = None
            return

        # The mouse covers a new widget
        if self.last_widget_mouse_hover != target:
            # We can send the mouse_enter event if the mouse was onto another widget
            if self.last_widget_mouse_hover is not None:
                self.last_widget_mouse_hover.mouse_leave(x, y)

            # mouse_enter event dispatcher
            target.mouse_enter(x, y)

            # Last widget with mouse onto update
            self.last_widget_mouse_hover = target

        # Dispatch the mouse_move event after
        target.mouse_move(x, y)

    ################ Methods ################
    def send_repaint(self, widget):
        """ Call paint() for a child widget """
        # Draw children
        widget.paint(self.window.window_handle)

        # Update display just in the widget's hitbox
        pg.display.update(widget.get_hitbox())

    def focus_child(self, widget):
        """ Focus the child and distract the old child """ 
        # Distract
        if self.focused_child is not None:
            self.focused_child.distract()

        # Focus
        self.focused_child = widget
        self.focused_child.focus()

    ################ Queries ################
    def widget_pointed(self, x, y):
        """ Returns the widget where the point is (or None if the point is not in a widget) """
        for child in self.children:
            # We test if the point is in the widget's hitbox
            if x >= child.x and x <= child.x + child.width and \
                y >= child.y and y <= child.y + child.height:
                return child

        # The point is outside of any widgets
        return None


class Window:
    """
        Functions to monitor a window.
    !!! This class must be used with App to handle events.
    """
    def __init__(self, width, height, title, icon_path):
        self.width = width
        self.height = height
        self.title = title
        self.icon_path = icon_path

    def open(self):
        """ Open the window """
        # Size
        self.window_handle = pg.display.set_mode((self.width, self.height))
        
        # Title
        pg.display.set_caption(self.title)
        
        # Icon
        if self.icon_path != "":
            pg.display.set_icon(pg.image.load(self.icon_path).convert_alpha())


class Widget:
    """ A GUI component. """

    def __init__(self, x, y, width, height, parent=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.parent = parent
        
        self.focused = False

    ################ Getters ################
    def get_hitbox(self):
        """ Returns the tuple (x, y, width, height) """
        return (self.x, self.y, self.width, self.height)


    ################ Events ################
    ######## Life Cycle ########
    def paint(self, surf):
        """ Paint the widget on the surface """
        pass

    def destroy(self):
        """ Free memory """
        pass

    ######## Mouse ########
    def mouse_click(self, x, y):
        """ When a (left) click is detected in the hitbox """
        pass

    def mouse_release(self, x, y):
        """ When the user stops to click (called even if the mouse is outside the hitbox) """
        pass

    def mouse_right_click(self, x, y):
        """ When a right click is detected in the hitbox """
        pass

    def mouse_move(self, x, y):
        """ When the mouse moves inside the hitbox """
        pass

    def mouse_enter(self, x, y):
        """ When the mouse enters the hitbox """
        pass

    def mouse_leave(self, x, y):
        """ When the mouse leaves the hitbox """
        pass

    ######## Keyboard ########
    def key_down(self, key):
        """ When the widget is focused and when a key becomes pressed """
        pass

    def key_up(self, key):
        """ When the widget is focused and when a key becomes released """
        pass

    ######## Focus ########
    def focus(self):
        """ When the user focus on this widget """
        self.focused = True

    def distract(self):
        """ When the user stops to focus on this widget """
        self.focused = False
        self.repaint()

    ################ Methods ################
    def repaint(self):
        """ Repaint the widget just within the hitbox """
        self.parent.send_repaint(self)
