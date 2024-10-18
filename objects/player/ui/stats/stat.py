class Stat:
    def __init__(self, value, max=100, min=0):
        """
        An integer with a minimum and maximum
        @param value: Value of the Stat
        @param max: Highest the Stat can go (default: 100)
        @param min: Lowest the Stat can go (default: 0)
        """
        self.value = value
        self.max = max
        self.min = min

    def __add__(self, other):
        self.value = self.change_value(other)
        return self

    def __sub__(self, other):
        self.value = self.change_value(-other)
        return self

    def __str__(self):
        return f"{self.value}"

    def change_value(self, adjust):
        """
        Adjust self.value within self.max and self.min
        @param adjust: Amount to add to self.value
        @return: Int new self.value
        """
        rtrn = int(self.value) + adjust
        if rtrn > self.max:
            return rtrn - adjust
        elif rtrn < self.min:
            return self.min
        return rtrn
