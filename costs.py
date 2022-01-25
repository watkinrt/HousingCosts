def mortgage(r, L, n=30):
    """ Monthly mortgage payment
        
    Inputs
    ------
    r: float > 0
        Unitless yearly interest rate (i.e., not as a percent)
    L: float > 0
        Loan amount
    n: loan term in years (default at 30 years)
    
    Output
    ------
    monlyth mortgage payment
    
    """
    # Calculate monthly payment cost
    # http://www.intmath.com/money-math/3-math-of-house-buying.php
    return (L*r/12.)/(1-(1+r/12.)**(-n*12))

def interestComparison(r1, r2, L, n=30):
    """ Total cost comparison for 2 different interest rates 
    
    Inputs
    ---------
    r1, r2: float > 0
        Unitless yearly interest rate (i.e., not as a percent)
    L: float > 0
        Loan amount
    n: loan term in years (default at 30 years)
    
    Output
    ------
    Prints a cost comparison between the 2 rates
    
    """
    
    # Calculate monthly mortgage costs for each rate
    m1 = mortgage(r1, L, n)
    m2 = mortgage(r2, L, n)
    
    # Print comparison
    print(f"Monthly mortgage {r1*100:,.3f}%: ${m1:,.0f}")
    print(f"Monthly mortgage {r2*100:,.3f}%: ${m2:,.0f}")
    print(f"Mortgage difference: ${m2-m1:,.0f}")
    print(f"Total difference over 5 years: ${(m2-m1)*5*12:,.0f}")
    print(f"Total difference over 10 years: ${(m2-m1)*10*12:,.0f}")
    print(f"Total difference over loan term: ${(m2-m1)*n*12:,.0f}")
    
def cost(houseCost=500000., loanInterestRate=0.033, taxRate=0.00793, 
         downpayment=0.2, loanTerm=30, 
         mortgageInsurance=0.0075, mortgateInsuranceYears=None,
         hoa=0., size=2000., monthlyRent=2100,
         yearlyHomeInsurance=1800, yearlyEarthquakeInsurance=1200,
         inflation=0.03):
    """ Cost breakdown for mortgage 
    
    Inputs
    ------
    houseCost: float > 0 (default: $500k)
        Cost of the house.
    loanInterestRate: float > 0 (default: 0.033)
        Yearly interest rate on the mortgage (as a unitless number rather than a percentage)
    taxRate: float >= 0 (default: 0.00793)
        Yearly property tax rate (as a unitless number rather than a percentage)
    downpayment: 0 < float < 1 or float > 1 (default: 0.2)
        Downpayment amount. If between 0 and 1, assumed to be a percent of the house 
        cost as a unitless number (rather than a percentage). If greater than 1, 
        assumed to be a dollar amount.
    loanTerm: float > 0 (default: 30)
        Loan term in years.
    mortgageInsurance: 0 < float < 1 or float > 1 (default: 0.0075)
        Morgate insureance. If between 0 and 1, assumed to be a percent of the house cost as a unitless number 
        (rather than a percentage). If greater than 1, assumed to be a monthly dollar amount.
    mortgageInsurfaceYears: None or float > 0 (default: None)
        Number of years that mortgage Insurance is required. If not specified, this is calculated
        automatically.
    hoa: float >= 0 (default: 0)
        Montlhy HOA fees
    size: float > 0 (default: 2000)
        House square footage. This number is used to estimate house upkeep costs.
    monthlyRent: float >= 0 (default: 2100)
        Currently montly rent cost. This is just used as a cost comparison point and can be set
        to zero if not relevant.
    yearlyHomeInsurance: float > 0 (default: 1800)
        Yearly cost of home owners insurance.
    yearlyEarthquakeInsurance: float >= 0 (default: 1200)
        Yearly cost for earthquake insurance 
    inflation: float >=0 (default: 0.03)
        Assumed inflation rate over the term of the loan as a unitless number (rather than a percentage)
    
    Output
    ------
    Printout of loan comparison details. Notes:
        - "Nonreturnable" corresponds to costs that you never see again; 
        for example, rent, taxes, nterest, upkeep, etc. These numbers help deconflate 
        the true value of your equity.
        - "Total" costs refer to the baseline cost plus additional nonreturnable costs.
        - Upkeep costs are estimated based 1$/ft^2 per year.
    
    """
    
    # Load term in months
    monthlyLoanTerm = loanTerm*12.
    
    # Calculate downpayment and modify remaining balance
    if downpayment < 1:
        downpayment = houseCost*downpayment
    remainingCost = houseCost - downpayment
    
    # In-depth closing costs
    # Based off of http://www.cardinalescrow.com/cpe/buyerseller-closing-costs/
    # closingCostsRough = closingCostRate*houseCost
    escrowFees = 2*houseCost*1e-3 + 550 + 150.
    if escrowFees < 795:
        escrowFees = 795.
    titleFees = 65 + 200 + 25 + 85 + 20 + 35
    morgateFees = houseCost*.01 + 800 + 60 + 700 + 700 + 150 + 500 +\
                    75 + 75 + 100
    closingCostsDetailed = escrowFees + titleFees + morgateFees
    
    # Calculate total payments at purchasing the house
    closingCosts = closingCostsDetailed
    initialPayment = downpayment + closingCosts
    
    # Calculate monthly payment cost
    # http://www.intmath.com/money-math/3-math-of-house-buying.php
    r = loanInterestRate/12.
    L = remainingCost
    n = monthlyLoanTerm
    monthlyMorgagePayment = (L*r)/(1-(1+r)**(-n))
    
    # Calculate tax payments
    yearlyTaxPayment = houseCost*taxRate
    monthlyTaxPayment = yearlyTaxPayment/12.
    
    # Calculate morgage insurance
    if downpayment < houseCost*.2:
        yearlyMorgageInsurancePayment = houseCost*mortgageInsurance
        monthlyMorgageInsurancePayment = yearlyMorgageInsurancePayment/12.
    else:
        yearlyMorgageInsurancePayment = 0.
        monthlyMorgageInsurancePayment = 0.
    
    # Calculate morgage insurance
    if mortgateInsuranceYears:
        # If a total number of years is specified to pay off, check accordingly
        check = lambda paid2principle, count: count < mortgateInsuranceYears*12
    elif yearlyMorgageInsurancePayment:
        # Otherwise, assume that you get PMI removed when you payed back 22% of the house cost
        check = lambda paid2principle, count: paid2principle+downpayment < houseCost*.22
    else:
        check = lambda paid2principle, count: False
    remainingCostTmp = remainingCost
    paid2principle = 0
    totalNonreturnPMI = 0
    count = 0
    while check(paid2principle, count) or count > 1000:
        incurredInterest = r*remainingCostTmp
        towardsPinciple = monthlyMorgagePayment - incurredInterest
