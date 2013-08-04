from fabric.api import puts
from fabric.colors import red, green, yellow


def notify(msg):
    return puts(green(msg))


def warn(msg):
    return puts(yellow(msg))


def alert(msg):
    return puts(red(msg))
