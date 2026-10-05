# Let -- Parse tree node strategy for printing the special form let

from Special import Special

class Let(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
<<<<<<< HEAD
        nil = Nil.getInstance()
=======
        self.printBeginStyle(t, n, p)
>>>>>>> ea405699e0755c9cfb0705eaf943b28a5780d461

        if t == nil:
            t.print(n, p)
            return

        print(" " * n, end="")

        if not p:
            print("(let", end="\r\n  ")
        
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
