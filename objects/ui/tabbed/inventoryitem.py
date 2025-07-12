from direct.gui.DirectButton import DirectButton

from objects.ui.uiconstants import UIConstants


class InventoryItem:
    def __init__(self, note, font, index):
        self.note = note
        self.button = self.create_inventory_button(note, font)

    def reparentTo(self, parent):
        self.button.reparentTo(parent)

    def click(self):
        # Button pressed, display message
        self.note.display()
        messenger.send("inv_disable")

    def move_down(self):
        cur_pos = self.button.get_pos()
        cur_pos.z -= 0.125
        self.button.set_fluid_pos(cur_pos)

    def create_inventory_button(self, note, font):
        return DirectButton(text=note.title,
                            text_scale=UIConstants.BTNS["INV"]["text_scale"],
                            text_pos=UIConstants.BTNS["INV"]["text_pos"],
                            pos=UIConstants.BTNS["INV"]["pos"],
                            geom=loader.loadModel('art/drawn_square.egg').find("**/drawn_square"), relief=None, text_fg=UIConstants.COLOR_ENABLE,
                            geom_scale=UIConstants.BTNS["INV"]["geom_scale"],
                            text_font=font,
                            command=self.click,
                            clickSound=base.loader.loadSfx("art/sounds/open.ogg"))


