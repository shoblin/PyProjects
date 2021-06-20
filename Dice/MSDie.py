import random


class Dice:
    """
    Multi-sided dices
    """

    def __init__(self, num_sides=6):
        """
        :param
        """
        self.num_sides = num_sides
        self.curr_value = self.roll()

    def roll(self):
        self.curr_value = random.randrange(1, self.num_sides + 1)
        return self.curr_value

    def __str__(self):
        return str(self.curr_value)

    def __repr__(self):
        return f"dx{self.num_sides}: {self.curr_value}"


# class Throw:
#     """
#     *number of dice*d*number sides*
#     Exm: 3d6 - throw 3 6-sided dices
#     """
#
#     def __init__(self, dices):
#         dices = dices.split('d')
#         if len(dices) != 2:
#             raise Exception('Throw must match the pattern: 3d6')
#
#         self.num_dices = int(dices[0])
#         self.num_sides = int(dices[1])
#
#         self.dices = [Dice(self.num_sides) for i in range(self.num_dices)]
#
#     def get_sum(self):
#         r = 0
#         for dice in self.dices:
#             r += dice.curr_value
#         return f""
#
#
#     def new_throw(self):
#         print(self.dices[0])