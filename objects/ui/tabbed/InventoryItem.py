from direct.gui.DirectButton import DirectButton


class InventoryItem:
    def __init__(self, note, font, index):
        self.note = note
        self.button = DirectButton(text=note.title, text_scale=0.07, text_pos=(0, -.02),
                                  pos=(-.5, 0, .13), geom=loader.loadModel('art/drawn_square.egg')
                                  .find("**/drawn_square"), relief=None, text_fg=(1, 1, 1, 1),
                                  geom_scale=[1.5, 1, .1], text_font=font, command=self.click,
                                   clickSound=base.loader.loadSfx("art/sounds/open.ogg"))

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