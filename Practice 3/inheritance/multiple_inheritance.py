class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, my name is", self.name)


class Worker:
    def __init__(self, salary):
        self.salary = salary

    def show_salary(self):
        print("My salary is", self.salary)


# Multiple inheritance
class WorkingStudent(Person, Worker):
    def __init__(self, name, salary, university):
        Person.__init__(self, name)
        Worker.__init__(self, salary)
        self.university = university

    def info(self):
        print(self.name, "studies at", self.university)


ws = WorkingStudent("David", 1500, "MIT")

ws.say_hello()
ws.show_salary()
ws.info()
