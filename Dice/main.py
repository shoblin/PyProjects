import MSDie as MSD


def main():

    ms_dice6 = MSD.Dice(6)
    for _ in range(5):
        print(ms_dice6.curr_value)
        ms_dice6.roll()

    test_list = [MSD.Dice(6), MSD.Dice(20)]
    print(test_list)


if __name__ == '__main__':
    main()
