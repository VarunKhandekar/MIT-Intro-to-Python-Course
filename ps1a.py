# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:58:14 2021

@author: Varun

Code to calculate the number of months needed to make a downpayment for a home
"""
import math
import numpy
import pylab

total_cost = float(input("Input the house price: "))
ann_salary = float(input("Type salary: "))
ann_rate_of_return = float(input("Type expected rate of return on savings: "))                                                   
portion_saved = float(input("Type the expected % of income to be saved: "))
perc_downpayment = float(input("As a proportion of house price: "))



def number_of_months(total_cost, perc_downpayment, ann_salary, ann_rate_of_return, portion_saved):

    # downpayment required
    downpayment_required = total_cost*perc_downpayment

    monthly_salary = ann_salary/12

    # amount saved per month
    monthly_saved = monthly_salary*portion_saved

    # monthly rate of return
    monthly_rate_of_return = ann_rate_of_return/12
    # initialise values
    months = 0.0
    current_savings = 0.0

    while current_savings < downpayment_required:
        #count the number of months
        months += 1
    
        # add the amount saved this period + interest earned from what we previously had saved
        current_savings += current_savings+monthly_rate_of_return
        current_savings += monthly_saved

    return print(months)

number_of_months(total_cost, perc_downpayment, ann_salary, 
                     ann_rate_of_return, portion_saved)


 # downpayment required
downpayment_required = total_cost*perc_downpayment

monthly_salary = ann_salary/12

# amount saved per month
monthly_saved = monthly_salary*portion_saved

# monthly rate of return
monthly_rate_of_return = ann_rate_of_return/12
# initialise values
months = 0.0
current_savings = 0.0

while current_savings < downpayment_required:
#count the number of months
    months += 1
    
    # add the amount saved this period + interest earned from what we previously had saved
    current_savings += current_savings*monthly_rate_of_return
    current_savings += monthly_saved
print(months)


