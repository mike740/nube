import numpy as np
import csv

a=0.015 # rate of interest per period
b=24 # number of compounding periods
c=200000 # money borrowed at present value

numberOfPaymentsM=[] #number of the months
monthlyInstallmentM=[] # money to pay per month [$usd]
interestM=[] # interest to pay per month [$usd]
principalM=[]
balanceM=[]



def Mycsv2(periods):
    
    with open('Loan.csv','w',newline='') as f:
        fieldnames=['Number of payments','Monthly installment','Interest','Principal','Balance']
        #fieldnames=['Period','Monthly energy production','Panel degradation','Energy generation','Minimum Fees','Cashflow','Net cashflow']
        thewriter=csv.DictWriter(f ,fieldnames=fieldnames)
        thewriter.writeheader()
        
        for i in range (periods+1):
            number=numberOfPaymentsM[i]
            installment=monthlyInstallmentM[i]
            interest=interestM[i]
            principal=principalM[i]
            balance=balanceM[i]
            thewriter.writerow({'Number of payments':number,'Monthly installment':installment,'Interest':interest,'Principal':principal,'Balance':balance})           
            #thewriter.writerow({'Period':period, 'Monthly energy production':pro,'Panel degradation': deg,'Energy generation': gen,'Minimum Fees':fee,'Cashflow':cas,'Net cashflow':net})

def loan(rate,periods,quantity):
    installment = np.pmt(rate,periods,-quantity) # monthly installment
    numberOfPaymentsM.append(0)
    monthlyInstallmentM.append(0)
    interestM.append(0)
    principalM.append(0)
    balanceM.append(quantity)
    
    for i in range(1,periods+1):
        numberOfPaymentsM.append(i)
        monthlyInstallmentM.append(installment)
        interest=balanceM[i-1]*rate
        interestM.append(interest)
        principal=monthlyInstallmentM[i]-interestM[i]
        principalM.append(principal)
        balance=balanceM[i-1]-principalM[i]
        balanceM.append(balance) 
    Mycsv2(periods)

#loan(a,b,c)    

     
