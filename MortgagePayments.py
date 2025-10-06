#Question 1: Mortgage Payment Calculator 
class MortgagePayment:
    def __init__(self, principal, interestrate, amortization_period):
        self.principal = principal
        self.interestrate = interestrate / 100 #Converts Percentage to Decimal 
        self.amortization_period = amortization_period
        #Convert Yearly Interest Rate to Monthly Interest Rate 
        self.monthlyinterestrate = (1 + self.interestrate /2) ** (1/6) - 1 #This gives Monthly Rate 
        #Convert Yearly Interest Rate to Semi-monthly Interest Rate
        self.semimonthlyinterestrate = (1 + self.interestrate / 2) ** (1/12) - 1 #This gives Semi-monthly Rate
        #Convert Yearly Interest Rate to Bi-weekly Interest Rate
        self.biweeklyinterestrate = (1 + self.interestrate / 2) ** (1/13) - 1 #This gives Bi-weekly Rate
        #Convert Yearly Interest Rate to Weekly Interest Rate 
        self.weeklyinterestrate = (1 + self.interestrate / 2) ** (1/26) - 1 #This gives Weekly Rate 
    def calculatepayments(self):
        Months= self.amortization_period * 12 #Gives us No. Monthly Payments 
        #Function to calculate payments using PVA Formula 
        def calculatepayments(monthlyinterestrate, Months):
            return self.principal / ((1 - (1 + monthlyinterestrate) ** (-Months))/monthlyinterestrate)
        #Calculate Monthly Payment 
        MonthlyPayment = calculatepayments(self.monthlyinterestrate,Months)
        #Calculate Semi-monthly Payment
        SemimonthlyPayment = calculatepayments(self.semimonthlyinterestrate,(Months * 2))
        #Calculate Bi-weekly Payment 
        BiweeklyPayment = calculatepayments(self.biweeklyinterestrate, (self.amortization_period * 26))
        #Calculate Weekly Payment 
        WeeklyPayment = calculatepayments(self.weeklyinterestrate, (self.amortization_period * 52))
        #Calculate Rapid Bi-weekly Payment
        RapidBiweeklyPayment = MonthlyPayment / 2
        #Calculate Rapid Weekly Payment 
        RapidWeeklyPayment = MonthlyPayment / 4
        return (MonthlyPayment, SemimonthlyPayment, BiweeklyPayment , WeeklyPayment, RapidBiweeklyPayment, RapidWeeklyPayment)
    
#Example Calculation 
principal = 100000
interestrate = 5.5
amortization_period = 25

mortgage_calculator = MortgagePayment(principal, interestrate, amortization_period)
payments = mortgage_calculator.calculatepayments()

#Print all the Payments in Tuple Format 
print(f"Monthly Payment: ${payments[0]:.2f}")
print(f"Semi-monthly Payment: ${payments[1]:.2f}")
print(f"Bi-weekly Payment: ${payments[2]:.2f}")
print(f"Weekly Payment: ${payments[3]:.2f}")
print(f"Rapid Bi-weekly Payment: ${payments[4]:.2f}")
print(f"Rapid Weekly Payment: ${payments[5]:.2f}")





    