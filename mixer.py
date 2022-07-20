import random
import time
from copy import copy

import platform
osname = platform.system()

if osname == 'Windows':
    from threadwithqueue import ThreadWithQueue
elif osname == 'Linux':
    from threadwithqueue.threadwithqueue import ThreadWithQueue
else:
    raise NotImplementedError(osname)

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    import fake_gpio as GPIO

import conf
import liquids
import recipes
from conf import RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, RANDOM_MAX_VOLUME

gpio_mapping = {0: 5,
                1: 6,
                2: 13,
                3: 19,
                4: 26,
                5: 21,
                6: 20,
                7: 16}


class Mixer(ThreadWithQueue):
    def __init__(self):
        super().__init__()
        self.class_name = self.__class__.__name__
        self._gpio_setup()
        self.pump_states = [False for _ in range(0, len(liquids.liquids))]
        self._gui = None

    def _handle_message(self, msg):
        if msg[0] == 'make drink':
            self._make_drink(msg[1])
        elif msg[0] == 'GUI':
            self._gui = msg[1]

    def _gpio_setup(self):
        self.log.info(f'{self.class_name}: GPIO setup')
        GPIO.setmode(GPIO.BCM)

        for i in range(0, 8):
            GPIO.setup(gpio_mapping[i], GPIO.OUT)
            GPIO.output(gpio_mapping[i], True)

    def _make_drink(self, drink_name):
        self._gui.set_progress(0)
        drink_recipe = []

        # For drinks not in the recipe book make a randon drink
        if drink_name not in recipes.recipes:
            self.log.warning(f'{self.class_name}: Drink does not exist make random drink instead')
            drink_name = f'Random drink'
            ing_amount = random.randrange(RANDOM_MIN_INGREDIENTS, RANDOM_MAX_INGREDIENTS, 1)
            liquid_volume = random.randrange(ing_amount, RANDOM_MAX_VOLUME, 1)

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
            drink_recipe = recipes.recipes[drink_name]

        self.log.info(f'{self.class_name}: Start making {drink_name}')
        self._gui.to_log(f'Start making {drink_name}')
        desired_pump_states = [False for _ in range(0, len(liquids.liquids))]
        for i in drink_recipe:
            desired_pump_states[liquids.liquids[i[0]]] = True
            self._gui.set_liquid_active(i[0], True)
        # print(desired_pump_states)
        self.set_pumps_state(desired_pump_states)

        for i in range(1, conf.MAX_VOLUME + 1):
            time.sleep(1)
            # print(i)
            progress = int(i / conf.MAX_VOLUME * 100)
            self._gui.set_progress(progress)
            for ing in drink_recipe:
                if ing[1] == i:  # Has been on for enough time
                    desired_pump_states[liquids.liquids[ing[0]]] = False
                    self._gui.set_liquid_active(ing[0], False)
            self.set_pumps_state(desired_pump_states)
            if True not in desired_pump_states:
                break
        self._gui.to_log(f'{drink_name} done')
        self._gui.set_progress(100)

    def set_pumps_state(self, desired_pump_states: list[bool]):
        for n, p in enumerate(desired_pump_states):
            if self.pump_states[n] != p:
                self.set_pump_state(n, p)
                self.pump_states[n] = p

    @staticmethod
    def set_pump_state(pump: int, state: bool):
        # Just placeholder code fo the moment
        if state:
            GPIO.output(gpio_mapping[pump], False)
            print(f'Starting pump {pump}')
        else:
            GPIO.output(gpio_mapping[pump], True)
            print(f'Stopping pump {pump}')
