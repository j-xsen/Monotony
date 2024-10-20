from objects.player.ui.panel import Panel


class Inventory(Panel):
    def __init__(self):
        size = .45
        Panel.__init__(self, "inventory",
                       frame_size=(size, -size*2.75, size, -size),
                       pos=(-0.1, 0, -.52))
