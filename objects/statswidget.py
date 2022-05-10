"""
This is the stats widget in the bottom right
"""
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib
from direct.task import Task


class StatsWidget:
    def __init__(self, player, clock):
        self.player = player
        self.clock = clock
        self.white_square = OnscreenImage(image='art/white_square.png', scale=0.4, pos=(.88, 0, -.55))
        self.white_square.setTransparency(TransparencyAttrib.MAlpha)

        self.hour_text = OnscreenText(pos=(.6, -.25), scale=0.07,
                                      fg=(1, 1, 1, 1))
        self.money_text = OnscreenText(pos=(.6, -.35), scale=0.07,
                                       fg=(1, 1, 1, 1))
        self.update_stats()
        self.task_update_stats = taskMgr.doMethodLater(1, self.update_stats_task, 'update_stats')

    def update_stats(self):
        self.hour_text.setText(f"[{str(self.clock.time)}]")  # clock
        self.money_text.setText(f"${self.player.money}")  # money
        # hygiene
        # hunger
        # sleep

    def update_stats_task(self, task):
        self.update_stats()
        return Task.again
