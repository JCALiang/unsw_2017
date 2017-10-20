#!/usr/bin/python3

# test3 : subset 4 test for sys.stdin iteration, stdout, sys.stdin.readlines, string % format
# written by Chieh An Liang

import sys


sys.stdout.write("test function sys.stdout.write\n")

text = sys.stdin.readlines()

for i in text:
    print(i)



for i in sys.stdin:
    print("%s comp9041" % i)

