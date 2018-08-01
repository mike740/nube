'''
Created on Jul 31, 2018

@author: Miguel RT
Source of information:"https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/TarifaDAC.aspx"

'''

def allocation(type,solarP):
    
    print (solarP)
    consumption=int(solarP)/12
    
    print('alloc')
    if type=='residential':
        residential(type,consumption)
    elif type=='industrial':
        industrial(type,consumption)
    elif    type=='business':
        business(type,consumption)
    

def residential(type,consumption):    
    print ('Residential price')
    one=int(250) #limit in kwh
    a=int(300) #limit in kwh
    b=int(400) #limit in kwh
    c=int(850)
    d=1000 #limit in kwh
    e=2000 #limit in kwh
    f=2500 #limit in kwh
    energyP=0.147 # USD/kwh
    return(energyP)
    '''
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

def industrial(type,consumption):
    print('industrial price')
    energyP=0.037895
    return(energyP)
    
def business(type,consumption):
    print ('Business price')
    energyP=0.147
    return(energyP)
