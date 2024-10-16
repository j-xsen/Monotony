from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d.core import ConfigVariableString


class Notifier:
    def __init__(self, name):
        self.notify = directNotify.newCategory(name)
        ConfigVariableString(f"notify-level-{name}", "debug")
