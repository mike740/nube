'''
Created on Jun 27, 2018

@author: Miguel RT
implement irradiation distribution to generation

'''
#Calculate ROI
#check tax benefits
#Add minimum fees

from click._compat import raw_input
from Loan import principalM, monthlyInstallmentM
import matplotlib.ticker as mtick


import matplotlib.pyplot as plt         
import numpy as np
import SolarProductionN
import csv  
import datetime
import EnergyPriceN
import Loan
import ExchangeRate
import Distribution

# Inputs

# Ratio of KWp by area [KWP/m2], value obtained from the manufacturer technical sheet
wp=0.145 # ratio in [kwp/m2]

#Area of the solar panels in [m2]
area=100 #m2
#postal code
#cp=int(raw_input("What is your postal code??"))
cp=44670
#Exchange rate

exchangeRate=ExchangeRate.exchange() #[mxn/usd]
now=datetime.datetime.now()
day=now.strftime
#print (now.strftime("%Y-%m-%d %H:%M"))
print (' Exhange rate: ', str(exchangeRate)+' mxn/usd')
#solar production year estimate_bandwidth    kw*h/yr
irradiationMean=SolarProductionN.myfunc(wp,cp)
#solarP=SolarProductionN.myfunc(wp,cp)*area*wp
solarP=irradiationMean*area*wp
irradiationDistribution=Distribution.distribution(irradiationMean) #irradiation distribution by month [kwh/hwp/year]
print('irradiation distribution: '+str(irradiationDistribution)+'kwh/kwp/yr.')
print('Anual solar output:  '+str(solarP)+' kw*h/yr') 

#Total cost of install  $
#iInv=15265
#print(area*wp)
if (area*wp)<4:
    iInv=area*wp*1840*1.4
    print('menor a 4')
elif (area*wp)>4 and (area*wp) < 10:
    iInv=area*wp*1509*1.4
    print('entre 4 y 10')
else:
    iInv=area*wp*1153*1.4
    print('mayor a 10')
print('inivital investment:  '+str(iInv)+' $ USD')

#Discount rate
dRate=0.0772
dRateM=(1+dRate)**(1/12)-1
dRate2=0.115
dRateM2=(1+dRate2)**(1/12)-1
print (dRateM)
#number of months
months=12*25

'''
#Tax benefits
taxBenefit=int(raw_input('Type the percentage of tax benefit'))/100
iInv=(1-taxBenefit)*iInv
'''
#Loan
#percentageLoan= int(raw_input('Percentage of borrowed from the initial investment'))/100
percentageLoan=0.5
installment= Loan.loan(dRateM2,months,percentageLoan*iInv)   


#Energy price per [$/KW*h]  Type of user
#type=raw_input('Enter type of user:residential,industrial or business')

energyP=EnergyPriceN.allocation('residential', solarP, cp)*float(exchangeRate)
print ('Unit price:'+str(energyP)+' $/kwh')
#energyP=0.147
#energyP=2.6811

#electricity price increase per year    1/yr
electricityI=0.02

#solar panel yearly degradation 1/yr
panelD=0.005


#Minimum fees $/month
minimumFee=5


#Cash flow model
vTime=[] 
vTimeY=[]
mEProduction=[]
mEProduction.append(0)
mdistribution=[]
mdistribution.append(0)
vDegradation=[]
vDegradation.append(0)
eGeneration=[]
eGeneration.append(0)
MinFees=[]
MinFees.append(0)
cashFlow=[]
cashFlowY=[]
netCashFlow=[]
netCashFlowY=[]
cashFlow.append(-iInv)
netCashFlow.append(-iInv)

#Columns:Time interval[month]
for i in range(months+1):
    vTime.append(i)
    
#Columns: Monthly energy production[kw*h],Degradation[%],Energy generation by month[kw*h], minimum fee [usd/month], Cash flow [usd/month], netcashflow [usd/month]
for i in range(1,months+1):
    j=i%12
    if j==0:
        j=12
    #print ('j es igual    '+str(j))
    mProduction=round(solarP/12,7) # delete round
    mEProduction.append(mProduction)
    mProductionD=float(irradiationDistribution[j-1])*area*wp 
    mdistribution.append(mProductionD)
    
    
    
    degradation=round(i*panelD/12,7) 
    vDegradation.append(degradation)
    
    generation=round(mProductionD*(1-degradation),7) # takes into account the distributed energy
    eGeneration.append(generation)
    
    MinFees.append(minimumFee)
    
    
    cash=round(generation*energyP*(1+i*electricityI/(12)),7)-minimumFee-Loan.monthlyInstallmentM[i]# aqui esta el peine
    cashFlow.append(cash)
    
    net=round(sum(cashFlow),3)
    netCashFlow.append(net)
    
   

# Output Parameters

#print(cashFlow)

