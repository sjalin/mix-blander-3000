import random

import liquids
import recipes
from conf import RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, RANDOM_MAX_VOLUME


def make_drink(drink_name):
    drink_recipe = []

    # For drinks not in the recipe book make a randon drink
    if drink_name not in recipes.recipes:
        ing_amount = random.randrange(RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, 1)
        liquid_volume = random.randrange(ing_amount, RANDOM_MAX_VOLUME, 1)
        print(f'{drink_name} not in recipes, making random drink with '
              f'{ing_amount} ingredients and {liquid_volume} total volume')

        for _ in range(ing_amount):
            # TODO: Make the same liquid not appear more than once
            drink_recipe.append((list(liquids.liquids.keys())[random.randrange(0, len(liquids.liquids), 1)], 1))
        if len(drink_recipe) < liquid_volume:
            for _ in range(liquid_volume - len(drink_recipe)):
                r = random.randrange(0, len(drink_recipe))
                drink_recipe[r] = (drink_recipe[r][0], drink_recipe[r][1]+1)
    else:
        print(f'Start making {drink_name}')
        drink_recipe = recipes.recipes[drink_name]
    print(drink_recipe)
