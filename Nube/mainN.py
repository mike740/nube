#Calculate ROI
#Indicate the number of solar panels and inverters
from click._compat import raw_input


'''
Created on Jun 27, 2018

@author: Miguel RT
'''
import matplotlib.pyplot as plt         
import numpy as np
import SolarProductionN
import csv  
import EnergyPriceN
import Loan

# Inputs

# Ratio of KWp by area [KWP/m2], value obtained from the manufacturer technical sheet
wp=0.145 # ratio in [kwp/m2]

#Area of the solar panels in [m2]
area=100 #m2
#solar production year estimate_bandwidth    kw*h/yr
solarP=SolarProductionN.myfunc(wp)*area*wp
print('Anual solar output:  '+str(solarP)+' kw*h/yr') 
# Tax reduction



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
print (dRateM)
#number of months
months=12*25
#Loan
percentageLoan= int(raw_input('Percentage of borrowed from the initial investment'))/100
loan= Loan.loan(dRateM,months,percentageLoan*iInv)   


#Energy price per $/KW*h  Type of user
#type=raw_input('Enter type of user:residential,industrial or business')
#energyP=EnergyPrice.allocation(type,solarP)
energyP=0.147

#electricity price increase per year    1/yr
electricityI=0.02

#solar panel yearly degradation 1/yr
panelD=0.005


#Minimum fees $/month
minimumFee=0



#Cash flow model
vTime=[] 
vTimeY=[]

mEProduction=[]
mEProduction.append(0)
vDegradation=[]
vDegradation.append(0)
eGeneration=[]
eGeneration.append(0)
MinFees=[]
MinFees.append(9)
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
    
    mProduction=round(solarP/12,7) # delete round
    mEProduction.append(mProduction)
    
    degradation=round(i*panelD/12,7) # delete round ???
    vDegradation.append(degradation)
    
    generation=round(mProduction*(1-degradation),7)# 
    eGeneration.append(generation)
    
    MinFees.append(minimumFee)
    
    #cash=round(generation*energyP*(1+i*electricityI/(100*12)),3) # aqui esta el peine
    cash=round(generation*energyP*(1+i*electricityI/(12)),7)-minimumFee # aqui esta el peine
    cashFlow.append(cash)
    
    net=round(sum(cashFlow),3)
    netCashFlow.append(net)
    
   
    
    
# Output Parameters

#print(cashFlow)

# from months to years
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


presentValue=np.npv(dRateM,netCashFlow)
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
    fieldnames=['Period','Monthly energy production','Panel degradation','Energy generation','Minimum Fees','Cashflow','Net cashflow']
    thewriter=csv.DictWriter(f ,fieldnames=fieldnames)
    
    thewriter.writeheader()
    #thewriter.writerow({'column 1':'juan','column2':'ale','column 3':'raquel'})
    for i in range(len(vTime)):
        period= vTime[i]
        pro= mEProduction[i]
        deg= vDegradation[i]
        gen= eGeneration[i]
        cas= cashFlow[i]
        net= netCashFlow[i]
        fee=MinFees[i]
        thewriter.writerow({'Period':period, 'Monthly energy production':pro,'Panel degradation': deg,'Energy generation': gen,'Minimum Fees':fee,'Cashflow':cas,'Net cashflow':net})
        

#----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots----Plots


area2=200
k=area/area2
case2=[i *k for i in netCashFlowY]



grafica=plt.figure(1)
ax=grafica.add_subplot(421)
ax.bar(vTimeY,netCashFlowY,color=(1.0,0.5,0.62))
ax.set_ylabel('Cash flow')
ax.set_xlabel('Years')
ax.set_title('Cash flow solar panels 25 years')
ax.grid(color='b', linestyle='-', linewidth=0.1)


ax=grafica.add_subplot(422)
ax.plot(vTime,netCashFlow)
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
ax.set_ylabel('Cash flow')
ax.set_xlabel('Months')
ax.set_title('Break even point project 1')
ax.grid(color='b', linestyle='-', linewidth=0.1)

plt.axhline(linewidth=1, color='r')



ax=grafica.add_subplot(425)
ax.plot(vTimeY,netCashFlowY,'g',vTimeY,case2,'r')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
#ax.set_xticks(ax.get_xticks()[::1])# number of times the x axis is divided
ax.set_ylabel('Cash flow')
ax.set_xlabel('Years')
ax.set_title('Revenue of two projects')
ax.grid(color='b', linestyle='-', linewidth=0.1)
p1=str(area)+' m2 project '
p2=str(area2)+' m2 project'
ax.legend([p1,p2])


ax=grafica.add_subplot(426)
ax.plot(timeP,presentM)
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
#ax.set_xticks(ax.get_xticks()[::1])# number of times the x axis is divided
ax.set_ylabel('Cash flow')
ax.set_xlabel('Discount rate')
ax.set_title('IRR project '+p1)
ax.grid(color='b', linestyle='-', linewidth=0.1)
plt.axhline(linewidth=1, color='r')
plt.show()

'''
plt.figure(1)



plt.subplot(3,1,1)
plt.plot(vTime[1:300],eGeneration[1:300])
plt.ylim((0, max(eGeneration)*1.1))
plt.ylabel('Energy Kw*h')
plt.xlabel('months')
plt.title('Energy Generation')

plt.subplot(3,1,3)
plt.plot(vTime[1:12],eGeneration[1:12])
plt.ylabel('Energy Kw*h')
plt.xlabel('months')
plt.title('First year of energy generation')



plt.show()

    '''
    
    


