from codes.locations import *


class Player:
    def __init__(self):
        self.location = BED
        self.active = True  # this is if the player can take an action
        self.hygiene = 100
        self.hunger = 100
        self.sleep = 100
        self.money = 100
