from direct.gui.DirectGui import DGG

from objects.ui.tabbed.inventoryitem import InventoryItem
from objects.ui.tabbed.tab import Tab
from objects.ui.uiconstants import UIConstants


class Inventory(Tab):
    def __init__(self):
        Tab.__init__(self)
        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.items = []
        self.accept("inv_disable", self.disable_all)
        self.accept("inv_enable", self.enable_all)
        self.accept("add_note", self.add_note)

    def add_note(self, note):
        for item in self.items:
            item.move_down()
        if note.title != "Welcome to Monotony!":
            receive_sound = base.loader.loadSfx("art/sounds/receive_note.ogg")
            receive_sound.setVolume(0.5)
            receive_sound.play()
        note.display()
        new_item = InventoryItem(note, self.font, len(self.items))
        new_item.reparentTo(self.frame)
        self.items.append(new_item)

    def disable_all(self):
        for item in self.items:
            item.button["state"] = DGG.DISABLED
            item.button.setColor(UIConstants.COLOR_DISABLE)
            item.button["text_fg"] = UIConstants.COLOR_DISABLE

    def enable_all(self):
        for item in self.items:
            item.button["state"] = DGG.NORMAL
            item.button.setColor(UIConstants.COLOR_ENABLE)
            item.button["text_fg"] = UIConstants.COLOR_ENABLE

    def destroy(self):
        self.ignore_all()