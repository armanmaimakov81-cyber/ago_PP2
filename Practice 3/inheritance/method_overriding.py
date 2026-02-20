class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def introduce(self):
        print("Hello, my name is", self.firstname, self.lastname)


class Student(Person):
    def __init__(self, fname, lname, major):
        super().__init__(fname, lname)
        self.major = major

    # Method overriding
    def introduce(self):
        print("Hi, I'm", self.firstname, self.lastname,
              "and I study", self.major)


p = Person("John", "Smith")
p.introduce()

s = Student("Alice", "Brown", "Computer Science")
s.introduce()
