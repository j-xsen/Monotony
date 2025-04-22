from objects.notifier import Notifier


class Stat(Notifier):
    def __init__(self, value: int, stat_max: int = 100, stat_min: int = 0):
        """

        :param value: Starting value of the stat.
        :type value: int
        :param stat_max: Maximum value of the stat.
        :type stat_max: int
        :param stat_min: Minimum value of the stat.
        :type stat_min: int
        """
        Notifier.__init__(self, "stat")
        self.value = value
        self.stat_max = stat_max
        self.stat_min = stat_min

    def __add__(self, other: int):
        self.value = self.change_value(other)
        return self

    def __sub__(self, other: int):
        self.value = self.change_value(-other)
        return self

    def __str__(self):
        return f"{self.value}"

    def change_value(self, adjust: int) -> int:
        """

        :param adjust: Amount to adjust the stat by.
        :type adjust: int
        :return: The new stat value.
        :rtype: int
        """
        rtrn = int(self.value) + adjust
        if rtrn > self.stat_max:
            self.notify.debug(f"[change_value] {self.value} + {adjust} > {self.stat_max}. Setting value to {self.stat_max}.")
            return self.stat_max
        elif rtrn < self.stat_min:
            self.notify.debug(f"[change_value] {self.value} + {adjust} < {self.stat_min}. Setting value to {self.stat_min}.")
            return self.stat_min
        messenger.send("update_stats")
        return rtrn
