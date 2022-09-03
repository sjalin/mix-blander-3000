import random
import time
from copy import copy
from threadwithqueue.threadwithqueue import ThreadWithQueue


try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    import fake_gpio as GPIO

import conf
import liquids
import recipes
from conf import RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, RANDOM_MAX_VOLUME


class Mixer(ThreadWithQueue):
    def __init__(self):
        super().__init__()
        self.gpio_setup()
        self.pump_states = [False for _ in range(0, len(liquids.liquids))]

    def run(self):
        super().run()
        while True:
            msg = self.get_message(3000)
            if msg:
                print(msg)
                self.make_drink(msg)

    @staticmethod
    def gpio_setup():
        print('GPIO setup')
        GPIO.setmode(GPIO.BCM)

        for i in range(0, 15):
            GPIO.setup(i, GPIO.OUT)

    def make_drink(self, drink_name):
        drink_recipe = []

        # For drinks not in the recipe book make a randon drink
        if drink_name not in recipes.recipes:
            ing_amount = random.randrange(RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, 1)
            liquid_volume = random.randrange(ing_amount, RANDOM_MAX_VOLUME, 1)
            print(f'{drink_name} not in recipes, making random drink with '
                  f'{ing_amount} ingredients and {liquid_volume} total volume')

            tmp_liquids = copy(liquids.liquids)
            for _ in range(ing_amount):
                # TODO: Make the same liquid not appear more than once
                new_ing = (list(tmp_liquids.keys())[random.randrange(0, len(tmp_liquids), 1)], 1)
                tmp_liquids.pop(new_ing[0])
                drink_recipe.append(new_ing)
            if len(drink_recipe) < liquid_volume:
                for _ in range(liquid_volume - len(drink_recipe)):
                    r = random.randrange(0, len(drink_recipe))
                    drink_recipe[r] = (drink_recipe[r][0], drink_recipe[r][1] + 1)
        else:
            print(f'Start making {drink_name}')
            drink_recipe = recipes.recipes[drink_name]
        print(drink_recipe)

        print('Start of making drink')
        desired_pump_states = [False for _ in range(0, len(liquids.liquids))]
        for i in drink_recipe:
            desired_pump_states[liquids.liquids[i[0]]] = True
        print(desired_pump_states)
        self.set_pumps_state(desired_pump_states)

        for i in range(1, conf.MAX_VOLUME + 1):
            time.sleep(1)
            print(i)
            for ing in drink_recipe:
                if ing[1] == i:
                    desired_pump_states[liquids.liquids[ing[0]]] = False
                    self.set_pumps_state(desired_pump_states)
            if True not in desired_pump_states:
                break

    def set_pumps_state(self, desired_pump_states: list[bool]):
        for n, p in enumerate(desired_pump_states):
            if self.pump_states[n] != p:
                self.set_pump_state(n, p)
                self.pump_states[n] = p

    @staticmethod
    def set_pump_state(pump: int, state: bool):
        # Just placeholder code fo the moment
        if state:
            GPIO.output(pump, True)
            print(f'Starting pump {pump}')
        else:
            GPIO.output(pump, False)
            print(f'Stopping pump {pump}')
