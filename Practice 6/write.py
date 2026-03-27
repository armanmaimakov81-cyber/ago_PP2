with open("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\sample.txt", "w") as f:
    f.write("Hello\n")
    f.write("This is a sample file\n")

with open("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\sample.txt", "a") as f:
    f.write("New line 1\n")
    f.write("New line 2\n")

with open("C:\\Users\\acer\\Documents\\hefbvi\\Practice 6\\sample.txt", "r") as f:
    print(f.read())

