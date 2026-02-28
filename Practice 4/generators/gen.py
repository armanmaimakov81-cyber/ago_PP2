#1:
def squares(n):
    for i in range(n):
        yield i * i
n = int(input())
for i in squares(n):
    print(i)
#2:
def even(n):
    for i in range(n):
        if i % 2 == 0:
            if i+3>n:
                 yield i
            else:
                yield str(i)+','
for i in even(n):
    print(i,end='')
print(" ")
#3:
def div(n):
    for i in range(n+1):
        if i % 3 ==0 and i%4 == 0:
            yield i
for i in div(n):
    print(i,end=' ')
print(" ")
#4:
def squares(a,b):
    for i in range(a,b+1):
        yield i * i
a,b = map(int,input().split())
for i in squares(a,b):
    print(i,end=' ')
print(" ")
#5:
def count(n):
    for i in range(n , -1 , -1):
        yield i
for i in count(n):
    print(i,end=' ')
print(" ")