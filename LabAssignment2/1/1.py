import numpy as np

#A
M = np.arange(5,21)
print(M)
print('\n')

#B
M = M.reshape(4,4)
print(M)
print('\n')

#C
M[1:3, 1:3] = 0
print(M)
print('\n')

#D
M = M@M
print(M)
print('\n')

#E
v = M[0]
mag = np.sqrt(sum(i**2 for i in v))
print(mag)