from objects.notifier import Notifier


class Location(Notifier):
    def __init__(self, player):
        Notifier.__init__(self, "location")
        self.player = player
        self.action_bar = player.level_holder.action_bar
        self.self_portrait = player.level_holder.self_portrait
        self.actions = []  # list of lists
        self.stage = 0  # starting stage is 0

    def set_stage(self, stage):
        if stage < len(self.actions):
            self.notify.debug(f"[set_stage] Setting stage to {stage}")
            self.stage = stage
            self.action_bar.set_actions(self.actions[self.stage])
        else:
            self.notify.warning(f"[set_stage] Cannot set stage to {stage} (Out of index).")
