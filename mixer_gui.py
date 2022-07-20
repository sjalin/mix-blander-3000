from kivy.utils import get_color_from_hex

import recipes
import liquids

from queue import SimpleQueue

from kivy.app import App
from kivy.clock import mainthread
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

from functools import partial

# Made for resolution 800 X 480



class MyGrid(Widget):
    p_bar: ProgressBar
    std_out: TextInput
    drink_mixing = False
    mixer_buttons: GridLayout
    insert_liquids_here: GridLayout

    def __init__(self, message_queue):
        self.message_queue: SimpleQueue = message_queue
        self.message_queue.put(('GUI', self))
        self.liquid_buttons = {}
        super().__init__()
        for r in recipes.recipes.keys():
            b = Button(text=r)
            b.color = get_color_from_hex('#00834d')
            b.background_color = get_color_from_hex('#007700')
            b.bind(on_press=partial(self.drink_btn_click, r))
            self.mixer_buttons.add_widget(b)
            b.font_size = 33
        for l in liquids.liquids.keys():
            b = Button(text=l)
            b.color = get_color_from_hex('#FFFFFF')
            b.background_color = get_color_from_hex('#abcdef')
            b.bind(on_press=partial(self.liquid_btn_press, l))
            b.bind(on_release=partial(self.liquid_btn_release, l))
            b.font_size = 22
            self.insert_liquids_here.add_widget(b)
            self.liquid_buttons[l] = b


    @mainthread
    def to_log(self, text):
        # t = time.strftime("%H:%M:%S", time.localtime())
        # self.std_out.text += f'\n{t} - {text}'
        self.std_out.text += f'\n{text}'

    @mainthread
    def set_progress(self, progress):
        self.p_bar.value = progress

    @mainthread
    def set_liquid_active(self, button, state):
        if state:
            self.liquid_buttons[button].background_color = get_color_from_hex('#fedcba')
        else:
            self.liquid_buttons[button].background_color = get_color_from_hex('#abcdef')

    def drink_btn_click(self, drink_id, *args):
        self.message_queue.put(('make drink', drink_id))

    def liquid_btn_press(self, liquid, *args):
        self.message_queue.put(('start liquid', liquid))

    def liquid_btn_release(self, liquid, *args):
        self.message_queue.put(('stop liquid', liquid))


class GuiApp(App):
    def __init__(self, message_queue):
        self.message_queue = message_queue
        super().__init__()

    def build(self):
        return MyGrid(self.message_queue)
