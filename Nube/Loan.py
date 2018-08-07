import numpy as np
import csv
import matplotlib.pyplot as plt



numberOfPaymentsM=[] #number of the months
monthlyInstallmentM=[] # money to pay per month [$usd]
interestM=[] # interest to pay per month [$usd]
aInterestM=[] #Cumulative interest to pay per month [$usd]
principalM=[] # Principal matrix [$usd]
aPrincipalM=[] # Cumulative Principal matrix [$usd]
balanceM=[] #balance per month [$USD]



def PlotLoan(numberOfPaymentsM,aInterestM,aPrincipalM,balanceM):
    plt.figure(1)
    plt.plot(numberOfPaymentsM,balanceM,'r',numberOfPaymentsM,aInterestM,'b',numberOfPaymentsM,aPrincipalM,'g')
   # plt.show()
    

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
    aInterestM.append(0)
    aPrincipalM.append(0)
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
        acumi=sum(interestM)
        aInterestM.append(acumi)
        aprin=sum(principalM)
        aPrincipalM.append(aprin)

    PlotLoan(numberOfPaymentsM,aInterestM,aPrincipalM,balanceM)         
    Mycsv2(periods)
    
    return (monthlyInstallmentM)
    
    

     
