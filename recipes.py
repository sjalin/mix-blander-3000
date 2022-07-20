# Descriptions on how to mix the drinks

import liquids
import logging

recipes = {'GT': [('gin', 1), ('tonic', 4)],
           'Gin balalaika': [('gin', 1), ('orange juice', 4), ('russian water', 4)],
           'Fulgrogg': [('fanta', 1), ('rum', 2), ('gin', 1), ('punsch', 1)],
           'Golden shower': [('fanta', 6), ('punsch', 2)],
           }


def test_recipes():
    cant_do = []
    for name, parts in recipes.items():
        can_do = True
        for p in parts:
            if p[0] not in liquids.liquids.keys():
                print(f'Can\'t make {name} due to lack of {p[0]}')
                can_do = False
        if not can_do:
            cant_do.append(name)
    if cant_do:
        logging.warning(f'Can\'t do the following {cant_do}')
