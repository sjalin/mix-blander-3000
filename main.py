import liquids
import recipes
import mixer

from flask_server import app as webapp


def test_stuff():
    liquids.test_liquids()
    recipes.test_recipes()


def main():
    print('Start mix-blander-3000')
    test_stuff()

    # Test code to run something in the beginning

    mix = mixer.Mixer()
    mix.start()

    webapp.setMixer(mix.message_queue)
    webapp.run(port=8080)


if __name__ == '__main__':
    main()
