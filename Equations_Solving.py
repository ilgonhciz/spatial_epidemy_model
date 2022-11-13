import array
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math
n=5
Y=np.zeros((4,n))
V=np.zeros((n,n))
D=np.zeros((4,n))
Beta=[0]*n
Gamma=[0]*n
Nu=[0]*n
VS=[0]*n
VI=[0]*n
VR=[0]*n

def func(x):
    if x>=0:
        return(x)
    else:
        return(0)
def odes(x,t):
    # Constants
    n = 3
    V1=np.array([[0,10,10],[-10,0,10],[-10,-10,0]])
    V2=V1.ravel()
    Z0=np.empty(n)
    Z1=np.empty(n)
    Z2=np.empty(n)
    Beta=(0.1,10,20)
    Gamma=(0,0,0)
    Nu=(0,0,0)
    l=0
    D = np.zeros((n,4))
    for i in range(0,n):
         for l in range(0,4):
           Y[l][i]=x[4*i+l]
    #local variables
    # assign each ODE to a vector element
    for j in range(0,n):
        Z0[j]=Y[0][j]/(Y[0][j] + Y[1][j] + Y[2][j])
        Z1[j]=Y[1][j]/(Y[0][j] + Y[1][j] + Y[2][j])
        Z2[j]=Y[2][j]/(Y[0][j] + Y[1][j] + Y[2][j])
    for k in range(0,n):
         #Flow contribution
          VS[k]=np.dot(V1[k],Z0)*math.sin(2*math.pi*t)
          VI[k] =np.dot(V1[k], Z1) * math.sin(2 * math.pi * t)
          VR[k] =np.dot(V1[k], Z2) * math.sin(2 * math.pi * t)


# define each ODE
    for i in range(0,n):
           D[i][0]= -Beta[i] * Y[0][i] * Y[1][i] / (Y[0][i] + Y[1][i] + Y[2][i])-VS[i]
           D[i][1] = Beta[i] * Y[0][i] * Y[1][i] / (Y[0][i] + Y[1][i] + Y[2][i])-(Gamma[i]+Nu[i])*Y[1][i] - VI[i]
           D[i][2] = Gamma[i]*Y[1][i]-VR[i]
           D[i][3] = Nu[i]*Y[2][i]
    D=D.ravel()
    return(D)
     # initial conditions
Y00=np.array([[100,1,0,0],[10000,0,0,0],[100000,0,0,0]])
Y01=Y00.ravel()
odes(Y01,t=0)
# declare a time vector (time window)
t = np.linspace(0,100,10000)
(x,d) = odeint(odes,Y01,t,full_output = 1)

# plot the results
fig, ax = plt.subplots()
for i in range(0,n-2):
    for j in range(0,4):
     S1 = x[:,i*4+j]

ax.plot(t,x[:,0])
ax.legend()
plt.show()

