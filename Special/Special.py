# Special -- Parse tree node strategy for printing special forms

from abc import ABC, abstractmethod

from Tree.Nil import Nil

import sys

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.

class Special(ABC):
    @abstractmethod
    def print(self, t, n, p):
        pass

    def printRegularStyle(self, t, n, p=False):
        for _ in range(0, n):
            print(' ', end='')

        if not t.isPair():
            t.print(0, p)
            return

        if not p:
            print('(', end='')
        else:
            print(' ', end='')

        self.printRegularStyle(t.getCar(), 0, False)
        self.printRegularStyle(t.getCdr(), 0, True)

    def printBeginStyle(self, t, n, p=False):
        if not p:
            for _ in range(0, n):
                sys.stdout.write(' ')

            sys.stdout.write('(')

        car = t.getCar()
        cdr = t.getCdr()

        # print first element
        self.printRegularStyle(car, 0)

        # print rest of elements on indented lines
        while not cdr.isNull():
            sys.stdout.write('\n')

            cdr.getCar().print(n + 2, False)
            cdr = cdr.getCdr()

        sys.stdout.write('\n')

        for _ in range(0, n):
            sys.stdout.write(' ')

        sys.stdout.write(')')

    def printIfStyle(self, t, n, p=False):
        if not p:
            for _ in range(0, n):
                sys.stdout.write(' ')

            sys.stdout.write('(')

        car = t.getCar()
        cdr = t.getCdr()

        # print first element
        self.printRegularStyle(car, 0)

        # print 2nd element if it exists
        if not cdr.isNull():
            sys.stdout.write(' ')
            self.printRegularStyle(cdr.getCar(), 0)

            cdr = cdr.getCdr()

        # print remaining elements
        while not cdr.isNull():
            sys.stdout.write('\n')

            cdr.getCar().print(n + 2, False)
            cdr = cdr.getCdr()

        sys.stdout.write('\n')

        for _ in range(0, n):
            sys.stdout.write(' ')

        sys.stdout.write(')')
        
