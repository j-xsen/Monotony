from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode, LVector3f, LVecBase3f
from direct.gui.DirectGui import DGG

from objects.ui.panel import Panel

size = .45


class DetailRectangle(Panel):
    def __init__(self, player):
        Panel.__init__(self, "inventory",
                       frame_size=(size, -size * 2.75, size - .045, -size),
                       pos=(-0.1, 0, -.52))
        self.player = player

        button_scale = 0.4
        self.nav_log = DirectButton(geom=player.drawn_square,
                                    text="Log",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=player.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-1, 0, -.045), command=self.goto_log)
        self.nav_inv = DirectButton(geom=player.drawn_square,
                                    text="Inventory",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=player.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-.5, 0, -.045), command=self.goto_inventory)

        self.log = Log()
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

    def switch_inv_log(self, is_inv):
        color_active = (1, 1, 1, 1)
        color_disabled = (1, 1, 1, 0.5)
        self.nav_log["state"] = DGG.NORMAL if is_inv else DGG.DISABLED
        self.nav_log["text_fg"] = color_active if is_inv else color_disabled
        self.nav_log.setColor(color_active if is_inv else color_disabled)
        self.nav_inv["state"] = DGG.DISABLED if is_inv else DGG.NORMAL
        self.nav_inv["text_fg"] = color_disabled if is_inv else color_active
        self.nav_inv.setColor(color_disabled if is_inv else color_active)


class DetailRectanglePane:
    def __init__(self):
        self.frame = DirectFrame(frameColor=(1, 0, 0, 0),
                                 frameSize=(size - .2, -size * 2.75, size - .245, -size - .1),
                                 pos=(0, 0, -.37))

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()


class Inventory(DetailRectanglePane):
    def __init__(self):
        DetailRectanglePane.__init__(self)
        self.items = []
        self.font = loader.loadFont("Monotony-Regular.ttf")

    def add(self, message):
        new_item = InventoryItem(message.get_title(), self.font)
        new_item.reparentTo(self.frame)
        self.items.append(new_item)


class InventoryItem:
    def __init__(self, message, font):
        new_button = DirectButton(text=message, text_scale=0.07, text_pos=(0,-.02),
                                  pos=(-.5,0,.13), geom=loader.loadModel('art/drawn_square.egg')
                                  .find("**/drawn_square"), relief=None, text_fg=(1, 1, 1, 1),
                                  geom_scale=[1.5,1,.1], text_font=font)
        self.button = new_button
        self.message = message

    def reparentTo(self, parent):
        self.button.reparentTo(parent)


class Log(DetailRectanglePane):
    def __init__(self):
        DetailRectanglePane.__init__(self)
        self.items = []

    def add(self, entry):
        for e in self.items:
            e.move_down()
        entry.reparentTo(self.frame)
        self.items.append(entry)


class LogEntry:
    def __init__(self, text, font):
        self.label = DirectLabel(text=text,
                                 text_align=TextNode.ALeft,
                                 pos=(-1.22, 0, .14),
                                 scale=0.06,
                                 frameColor=(1, 1, 1, 0),
                                 text_font=font,
                                 text_fg=(1, 1, 1, 1))

    def move_down(self):
        self.label.setPos(self.label.getPos() + LVector3f(0, 0, -0.08))

    def reparentTo(self, frame):
        self.label.reparentTo(frame)