# from months to years #optimize algorithm
years=int(months/12)
for i in range(years):
    vTimeY.append(i+1)
    sum=0
    add=0
    #k=i+1
    for j in range(12):
        #print (j)
        position=j+i*12+1
        #print(position)
        sum=sum+netCashFlow[position]
        add=add+cashFlow[position]
         
    if i==0:
        sum2=sum-iInv
        netCashFlowY.append(sum2)
        add2=add-iInv
        cashFlowY.append(add2)
    else:
        netCashFlowY.append(sum)
        cashFlowY.append(add)



irr=np.irr(cashFlow)
print('IRR: %s '%irr)
irrY=np.irr(cashFlowY)
print('IRR Year: %s '%irrY)


#presentValue=np.npv(dRateM,netCashFlow) # is it net cash flow???
presentValue=np.npv(dRateM,cashFlow)
print('Net Present value: '+str(presentValue))


#print(netCashFlow)
#print(netCashFlowY)


presentM=[]
timeP=[]
for i in range(0,30):
    x=(i+1)/100
    timeP.append(x)
    #present=np.npv(x,netCashFlowY)
    present=np.npv(x,cashFlowY)
    presentM.append(present)
#print(presentM)
    

#----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV----CSV
with open('mycsv.csv','w',newline='') as f:
    #fieldnames=['Period','Monthly energy production','Panel degradation','Energy generation','Minimum Fees','Cashflow','Net cashflow']
    fieldnames=['Period','Monthly energy production','Distributed Monthly energy production','Panel degradation','Energy generation','Minimum Fees','Monthly installment','Cashflow','Net cashflow']
    thewriter=csv.DictWriter(f ,fieldnames=fieldnames)
    
    thewriter.writeheader()
    #thewriter.writerow({'column 1':'juan','column2':'ale','column 3':'raquel'})
    for i in range(len(vTime)):
        period= vTime[i]
        pro= mEProduction[i]
        dis=mdistribution[i]
        deg= vDegradation[i]
        gen= eGeneration[i]
        fee=MinFees[i]
        mon=monthlyInstallmentM[i]
        cas= cashFlow[i]
        net= netCashFlow[i]
        
        thewriter.writerow({'Period':period, 'Monthly energy production':pro,'Distributed Monthly energy production':dis,'Panel degradation': deg,'Energy generation': gen,'Minimum Fees':fee,'Monthly installment':mon,'Cashflow':cas,'Net cashflow':net})
        

#----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots

area2=200
k=area/area2
case2=[i *k for i in netCashFlowY]



grafica=plt.figure(2)
ax=grafica.add_subplot(421)
ax.bar(vTimeY,netCashFlowY,color=(1.0,0.5,0.62))
ax.set_ylabel('Revenues [USD]')
ax.set_xlabel('Years',fontsize=14)
ax.set_title('Cash flow solar panels 25 years',fontsize=18)
ax.grid(color='b', linestyle='-', linewidth=0.1)
fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick) 
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)


ax=grafica.add_subplot(422)
ax.plot(vTime,netCashFlow)
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
ax.set_ylabel('Revenues [USD]')
ax.set_xlabel('Months')
ax.set_title('Break even point project 1',fontsize=18)
ax.grid(color='b', linestyle='-', linewidth=0.1)
fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick) 


plt.axhline(linewidth=1, color='r')



ax=grafica.add_subplot(425)
ax.plot(vTimeY,netCashFlowY,'g',vTimeY,case2,'r')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
#ax.set_xticks(ax.get_xticks()[::1])# number of times the x axis is divided
ax.set_ylabel('Cash flow [USD]')
ax.set_xlabel('Years')
ax.set_title('Revenue of two projects',fontsize=18)
ax.grid(color='b', linestyle='-', linewidth=0.1)
p1=str(area)+' m2 project '
p2=str(area2)+' m2 project'
ax.legend([p1,p2])
fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick) 




ax=grafica.add_subplot(426)
ax.plot(timeP,presentM)
#ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

ax.set_ylabel('NPV [USD]')
ax.set_xlabel('Discount rate')
ax.set_title('IRR project '+p1,fontsize=18)
ax.grid(color='b', linestyle='-', linewidth=0.1)
plt.axhline(linewidth=1, color='r')
plt.tight_layout()
fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick) 




plt.figure(3)
plt.plot(vTime[1:13],cashFlow[1:13],'r-.')
plt.bar(vTime[1:13],cashFlow[1:13])
plt.ylim(0,max(vTime)*1.15)
plt.grid()
plt.xlabel('Time[months]',fontsize=20)
plt.ylabel('Cash flow [USD]',fontsize=20)
plt.yticks([0,50,100,150,200,250,300],[0,'50$','100$','150$','200$','250$','300$'])
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],fontsize=15)
plt.yticks(fontsize=15)
plt.title("Cash flow of the first year", fontsize=20)


plt.show()



