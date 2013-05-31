#!/usr/bin/env python

import prettytable
import sys
import pickle
import copy

class BadInterpretationError(Exception): pass

# interval
class I(object):

    LBOUND = float("-inf")
    UBOUND = float("inf")

    def __init__(self, data = None):
        if data != None and len(data) != 2:
            raise BadInterpretationError("bad interval data: %s" % data)

        if data != None and data[0] > data[1]:
            raise BadInterpretationError("l > u: %s" % (data,))

        self.data = data

    def __str__(self):
        if self.data == None:
            return ("{}")

        return "[%s, %s]" % (self.data[0], self.data[1])

    # join | (ie, the set union)
    def __or__(self, other):
        if self.data == None:
            return other
        elif other.data == None:
            return self
        else:
            l = min(self.data[0], other.data[0])
            u = max(self.data[1], other.data[1])
            return I((l, u))

    # meet & (ie, the set intersection)
    def __and__(self, other):

        if self.data == None or other.data == None:
            return I(None)
        else:
            l = max(self.data[0], other.data[0])
            u = min(self.data[1], other.data[1])

            if l <= u:
                return I((l, u))
            else:
                return I() # empty interval

    def __add__(self, other):
        if self.data == None:
            return other
        elif other.data == None:
            return self
        else:
            l = self.data[0] + other.data[0]
            u = self.data[1] + other.data[1]

            return I((l, u))

    def __sub__(self, other):
        if self.data == None:
            return I.bot()
        elif other.data == None:
            return self
        else:
            l = self.data[0] - other.data[1]
            u = self.data[1] - other.data[0]
            return I((l, u))

    @staticmethod
    def top():
        return I((I.LBOUND, I.UBOUND))

    @staticmethod
    def bot():
        return I((None))

# main stuff

def print_state(st):
    tb = prettytable.PrettyTable(["PP", "Abstraction"])

    for i in range(len(st)):
        tb.add_row([i+1, str(st[i])])

    print(tb.get_string())

def make_sig(state):
    sig = ""
    for i in state:
        sig += pickle.dumps(i)

    return(sig)

if __name__ == "__main__":
    state = [ I.bot() for x in range(5) ]

    sig = make_sig(state)

    for iter in range(100):
        state[1-1] = I.top()
        state[2-1] = I((6, 6)) | state[4-1]
        state[3-1] = state[2-1] & I((1, I.UBOUND))
        state[4-1] = state[3-1] - I((2, 2))
        state[5-1] = state[2-1] & I((I.LBOUND, 0))


        print("ITERATION: %s" % iter)
        print_state(state)
        raw_input()

        new_sig = make_sig(state)
        if sig == new_sig:
            break

        sig = new_sig


    else:
        raise BadInterpretationError("100 iters")

    print("fixpoint met")
