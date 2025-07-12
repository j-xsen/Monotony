from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode, LVector3f

from objects.ui.UIConstants import UIConstants


class LogEntry:
    def __init__(self, text: str):
        self.label = DirectLabel(text=text,
                                 text_align=TextNode.ALeft,
                                 pos=(-1.22, 0, .14),
                                 scale=0.06,
                                 frameColor=(1, 1, 1, 0),
                                 text_font=loader.loadFont("Monotony-Regular.ttf"),
                                 text_fg=UIConstants.COLOR_ENABLE)

    def move_down(self):
        self.label.setPos(self.label.getPos() + LVector3f(0, 0, -0.08))

    def reparentTo(self, frame):
        self.label.reparentTo(frame)