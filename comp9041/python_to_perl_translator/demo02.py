#!/usr/bin/python3

# demo2 : subset 3 test for multiline, for range(), while, if
# written by Chieh An Liang

import sys

for i in range(10):
    print(i)
print()

for i in range(5,10):
    print(i)
print()

i = 1
j = 1
while i <= 5:
    while j <= 5:
        print(j)
        j = j + 1
    i = i + 1
print()

if i > 0:
    i = i + 1
    print(i)
elif a == 0:
    print(i)
else:
    print("smaller than 0")
