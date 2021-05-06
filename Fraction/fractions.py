class Fractions:

    def __init__(self, top, bottom):
        """

        :param top:
        :param bottom:
        """
        common = gcd(top, bottom)

        self.num = top // common
        self.den = bottom // common

    def __str__(self):
        return str(self.num) + '/' + str(self.den)
    # Math function

    def __add__(self, other):
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Fractions(new_num, new_den)

    def __sub__(self, other):
        new_num = self.num * other.den - other.num * self.den
        new_den = self.den * other.den
        return Fractions(new_num, new_den)

    def __mul__(self, other):
        new_num = self.num * other.num
        new_den = self.den * other.den
        return Fractions(new_num, new_den)

    def __truediv__(self, other):
        new_num = self.num * other.den
        new_den = self.den * other.num
        return Fractions(new_num, new_den)

    # Logic functions
    def __eq__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 == new_num2

    def __ge__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 > new_num2

    def __gt__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 >= new_num2

    def __le__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 < new_num2

    def __lt__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 <= new_num2

    def __ne__(self, other):
        new_num1 = self.num * other.den
        new_num2 = self.den * other.num
        return new_num1 != new_num2


def gcd(m, n):
    while m % n != 0:
        oldm = m
        oldn = n

        m = oldn
        n = oldm % oldn

    return n


def main():
    a = Fractions(1, 4)
    b = Fractions(2, 4)
    print(a != b)


if __name__ == '__main__':
    main()