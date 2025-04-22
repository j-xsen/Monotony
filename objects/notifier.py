from direct.directnotify.DirectNotifyGlobal import directNotify


class Notifier:
    def __init__(self, name: str):
        self.notify = directNotify.newCategory(name)
