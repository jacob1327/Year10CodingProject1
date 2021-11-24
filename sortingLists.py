import random
numbers = []

def sort_key(k):
    return k[1]

for i in range (1, 100):
    numbers += [[random.randint(1,100), chr(random.randint(65,90))]]
numbers.sort()
numbers.sort(key=sort_key)
for n in numbers:
    print(n)
