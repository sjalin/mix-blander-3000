import liquids
import recipes
import mixer
import logging

from mixer_gui import GuiApp
from kivy.core.window import Window

try:
    import RPi.GPIO as GPIO
    TARGET = True
except ModuleNotFoundError:
    TARGET = False


def test_stuff(log):
    log.info('Start self test')
    liquids.test_liquids()
    recipes.test_recipes()
    log.info('Self test done')


def main():
    # logging.basicConfig(level=logging.WARNING)
    log = logging.getLogger('Mix-Balnder 3000')
    # log.setLevel(logging.INFO)
    log.info('Start')
    test_stuff(log)

    # Test code to run something in the beginning

    log.info('Start mixer')
    mix = mixer.Mixer()
    mix.start()

    log.info('Start kivy')
    app = GuiApp(mix.get_message_queue())
    if TARGET:
        Window.fullscreen = 'auto'
    else:
        Window.borderless = True
        Window._size = (800, 480)
        log.warning('Not running on fullscreen')
    app.run()

    log.info('Teardown')
    mix.get_message_queue().put(('DIE', None))
    mix.join()

    log.info('Stop')


if __name__ == '__main__':
    main()
