# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:12:34 2021

@author: Varun

Code to calculate the number of months needed to make a downpayment for a home
This factors a 6m salary raise
"""

import math
import numpy
import pylab

total_cost = float(input("Input the house price: "))
ann_salary = float(input("Type salary: "))
ann_rate_of_return = float(input("Type expected rate of return on savings: "))                                                   
portion_saved = float(input("Type the expected % of income to be saved: "))
perc_downpayment = float(input("Type downpayment as a proportion of house price: "))
semi_annual_salary_raise = float(input("Type semi-annual salary raise: "))

# downpayment required
downpayment_required = total_cost*perc_downpayment

# monthly rate of return
monthly_rate_of_return = ann_rate_of_return/12

# initialise values
months = 0.0
current_savings = 0.0

while current_savings < downpayment_required:
    monthly_salary = ann_salary/12
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
        ann_salary += ann_salary*semi_annual_salary_raise
        
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
        
print(months)
