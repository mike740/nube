import pandas as pd
from click._compat import raw_input

def myfunc(wp,cp):
    
    df=pd.read_excel('DB.xlsx')
    #wp=0.145 # ratio in [kwp/m2]
    #cp=int(raw_input("What is your postal code??"))
    #cp=44670
    cp2=int(cp/1000)

    
    row=(df[df.PC==cp2])
    print("               ")
    print(row)

    ratio=row.iat[0,2]
    print("               ")
    #print(ratio)
    
    return ratio # The ratio is in Kwh/kwp





#https://www.youtube.com/watch?v=2AFGPdNn4FM