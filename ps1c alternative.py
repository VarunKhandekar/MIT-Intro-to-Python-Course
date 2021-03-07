# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 12:19:04 2021

@author: Varun
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:35:50 2021

@author: Varun
Code to determine the appropriate income % to save for the downpayment
"""

import math
import numpy
import pylab

total_cost = float(input("Input the house price: "))
ann_salary = float(input("Type salary: "))
ann_rate_of_return = float(input("Type expected rate of return on savings: "))
perc_downpayment = float(input("Type downpayment as a proportion of house price: "))
semi_annual_salary_raise = float(input("Type semi-annual salary raise: "))
desired_months = float(input("Type the number of months you want save for the downpayment in: "))

# downpayment required
downpayment_required = total_cost*perc_downpayment

# monthly rate of return
monthly_rate_of_return = ann_rate_of_return/12

# initialise values
current_savings = 0.0
#initial lower bound
LowerBound = 0
#initial upper bound
UpperBound = 10000
#initialise old mid bound; needed to exit if not possible to solve the problem
oldMidB = 0

#initial steps
steps = 0

#we need to initialise values within this loop for testing during this iterative process
#they must be initialised before each test
while abs(current_savings - downpayment_required)>100:
    MidB = int(round((UpperBound+LowerBound)/2))
    portion_saved = MidB/10000
    months = 0.0
    current_savings = 0.0
    salary = ann_salary
    while months < desired_months:
        monthly_salary = salary/12
        monthly_saved = monthly_salary*portion_saved
    
        #base case
        if months == 0.0:
            #count the number of months
            months += 1
    
            # add the amount saved this period + interest earned from what we previously had saved
            current_savings += current_savings*monthly_rate_of_return
            current_savings += monthly_saved
    
        #when we have reached a 6 month period
        elif months%6 == 0.0:
            #count the number of months
            months += 1
        
            #increase salary
            salary += salary*semi_annual_salary_raise
        
            # add the amount saved this period + interest earned from what we previously had saved
            current_savings += current_savings*monthly_rate_of_return
            current_savings += monthly_saved
    
        #all other cases
        else:
            #count the number of months
            months += 1
    
            # add the amount saved this period + interest earned from what we previously had saved
            current_savings += current_savings*monthly_rate_of_return
            current_savings += monthly_saved
    
    if abs(current_savings-downpayment_required) <= 100:
        print("best amount of income to save on a monthly basis =" , portion_saved*100, "%")
        print("steps in bisection search =", steps)
        break
    if MidB == oldMidB:
        print("It is not possible to save for the downpayment in desired number of months")
        break    
    
    oldMidB = MidB
    
    if current_savings - downpayment_required < 0:
        LowerBound = MidB
    else:
        UpperBound = MidB
    steps += 1



#this has been added as for some reason the print wasn't working in the LB and UB sections of the above while loop
if abs(current_savings-downpayment_required) <= 100:
   print("best amount of income to save on a monthly basis =" , portion_saved*100, "%")
   print("steps in bisection search =", steps)     