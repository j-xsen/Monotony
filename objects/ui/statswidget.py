from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task

from objects.ui.panel import Panel


class StatsWidget(Panel):
    def __init__(self, player, clock):
        Panel.__init__(self, "statswidget",
                       frame_size=(.85, 0, .85, 0),
                       pos=(0.45, 0, -.975))

        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.clock = clock
        self.player = player

        self.hour_text = OnscreenText(pos=(.6, -.25), scale=0.07,
                                      fg=(1, 1, 1, 1), font=self.font)
        self.money_text = OnscreenText(pos=(.6, -.35), scale=0.07,
                                       fg=(1, 1, 1, 1), font=self.font)

        # hygiene bar
        self.hygiene_text = OnscreenText(pos=(1.08, -.45), scale=0.07,
                                         fg=(1, 1, 1, 1), text="Hygiene", font=self.font)
        self.hygiene_bar = DirectWaitBar(value=100, pos=(0.875, 0, -.5), scale=(1, 1, 0.75),
                                         barColor=(1, 1, 1, 1), frameColor=(0, 0, 0, 1),
                                         frameSize=(-0.35, 0.35, -0.050, .025))

        # hunger bar
        self.hunger_text = OnscreenText(pos=(1.1, -.615), scale=0.07,
                                        fg=(1, 1, 1, 1), text="Hunger", font=self.font)
        self.hunger_bar = DirectWaitBar(value=100, pos=(0.875, 0, -.665), scale=(1, 1, 0.75),
                                        barColor=(1, 1, 1, 1), frameColor=(0, 0, 0, 1),
                                        frameSize=(-0.35, 0.35, -.050, .025))

        # Tired bar
        self.sleep_text = OnscreenText(pos=(1.12, -.8), scale=0.07,
                                       fg=(1, 1, 1, 1), text="Sleep", font=self.font)
        self.sleep_bar = DirectWaitBar(value=100, pos=(0.875, 0, -.85), scale=(1, 1, 0.75),
                                       barColor=(1, 1, 1, 1), frameColor=(0, 0, 0, 1),
                                       frameSize=(-0.35, 0.35, -.050, .025))

        self.accept("update_stats", self.update_stats)
        self.update_stats()

    def update_stats(self):
        self.hour_text.setText(f"[{str(self.clock.time)}]")  # clock
        self.money_text.setText(f"${self.player.money}")  # money
        # hygiene
        self.hygiene_bar['value'] = self.player.hygiene.value
        # hunger
        self.hunger_bar['value'] = self.player.hunger.value
        # sleep
        self.sleep_bar['value'] = self.player.sleep.value

    def update_stats_task(self, task):
        self.update_stats()
        return Task.again
