import math
#1:
deg = float(input())
rad = deg * math.pi / 180
print(round(rad,6))
#2:
h = float(input())
a = float(input())
b = float(input())
area =0.5 * h * (a+b)
print(area)
#3:
n = float(input())
a = float(input())
area = (n*a*a) / (4 * math.tan(math.pi/n))
print(round(area))
#4:
a = float(input())
b = float(input())
area = a * b
print(area)