from direct.gui.DirectButton import DirectButton

from objects.ui.panel import Panel


class Inventory(Panel):
    def __init__(self, player):
        size = .45
        Panel.__init__(self, "inventory",
                       frame_size=(size, -size*2.75, size-.045, -size),
                       pos=(-0.1, 0, -.52))
        self.player = player

        # button_size = 0.08
        # self.nav_inv = Panel("navinv",
        #                      frame_size=(button_size, -button_size*7, button_size, -button_size),
        #                      pos=(-1, 0, -.1))

        button_scale = 0.4
        self.nav_log = DirectButton(geom=player.drawn_square,
                                    text="Log",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=player.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale*0.35),
                                    pos=(-1, 0, -.045))
        self.nav_inv = DirectButton(geom=player.drawn_square,
                                    text="Inventory",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=player.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale*0.35),
                                    pos=(-.5, 0, -.045))
