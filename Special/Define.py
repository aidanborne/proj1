# Define -- Parse tree node strategy for printing the special form define

from Special import Special

class Define(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p=False):
        cdr = t.getCdr()

        if cdr.isPair() and cdr.getCar().isPair():
            self.printIfStyle(t, n, p)
        else:
            self.printRegularStyle(t, n, p)
