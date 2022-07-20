import liquids
import recipes
import mixer


def test_stuff():
    liquids.test_liquids()
    recipes.test_recipes()


def main():
    print('Start mix-blander-3000')
    test_stuff()

    # Test code to run something in the beginning
    # Will make a random drink since GT1 is not in the recipes
    mixer.make_drink('GT1')


if __name__ == '__main__':
    main()
