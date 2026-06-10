import numpy as np

freq = 2e9
lamda = 3e8/freq
D = np.array([10, 12.8, 15.9, 19, 22.3, 25.6])

D_lambda = D*lamda

print(D_lambda)
