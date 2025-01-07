from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import DGG
from direct.gui.DirectLabel import DirectLabel
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode, LVector3f

from objects.ui.panel import Panel

size = .45


class DetailRectangle(Panel):
    def __init__(self, clock):
        Panel.__init__(self, "inventory",
                       frame_size=(size, -size * 2.75, size - .045, -size),
                       pos=(-0.1, 0, -.52))
        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.drawn_square = loader.loadModel('art/drawn_square.egg').find("**/drawn_square")

        button_scale = 0.4
        self.nav_log = DirectButton(geom=self.drawn_square,
                                    text="Log",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=self.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-1, 0, -.045), command=self.goto_log)
        self.nav_inv = DirectButton(geom=self.drawn_square,
                                    text="Inventory",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=self.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-.5, 0, -.045), command=self.goto_inventory)

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

    def switch_inv_log(self, is_inv):
        color_active = (1, 1, 1, 1)
        color_disabled = (1, 1, 1, 0.5)
        self.nav_log["state"] = DGG.NORMAL if is_inv else DGG.DISABLED
        self.nav_log["text_fg"] = color_active if is_inv else color_disabled
        self.nav_log.setColor(color_active if is_inv else color_disabled)
        self.nav_inv["state"] = DGG.DISABLED if is_inv else DGG.NORMAL
        self.nav_inv["text_fg"] = color_disabled if is_inv else color_active
        self.nav_inv.setColor(color_disabled if is_inv else color_active)


class DetailRectanglePane(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
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
        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.items = []
        self.accept("inv_disable", self.disable_all)
        self.accept("inv_enable", self.enable_all)
        self.accept("add_note", self.add_note)

    def add_note(self, note):
        new_item = InventoryItem(note, self.font, len(self.items))
        new_item.reparentTo(self.frame)
        self.items.append(new_item)

    def disable_all(self):
        for item in self.items:
            item.button["state"] = DGG.DISABLED
            item.button.setColor(.4, .4, .4, 1)
            item.button["text_fg"] = (.4, .4, .4, 1)

    def enable_all(self):
        for item in self.items:
            item.button["state"] = DGG.NORMAL
            item.button.setColor(1, 1, 1, 1)
            item.button["text_fg"] = (1, 1, 1, 1)

    def destroy(self):
        self.ignore_all()


class InventoryItem:
    def __init__(self, note, font, index):
        self.note = note
        self.button = DirectButton(text=note.title, text_scale=0.07, text_pos=(0, -.02),
                                  pos=(-.5, 0, .13), geom=loader.loadModel('art/drawn_square.egg')
                                  .find("**/drawn_square"), relief=None, text_fg=(1, 1, 1, 1),
                                  geom_scale=[1.5, 1, .1], text_font=font, command=self.click)

    def reparentTo(self, parent):
        self.button.reparentTo(parent)

    def click(self):
        # Button pressed, display message
        self.note.display()
        messenger.send("inv_disable")


class Log(DetailRectanglePane):
    def __init__(self, clock):
        DetailRectanglePane.__init__(self)
        self.items = []
        self.clock = clock

        self.accept("add_log", self.add)

    def add(self, text):
        new_entry = LogEntry(f"[{self.clock.time}] {text}")
        for e in self.items:
            e.move_down()
        new_entry.reparentTo(self.frame)
        self.items.append(new_entry)


class LogEntry:
    def __init__(self, text):
        self.label = DirectLabel(text=text,
                                 text_align=TextNode.ALeft,
                                 pos=(-1.22, 0, .14),
                                 scale=0.06,
                                 frameColor=(1, 1, 1, 0),
                                 text_font=loader.loadFont("Monotony-Regular.ttf"),
                                 text_fg=(1, 1, 1, 1))

    def move_down(self):
        self.label.setPos(self.label.getPos() + LVector3f(0, 0, -0.08))

    def reparentTo(self, frame):
        self.label.reparentTo(frame)
