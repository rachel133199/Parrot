r = 0.2
avg = 0
while True:
    x = int(input())
    avg = (1 - r)*avg + r*x
    print(avg)
