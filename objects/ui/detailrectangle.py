from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode, LVector3f

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
                                    pos=(-1, 0, -.045))
        self.nav_inv = DirectButton(geom=player.drawn_square,
                                    text="Inventory",
                                    text_fg=(1, 1, 1, 1),
                                    text_pos=(0, -.03, 1),
                                    text_font=player.font, text_scale=0.06,
                                    relief=None,
                                    geom_scale=(button_scale, 1, button_scale * 0.35),
                                    pos=(-.5, 0, -.045))

        self.log = Log(player)


class Log:
    def __init__(self, player):
        self.player = player
        self.frame = DirectFrame(frameColor=(1, 0, 0, 0),
                                 frameSize=(size - .2, -size * 2.75, size - .245, -size - .1),
                                 pos=(0, 0, -.37))
        self.entries = []

    def add(self, entry):
        for e in self.entries:
            e.move_down()
        self.entries.append(entry)


class LogEntry:
    def __init__(self, log, text):
        self.label = DirectLabel(parent=log.frame,
                                 text=f"[{log.player.clock.time}] {text}",
                                 text_align=TextNode.ALeft,
                                 pos=(-1.22, 0, .14),
                                 scale=0.06,
                                 frameColor=(1, 1, 1, 0),
                                 text_font=log.player.font,
                                 text_fg=(1, 1, 1, 1))

    def move_down(self):
        self.label.setPos(self.label.getPos() + LVector3f(0, 0, -0.08))
