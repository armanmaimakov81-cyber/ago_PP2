names = ["Alex", "Bob", "John"]
scores = [90, 85, 88]

# enumerate
for i, name in enumerate(names):
    print(i, name)

# zip
for name, score in zip(names, scores):
    print(name, score)


x = "123"
print(type(x))
num = int(x)
flt = float(x)
print(num, flt)
if isinstance(num, int):
    print("It is integer")
