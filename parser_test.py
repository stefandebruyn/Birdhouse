import os
from interpreter.parsing import parse

input = open(os.getcwd() + "/input.txt", "r").readline()
result = parse("I want to live in Deer Park, Texas for around four hundred million.")

for r in result:
    print(r)
