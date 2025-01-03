from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG
from direct.showbase.ShowBaseGlobal import aspect2d
from panda3d.core import TextNode, LVecBase3f

from objects.ui.detailrectangle import LogEntry

text_scale = 0.1


class Action:
    def __init__(self, text, player):
        """
        An action doable in a location
        @param text: Text to display on button
        @param player: player object
        """
        self.text_node_path = None
        self.button = None
        self.player = player
        self.text_node = TextNode(text)
        self.text_node.setText(text)
        self.text_node.setFont(self.player.font)
        self.text_node.setAlign(TextNode.ACenter)

    def create_button(self):
        """
        Creates a DirectButton
        """
        self.button = DirectButton(scale=((self.text_node.getWidth() * text_scale) + 0.2, 1, 0.3), relief=None,
                                   command=self.command,
                                   geom=self.player.drawn_square, )
        self.text_node_path = aspect2d.attachNewNode(self.text_node.generate())
        self.text_node_path.setScale(text_scale)
        self.text_node_path.wrtReparentTo(self.button)
        self.text_node_path.setPos(0, 0, -.1)

    def destroy_button(self):
        """
        Destroys the DirectButton self.button
        """
        self.button.destroy()

    def command(self):
        """
        Call to check validity
        """
        return self.player.able

    def set_pos(self, pos):
        self.button.setPos(pos)

    def multiply_scale(self, multiple):
        cur = self.button.getScale()
        lvec = LVecBase3f(multiple * cur.x, multiple * cur.y, multiple * cur.z)
        self.button.setScale(lvec)

    def add_log(self, text):
        log = self.player.detail_rectangle.log
        log.add(LogEntry(f"[{self.player.clock.time}] {text}", self.player.font))

    def disable_button(self):
        tint = .4
        self.button["state"] = DGG.DISABLED
        self.button.setColor(tint, tint, tint, 1)

    def enable_button(self):
        self.button["state"] = DGG.NORMAL
        self.button.setColor(1, 1, 1, 1)


class DelayedAction(Action):
    def __init__(self, text, player):
        super().__init__(text, player)

    def post(self, e):
        pass
