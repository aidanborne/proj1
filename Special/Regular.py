# Regular -- Parse tree node strategy for printing regular lists

from Special import Special

from Tree.Nil import Nil

class Regular(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        nil = Nil.getInstance()

        if t == nil:
            t.print(n, p)
            return

        print(" " * n, end="")

        if not p:
            print("(", end="")

        first = True

        while True:
            if not first:
                print(" ", end="")
            else:
                first = False

            t.getCar().print(0)

            t = t.getCdr()

            if t == nil:
                print(")", end="")
                break
            
            elif not t.isPair():
                print(" . ", end="")
                t.print(0)
                
                print(")", end="")
                break
        


        
