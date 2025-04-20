from objects.ui.tabbed.LogEntry import LogEntry
from objects.ui.tabbed.Tab import Tab


class Log(Tab):
    def __init__(self, clock):
        Tab.__init__(self)
        self.items = []
        self.clock = clock

        self.accept("add_log", self.add)

    def add(self, text):
        new_entry = LogEntry(f"[{self.clock.time}] {text}")
        for e in self.items:
            e.move_down()
        new_entry.reparentTo(self.frame)
        self.items.append(new_entry)