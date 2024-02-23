
# Feb. 23, 2024
# Rich W.
# with GitHub CoPilot
# MSL.l

from importlib.machinery import SourceFileLoader
from inspect import ismodule
import types

print()
print("an exploration of the globals() in Python")
print()

print("The several 'if' type-checking conditionals give indication")
print("how weird the Python language is.")

print()

gk = list(globals().keys())

print("globals() keys: " + str(len(gk)))
print()

for k in gk:
    print("global key " + k)
    gki = globals()[k]
    if gki is None:
        print(k + " is type 'None'")
    elif isinstance(gki, SourceFileLoader):
        print(k + " is type 'SourceFileLoader'")
    elif ismodule(gki):
        print(k + " ismodule returned true")
    elif isinstance(gki, type):
        print(k + " is type 'type'")
    elif isinstance(gki, types.FunctionType):  
        print(k + " is type 'function'")
    else:
        print(k + " length: " + str(len(gki)))
    print()