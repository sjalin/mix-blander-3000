BCM = 'BCM'
OUT = 'OUT'


def setmode(tmp):
    print(f'Fake GPIO set mode: {tmp}')


def setup(tmp1, tmp2):
    print(f'Fake GPIO setup: {tmp1}, {tmp2}')


def output(pin, state):
    print(f'Fake GPIO set pin {pin} to {state}')