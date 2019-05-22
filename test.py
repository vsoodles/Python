#!/usr/bin/python3

list = [12,45,555555,67,89,444444444444444,444444455,111]
x = 0
y = 0
list1 = []
for i in list:
   if i > x:
     x = i
     list.remove(x)
for j in list:
    if j > y:
       y = j
print(y)
print(x)