#         print(monthlyMorgagePayment, incurredInterest)
        paid2principle += towardsPinciple
        remainingCostTmp -= towardsPinciple
        totalNonreturnPMI += monthlyMorgageInsurancePayment
        count += 1
#     while paid2principle+downpayment < houseCost*.2 or count > 1000:
#         incurredInterest = r*remainingCostTmp
#         towardsPinciple = monthlyMorgagePayment - incurredInterest
# #         print(monthlyMorgagePayment, incurredInterest)
#         paid2principle += towardsPinciple
#         remainingCostTmp -= towardsPinciple
#         totalNonreturnPMI += monthlyMorgageInsurancePayment
#         count += 1
    
    assert count < 1000, "Issues with total nonreturn PMI calculation"
    
    # Calculate home owners insurance
    monthlyInsurancePayment = yearlyHomeInsurance/12
    mountlyEarthquakeInsurance = yearlyEarthquakeInsurance/12.
    
    # Calculate up keep costs
    # Assume 1$/ft^2 per year
    yearlyUpkeepPayment = size
    monthlyUpkeepPayment = yearlyUpkeepPayment/12.
    
    # Calculate total monthly cost
    totalMonthlyPayment = monthlyMorgagePayment + monthlyTaxPayment + \
                monthlyMorgageInsurancePayment + monthlyInsurancePayment + \
                hoa + monthlyUpkeepPayment + mountlyEarthquakeInsurance
    totalPostMorgageMonthlyPayment = totalMonthlyPayment\
                                        - monthlyMorgagePayment\
                                        - monthlyMorgageInsurancePayment
    
    # Non returnable house costs
    totalNonreturnHouse = (totalMonthlyPayment-monthlyMorgageInsurancePayment)*monthlyLoanTerm\
                            - houseCost+closingCosts+totalNonreturnPMI
    
    # Non returnable apartment costs assuming 3% cost inflation
    totalInflatedNonreturnApartment = 0
    tmpMonthlyRent = monthlyRent
    for i in range(loanTerm):
        tmpMonthlyRent *= (1.+inflation)
        totalInflatedNonreturnApartment += tmpMonthlyRent*12
    totalNonreturnApartment = monthlyRent*monthlyLoanTerm
    
    
    # Print out results
    print("House cost: ${:,.0f}\n".format(houseCost) +
          f"20% Downpayment: ${0.2*houseCost:,.0f}\n" +
          f"Total morgage insurance cost: ${totalNonreturnPMI:,.0f} over {count/12:.1f} years\n" +
          f"Nonreturnable house cost: ${totalNonreturnHouse:,.0f}\n" +
          f"Inflated nonreturnable apartment cost: ${totalInflatedNonreturnApartment:,.0f}\n" +
          f"Nonreturnable apartment cost: ${totalNonreturnApartment:,.0f}\n" +
          f"Total house cost: ${totalNonreturnHouse+houseCost:,.0f}\n" +
           "Morgage details\n" +
           "  Morgage interest rate: {:,.1f}%\n".format(loanInterestRate*100.) +
           "  Loan term: {:,.0f} months\n".format(loanTerm) +
           "Initial costs: ${:,.0f}\n".format(initialPayment) +
           "  Downpayment = ${:,.0f}\n".format(downpayment) +
           "  Closing costs = ${:,.0f}\n".format(closingCosts) +
           "Monthly costs: ${:,.0f}\n".format(totalMonthlyPayment) +
           "  Morgage: ${:,.0f}\n".format(monthlyMorgagePayment) +
           "  Taxes: ${:,.0f}\n".format(monthlyTaxPayment) +
           "  Morgage insurance: ${:,.0f}\n".format(monthlyMorgageInsurancePayment) +
           "  Homeowners insurance: ${:,.0f}\n".format(monthlyInsurancePayment) + 
           "  Earthquake insurance: ${:,.0f}\n".format(mountlyEarthquakeInsurance) + 
           "  HOA fees: ${:,.0f}\n".format(hoa) +
           "  Upkeep costs: ${:,.0f}\n".format(monthlyUpkeepPayment) +
           f"Post-PMI monthly costs: ${totalMonthlyPayment-monthlyMorgageInsurancePayment:,.0f}\n"
           f"Post-morgage monthly costs: ${totalPostMorgageMonthlyPayment:,.0f}\n")