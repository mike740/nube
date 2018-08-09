from math import cos, exp, pi
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt


#a=946.3
b=6.214
c=8.143

# function we want to integrate
def f(x):
    return exp(-((x-b)/c)**2)
    #return exp(cos(-2 * x * pi)) + 3.2

# call quad to integrate f from -2 to 2
res, err = quad(f, 1, 12)

print("The numerical result is {:f} (+-{:g})"
    .format(res, err))

a=11*1858/res
print(a)

x=np.linspace(1,12,12)
print (x)
y=[]
for i in range (len(x)): 
    funcion=a*exp(-((x[i]-b)/c)**2)
    y.append(funcion)


plt.plot(x,y)
plt.ylim((0,a*1.2))

plt.show()
