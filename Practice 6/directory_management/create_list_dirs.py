import os

os.makedirs("folder1/folder2/folder3", exist_ok=True)
print("Directories created")

items = os.listdir(".")

for item in items:
    print(item)


for file in os.listdir("."):
    if file.endswith(".py"):
        print(file)

