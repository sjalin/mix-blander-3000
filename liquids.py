# Configuration of how the liquids are stored places in the contraption

liquids = {'punsch': 0,
           'gin': 1,
           'orange juice': 2,
           'russian water': 3,
           'tonic': 4,
           'vodka': 5,
           'fanta': 6,
           'rum': 7,}


def test_liquids():
    values = liquids.values()
    vals = set(values)

    if len(vals) != len(values):
        raise ValueError(f'different liquids cant be on the same place {values}')
