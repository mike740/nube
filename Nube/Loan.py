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
quantityM=[]



def PlotLoan(numberOfPaymentsM,aInterestM,aPrincipalM,balanceM,quantity):
    plt.figure(1)
    for i in (numberOfPaymentsM):
        quantityM.append(quantity)
    plt.title("Interest vs Balance in a PV project", fontsize=20)
    plt.plot(numberOfPaymentsM[1:],aInterestM[1:],label="Cumulative interest")
    plt.plot(numberOfPaymentsM,balanceM,label="Balance")
    plt.xlabel('Time [months]',fontsize=18)
    plt.ylabel('Cumulative Interest [USD]',fontsize=18)
    plt.yticks([0,2000,4000,6000,8000,10000,12000],['0','2,000$','4,000$','6,000$','8,000$','10,000$','12,000$'],fontsize=18)
    plt.rc('xtick',labelsize=15)
    plt.rc('ytick',labelsize=15)



    plt.grid()
    plt.legend(['Interest','Balance'],loc=9,shadow=True)

    
    #plt.hlines(y=10000, xmin=0, xmax=300, linewidth=2, color='r')

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

    PlotLoan(numberOfPaymentsM,aInterestM,aPrincipalM,balanceM,quantity)         
    Mycsv2(periods)
    
    return (monthlyInstallmentM)
    
    

     
