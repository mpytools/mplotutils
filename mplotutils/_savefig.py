from functools import wraps

from matplotlib.figure import Figure

# ensure the original implementation is not overwritten
try:
    savefig_orig
except NameError:
    savefig_orig = Figure.savefig


def savefig(func):

    @wraps(func)
    def inner(self, *args, **kwargs):

        # call draw in any case
        self.canvas.draw()

        return func(self, *args, **kwargs)

    return inner


class autodraw:

    def __init__(self, /, toggle):

        self.toggle = toggle
        if toggle:
            monkeypatch()
        else:
            undo()

    def __enter__(self):
        return

    def __exit__(self, type, value, traceback):

        if self.toggle:
            undo()
        else:
            monkeypatch()


def monkeypatch():
    # Monkey patch matplotlib to call our savefig instead of the standard

    Figure.savefig = savefig(savefig_orig)


def undo():
    Figure.savefig = savefig_orig
