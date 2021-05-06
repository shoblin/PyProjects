import random


class Dice:
    """
    Multi-sided dices

    num_sides: number of sides on Dice

    """

    def __init__(self, num_sides):
        self.num_sides = num_sides
        self.curr_value = self.roll()

    def roll(self):
        self.curr_value = random.randrange(1, self.num_sides + 1)
        return self.curr_value

    def __str__(self):
        return str(self.curr_value)

    def __repr__(self):
        return f"dx{self.num_sides}: {self.curr_value}"


class Roll:
    """

    """
    pass

