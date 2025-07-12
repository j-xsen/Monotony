from objects.clock import Clock
from objects.ui.tabbed.logentry import LogEntry
from objects.ui.tabbed.tab import Tab


class Log(Tab):
    def __init__(self, clock: Clock):
        Tab.__init__(self)
        self.items = []
        self.clock = clock

        self.accept("add_log", self.add)

    def add(self, text: str):
        new_entry = LogEntry(f"[{self.clock.time}] {text}")
        for e in self.items:
            e.move_down()
        new_entry.reparentTo(self.frame)
        self.items.append(new_entry)