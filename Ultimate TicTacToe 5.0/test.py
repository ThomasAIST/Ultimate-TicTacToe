# i = 0
# import time
# start = time.time()
# while i <7000000:
#     i+=1
# end = time.time()
# print(end-start)

import timeit
tem = [' ', ' ', '2', ' ', ' ', '1', ' ', ' ', ' ',
       '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
       ' ', '1', ' ', ' ', '1', ' ', ' ', '2', ' ',
       ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ',
       ' ', ' ', '1', ' ', '2', ' ', ' ', ' ', ' ',
       '1', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ',
       ' ', ' ', ' ', '2', ' ', ' ', ' ', '2', ' ',
       ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
       '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

hashing = [2**64, 2**64-2, 2**64-1]
def temfunc():
    num = 0
    for i in range(len(tem)):
        if i == ' ':
            num ^= hashing[0]
        elif i == '1':
            num ^= hashing[1]
        else: 
            num ^= hashing[2]
        num ^= i
    return num

print(timeit.timeit(lambda: ''.join(tem), number=10000000))
print(timeit.timeit(lambda: temfunc, number=10000000))