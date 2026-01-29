#Quotes inside quotes
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = "Hello, World!"
print(a[1])

for x in "banana":
  print(x)

a = "Hello, World!"
print(len(a))

txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")

b = "Hello, World!"
print(b[2:5])

b = "Hello, World!"
print(b[:5])

b = "Hello, World!"
print(b[-5:-2])

a = "Hello, World!"
print(a.upper())

a = " Hello, World! "
print(a.strip())

a = "Hello, World!"
print(a.replace("H", "J"))

a = "Hello"
b = "World"
c = a + " " + b
print(c)

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

txt = "We are the so-called \"Vikings\" from the north."
print(txt) 

txt = "hello world"

print(txt.capitalize())
print(txt.casefold())
print(txt.lower())
print(txt.upper())
print(txt.title())
print(txt.swapcase())

txt = "I love apples, apples are my favorite fruit"

print(txt.count("apples"))
print(txt.find("apples"))
print(txt.index("apples"))

txt = "Hello123"

print(txt.isalnum())
print(txt.isalpha())
print(txt.isdigit())
print(txt.islower())
print(txt.isupper())

