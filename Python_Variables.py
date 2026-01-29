#variables in Python
x = 5
y = "John"
print(x)
print(y)


x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)


x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
print(x)
print(y)
print(z)

x = "John"
print(x)
#double quotes are the same as single quotes:
x = 'John'
print(x)


#Variable names are case-sensitive:
a = 4
A = "Sally"

print(a)
print(A)

myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"


print(myvar)
print(my_var)
print(_my_var)
print(myVar)
print(MYVAR)
print(myvar2)

#Multi Words Variable Names
myVariableName = "John"
MyVariableName = "John"
my_variable_name = "John"

#multiple assignments
x, y, z = "Orange", "Banana", "Cherry"

print(x)
print(y)
print(z)
#same value to multiple variables
x = y = z = "Orange"
print(x)
print(y)
print(z)
#unpacking a collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits

print(x)
print(y)
print(z)
#output variables
x = "Python is awesome"
print(x)
#print multiple variables
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)
#you can also use the + operator to output multiple variables:
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

x = 5
y = 10
print(x + y)

x = 5
y = "John"
print(x, y)

x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)