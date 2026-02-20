#ex1:
x = lambda a : a + 10
print(x(5))
#ex2:
x = lambda a, b : a * b
print(x(5, 6))
#ex3:
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))
#ex4:
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))