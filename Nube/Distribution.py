from math import cos, exp, pi
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt



def distribution(irradiation):
    averageMonth=[] #vector of average irradiation by  month [kwh/kwp/month]
    #a=946.3
    b=6.214
    c=8.143
    
    # function we want to integrate
    def f(x):
        return exp(-((x-b)/c)**2)
        #return exp(cos(-2 * x * pi)) + 3.2
    
    # call quad to integrate f from -2 to 2
    res, err = quad(f, 1, 12)
    '''
    print("The numerical result is {:f} (+-{:g})"
        .format(res, err))
    '''
    a=11*irradiation/res
    #print(a)
    
    x=np.linspace(1,12,12)
    y=[]
    y2=[]
    
    for i in range (len(x)): 
        funcion=a*exp(-((x[i]-b)/c)**2)
        y.append(funcion)
        averageMonth.append(irradiation/12)
    yDistributionMean= sum(y)/len(y)
  
    correction=(irradiation-yDistributionMean) # correction coefficient 
  
    for i in range (len(x)):
        y2Temporal=(y[i]+correction)/12 #irradiation distribution by month
        y2.append(y2Temporal) 
        
   
    y2prom=sum(y2)/len(y2)
    print('y2 promedio'+str(y2prom))# includes correction factor
    
    plt.figure(3)
    plt.plot(x,y2,x,averageMonth)
    
    
    
    
    return (y2)
    
   




#irradiationDistribution=distribution(irradiation)