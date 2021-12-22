import numpy as np

M=np.arange(25)+2
print(M)
print()

M=M.reshape(5,5)
print(M)
print()

M[1:4,1:4]=np.zeros((3,3))
print(M)
print()

M=M@M
print(M)
print()

v=M[0]

mag=0
for i in range(0,5):
    mag+=v[i]**2
print(np.sqrt(mag))
