#!/usr/bin/python3
# written by Chieh-An Liang
# demo1 to test subset  2: single line if while, logical, comparison, bitwise operators


x = 1
y = 0

print( x + y)
while x <= 10: print(x); x = x + 2
print()
while not y: print(y); y = y + 1
print()
ans = 5
while x and ans: print(x + ans); ans = ans -1
print()
while x & ans: print(x + ans); ans = ans -1
ans = 5
if ans > 10: ans = ans + 2
if ans == 5: ans = ans - 1
print(ans)
