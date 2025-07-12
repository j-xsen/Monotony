from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG
from direct.showbase.ShowBaseGlobal import aspect2d
from panda3d.core import TextNode, LVecBase3f

from objects.ui.uiconstants import UIConstants


def add_log(text: str):
    messenger.send("add_log", [text])


class Action:
    def __init__(self, text: str):
        """
        An action that is able to be done.
        :param text: The text to be displayed on the button.
        :type text: str
        """
        self.font = loader.loadFont("Monotony-Regular.ttf")
        # self.font.setPixelsPerUnit(120)
        self.text_scale = 0.1
        self.text_node_path = None
        self.button = None
        self.text_node = TextNode(text)
        self.text_node.setText(text)
        self.text_node.setFont(self.font)
        self.text_node.setAlign(TextNode.ACenter)

    def create_button(self):
        """
        Creates a DirectButton
        """
        self.button = DirectButton(scale=((self.text_node.getWidth() * self.text_scale) + 0.2, 1, 0.3), relief=None,
                                   command=self.command,
                                   geom=loader.loadModel('art/drawn_square.egg').find("**/drawn_square"))
        self.text_node_path = aspect2d.attachNewNode(self.text_node.generate())
        self.text_node_path.setScale(self.text_scale)
        self.text_node_path.wrtReparentTo(self.button)
        self.text_node_path.setPos(0, 0, -.1)

    def destroy_button(self):
        """
        Destroys the DirectButton self.button
        """
        self.button.destroy()

    def command(self):
        pass

    def set_pos(self, pos):
        self.button.setPos(pos)

    def multiply_scale(self, multiple):
        cur = self.button.getScale()
        lvec = LVecBase3f(multiple * cur.x, multiple * cur.y, multiple * cur.z)
        self.button.setScale(lvec)

    def disable_button(self):
        tint = .4
        self.button["state"] = DGG.DISABLED
        self.button.setColor(tint, tint, tint, 1)

    def enable_button(self):
        self.button["state"] = DGG.NORMAL
        self.button.setColor(UIConstants.COLOR_ENABLE)


class DelayedAction(Action):
    def __init__(self, text: str):
        Action.__init__(self, text)

    def post(self, e):
        pass
