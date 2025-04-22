from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG

from objects.clock import Clock
from objects.ui.panel import Panel
from objects.ui.tabbed.Inventory import Inventory
from objects.ui.tabbed.Log import Log

size = .45
class TabContainer(Panel):
    def __init__(self, clock: Clock):
        Panel.__init__(self, "inventory",
                       frame_size=(size, -size * 2.75, size - .045, -size),
                       pos=(-0.1, 0, -.52))
        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.drawn_square = loader.loadModel('art/drawn_square.egg').find("**/drawn_square")

        button_scale = 0.4
        tab_change = base.loader.loadSfx("art/sounds/tab_change.ogg")
        tab_change.setVolume(0.5)
        self.nav_log = DirectButton(geom=self.drawn_square,
                                    text="Log",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=self.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-1, 0, -.045), command=self.goto_log,
                                    clickSound=tab_change)
        self.nav_inv = DirectButton(geom=self.drawn_square,
                                    text="Inventory",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=self.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-.5, 0, -.045), command=self.goto_inventory,
                                    clickSound=tab_change)

        self.log = Log(clock)
        self.inventory = Inventory()
        self.inventory.hide()
        self.switch_inv_log(False)

    def goto_inventory(self):
        self.log.hide()
        self.inventory.show()
        self.switch_inv_log(True)

    def goto_log(self):
        self.inventory.hide()
        self.log.show()
        self.switch_inv_log(False)

    def switch_inv_log(self, is_inv: bool):
        color_active = (1, 1, 1, 1)
        color_disabled = (1, 1, 1, 0.5)
        self.nav_log["state"] = DGG.NORMAL if is_inv else DGG.DISABLED
        self.nav_log["text_fg"] = color_active if is_inv else color_disabled
        self.nav_log.setColor(color_active if is_inv else color_disabled)
        self.nav_inv["state"] = DGG.DISABLED if is_inv else DGG.NORMAL
        self.nav_inv["text_fg"] = color_disabled if is_inv else color_active
        self.nav_inv.setColor(color_disabled if is_inv else color_active)