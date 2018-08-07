'''
Created on Jul 31, 2018

@author: Miguel RT
Source of information:"https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/TarifaDAC.aspx"

'''
import pandas as pd
solarPl =2797 #kw*h/yr

def allocation(type,solarP,cp):

    df=pd.read_excel('DB.xlsx')
    #cp=54670
    cp2=int(cp/1000)    
    row=(df[df.PC==cp2])
    typeR=row.iat[0,3]
    print ('Residential type: '+str(typeR))
    
    consumption=int(solarP)/12
    print('Monthly consumption:  '+str(consumption)+' kw*h/monthly')
    
    if type=='residential':
        energyP=residential(typeR,consumption)
        return(energyP)
    elif type=='industrial':
        energyP=industrial(consumption)
        return(energyP)
    elif    type=='business':
        energyP=business(consumption)
        return(energyP)
    
        
    

def residential(typeR,consumption):    
    df=pd.read_excel('DB.xlsx','ResidentialPrices')    
    row=(df[df.Type==typeR])
    basicConsumption=row.iat[0,1] #[$/kwh]
    intermediateConsumption=row.iat[0,2] #[$/kwh]
    extraConsumption=row.iat[0,3] #[$/kwh]
    firstLimit=row.iat[0,4] #[kwh]
    secondLimit=row.iat[0,5] #[kwh]        
    
    
    if 0 <= consumption < (firstLimit):
        print('first interval')
        totalPrice=consumption*basicConsumption #$
        
        
    elif firstLimit <= consumption < (firstLimit+secondLimit):
        print ('second interval')
        totalPrice=firstLimit*basicConsumption + (consumption-(firstLimit))*intermediateConsumption
    else:
        print ('third interval')
        totalPrice=firstLimit*basicConsumption+secondLimit*intermediateConsumption+ ((consumption-(firstLimit+secondLimit))*extraConsumption)
    unitPrice=totalPrice/consumption  #$/kwh
   
    return(unitPrice)
    #print ('Unit price: '+str(unitPrice)+'$/kwh')
    
    
    
    '''
    if typeR=='AA':
        print('AA')
    elif typeR =='A':
        print('A')    
    elif typeR =='B':
        print('B')
    elif typeR=='C':
        print('C')
    elif typeR=='D':
        print('D')
    elif typeR=='E':
        print('E')
    elif typeR=='F':
        print('F')   
    
    one=int(250) #limit in kwh
    a=int(300) #limit in kwh
    b=int(400) #limit in kwh
    c=int(850)
    d=1000 #limit in kwh
    e=2000 #limit in kwh
    f=2500 #limit in kwh
    energyP=0.147 # USD/kwh
    return(energyP)
    
    if 0 <= consumption <= one:
        print('tarifa one')  
    elif one < consumption <=a:
        print('tarifa a')
    elif a < consumption <=b:
        print('tarifa b')
    elif b < consumption <=c:
        print('tarifa c')
    elif c < consumption <=d:
        print('tarifa d')
    elif d < consumption <=e:
        print('tarifa e')
    elif consumption > e: 
        print('tarifa f')
    '''

def industrial(consumption):
    print('industrial price')
    energyP=0.037895
    return(energyP)
    
def business(consumption):
    print ('Business price')
    energyP=0.147
    return(energyP)

#allocation('residential',solarPl)
