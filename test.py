import numpy as np

a = [
    [
        [9,2,2,2],
        [9,3,3,3],
        [9,4,4,4],
        [9,5,5,5],
    ],
    [
        [7,2,2,2],
        [7,3,3,3],
        [7,4,4,4],
        [7,5,5,5],
    ],
    [
        [10,2,2,2],
        [10,3,3,3],
        [10,4,4,4],
        [10,5,5,5],
    ],
    [
        [5,2,2,2],
        [5,3,3,3],
        [5,4,4,4],
        [5,5,5,5],
    ],
]

a = sorted(a, key=lambda x: x[0][0])

# print(a)



def divideByN(list2divide,n):
    print(list2divide)
    listFinal = []
    xc = int(np.ceil(len(list2divide)/n))
    if n == 1:
        listFinal = list2divide
        print(listFinal)
    else:
        listFinal.append(list2divide[0:xc]) # first slice
        if n > 2:
            for i in range(2,n):
                listFinal.append(list2divide[xc*(i-1):xc*i]) # intermediate slice

        listFinal.append(list2divide[xc*(n-1):len(list2divide)]) # last slice

        [print(lf) for lf in listFinal]


z = ["a", "b", "c", "d" , "e", "f", "g", "h"]
z = range(100)
p = 4

# divideByN(z,p)


print(list(range(0,100)))
# x = len(z)/p
# xc = int(np.ceil(len(z)/p))
# print(x, xc)

# z1 = z[0:xc]
# z2 = z[xc:xc*2]
# z3 = z[xc*2:]

# print(z1)
# print(z2)
# print(z3)