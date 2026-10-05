# Cond -- Parse tree node strategy for printing the special form cond

from Special import Special

class Cond(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        nil = Nil.getInstance()
        self.printIfStyle(t, n, p)

        if t == nil:
            t.print(n, p)
            return

        print(" " * n, end="")

        if not p:
            print("(cond", end="\r\n  ")
        
        first = True

        while True:
            if not first:
                print(" ", end="")
            else:
                first = False
            
            t.getCar().print(0)
            if (t.getCar().print(0)) == ")":
                print("", end="\r\n  ")
            t = t.getCdr()

            if t == nil:
                print(")", end="")
                break

            elif not t.isPair():
                print(" . ", end="")
                t.print(0)

                print(")", end="")
                break        
