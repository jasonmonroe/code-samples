"""
jason@jasonmonroe.com
Copyright (c) 2025 Jason Monroe
April 23, 2025

Paycheck Calculator

This program calculates the paycheck for a week based on the hours worked each day.
Any work over 8 hours in a day considered overtime.  Any work over 12 hours in a day is considered double time.
Any work over 40 hours in a week is considered overtime.

@link www.opm.gov
@link https://www.dir.ca.gov/dlse/FAQ_Overtime.htm
@link https://www.irs.gov/filing/federal-income-tax-rates-and-brackets
"""

# Import Libraries
import lorem
import random

# Constants
# Threshold values for hours worked
MIN_HOURS_PER_DAY = 0
MAX_HOURS_PER_DAY = 24
STANDARD_HOURS_PER_DAY = 8
OVERTIME_HOURS_PER_DAY = 12
DOUBLE_TIME_HOURS_PER_DAY = 16
STANDARD_HOURS_PER_WK = 40
WEEKS_IN_YEAR = 52

# Pay rates by hours worked
STANDARD_RATE = 1.0
OVERTIME_RATE = 1.5
DOUBLE_TIME_RATE = 2.0
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# FICA Tax Rates
SS_RATE = 0.06
MEDICARE_RATE = 0.0145
CA_DISABILITY_RATE = 0.012

# California Minimum Wage
min_pay_rate = 1.00 #16.50

# Total number of hours worked in a day and week.
hours_in_week = 0

# Determines whether a worker will be paid double-time.
double_time = None

# Paycheck that will be generated for the week.
paycheck = []

# Total pay of worker in a week.
gross_pay = 0.0

def show_banner():
    print("=" * 27)
    print(" CALIFORNIA PAY CALCULATOR ")
    print("=" * 27)

# Create a random company name.
def company_name():
    word_cnt = random.randint(1, 3)
    words = lorem.text().split()
    return ' '.join(words[:word_cnt]) + ", Inc."

# 2025 Federal Tax Rates
def get_federal_tax_rates():
    return [
        (0.10, 11925),
        (0.12, 48475),
        (0.22, 103350),
        (0.24, 197300),
        (0.32, 250525),
        (0.35, 626350),
        (0.37, float("inf"))
    ]

# 2025 California State Tax Rates
def get_state_tax_rates():
    return [
        (0.01, 10099),
        (0.02, 23942),
        (0.04, 37788),
        (0.06, 52455),
        (0.08, 66295),
        (0.093, 338639),
        (0.103, 406364),
        (0.113, 677275),
        (0.123, 1000000),
        (0.133, float("inf"))
    ]

# Prompt for hourly pay rate
def prompt_pay_rate() -> float:
    input_value = input("Enter your pay rate in USD: $")
    
    if input_value == "":
        return 0.0
    
    pay_rate = float(input_value)

    if pay_rate < min_pay_rate:
        print(f"California minimum wage is {min_pay_rate:2f}.  Please raise your pay rate.")

        if pay_rate <= 0.0:
            print("Invalid input. Please enter a positive number.")

        return prompt_pay_rate()

    return pay_rate

# Total number of hours worked in a day and week.
def prompt_day_hours() -> float:
    input_value = input(f"Enter hours worked on {day}: ")
    
    if input_value == "":
        return 0.0
    
    hours_input = float(input_value)

    while hours_input < MIN_HOURS_PER_DAY or hours_input > MAX_HOURS_PER_DAY:
        print(f"Invalid input. Please enter a number between {MIN_HOURS_PER_DAY} and {MAX_HOURS_PER_DAY}.")
        hours_input = float(input(f"Enter hours worked on {day}: "))

    return hours_input

# Function to check if the hours worked in a day are overtime or double time.
def check_double_time(day_str: str):
    if hours_in_day == 0:
        print("\tNo hours worked today.")
        return False
        
    if day_str == "Sunday" and double_time is None and hours_in_day > STANDARD_HOURS_PER_DAY:
        print("\tDouble time flag!")
        return True

    return None

def calc_standard_pay() -> float:
    return standard_hours * STANDARD_RATE * pay_rate

def calc_overtime_pay() -> float:
    return overtime_hours * OVERTIME_RATE * pay_rate

def calc_double_time_pay() -> float:
    return double_time_hours * DOUBLE_TIME_RATE * pay_rate

# Calculate the deductions for federal, state, FICA, and disability taxes.
def calc_deductions(gross: float) -> dict:
    federal = calc_federal_tax(gross)
    state = calc_state_tax(gross)
    fica = calc_fica_tax(gross)
    ss = fica["ss"]
    medicare = fica["medicare"]
    disability = gross * CA_DISABILITY_RATE
    net = gross - (federal + state + ss + medicare + disability)
    
    return {
        "gross": gross,
        "federal": federal,
        "state": state,
        "ss": ss,
        "medicare": medicare,
        "disability": disability,
        "net": net
    }

# Calculate federal and state taxes.
def calc_tax(gross: float, rates: list) -> float:
    projected_gross_yr = gross * WEEKS_IN_YEAR
    print("\tProjected gross income for the year:", projected_gross_yr)
    amount = 0.0
    prev_limit = None

    for rate, limit in rates:
        if projected_gross_yr >= limit:
            if prev_limit is None:
                prev_limit = limit
                amount += limit * rate
            else:
                amount += (limit - prev_limit) * rate
        else:
            # Calculate the remaining amount then break loop.
            gross_rem = projected_gross_yr - prev_limit
            amount += gross_rem * rate
            break

    amount /= WEEKS_IN_YEAR
    return amount

# Assume the weekly amount is the annual amount to calculate the federal tax.
def calc_federal_tax(gross: float) -> float:
    return calc_tax(gross, get_federal_tax_rates())

# Calculate the state tax amount.
def calc_state_tax(gross: float) -> float:
    return calc_tax(gross, get_state_tax_rates())

# Calculate the FICA tax amount.
def calc_fica_tax(gross: float) -> dict:
    ss = gross * SS_RATE
    medicare = gross * MEDICARE_RATE
    
    return {"ss": ss, "medicare": medicare}

# Display the weekly result summary.
def show_paycheck():

    deductions = calc_deductions(gross_pay)
    federal = deductions["federal"]
    state = deductions["state"]
    ss = deductions["ss"]
    medicare = deductions["medicare"]
    disability = deductions["disability"]
    net_pay = deductions["net"]
    effective_rate = (1 - (net_pay / gross_pay))

    print("\n")
    print("=" * 28)
    print(" CA Weekly Paycheck Summary")
    print(f" {company_name()}")
    print("=" * 28)

    print(f"Pay Rate: ${pay_rate:.2f}")
    print(f"Hours Worked: {hours_in_week}")
    print(f"Gross Pay: ${gross_pay:.2f}\n")

    print("Deductions")
    print(f"Effective Rate: {effective_rate:.2%}")
    print(f"Federal Tax: -${federal:.2f}")
    print(f"State Tax: -${state:.2f}")
    print(f"Disability Tax: -${disability:.2f}")

    print("\nFICA")
    print(f"SS Tax: ${ss:.2f}")
    print(f"Medicare Tax: ${medicare:.2f}\n")

    print(f"Net Pay: ${net_pay:.2f}\n")
    
    print("-" * 67)
    print(" Day\t| Hours Worked || Standard | Overtime | Double Time || Pay")
    print("-" * 67)

    for day_hours in paycheck:
        day_str = day_hours["day"]
        hours_worked = day_hours["hours_worked"]
        day_standard_hours = day_hours["hours"]["standard_hours"]
        day_overtime_hours = day_hours["hours"]["overtime_hours"]
        day_double_time_hours = day_hours["hours"]["double_time_hours"]
        day_gross_pay = day_hours["pay"]

        print(f"{day_str} | {hours_worked}\t\t|| {day_standard_hours}\t\t| {day_overtime_hours}\t| {day_double_time_hours}\t|| ${day_gross_pay:.2f}")

    print("\n")

# Beginning of the program
show_banner()
pay_rate = prompt_pay_rate()

for day in WEEKDAYS:

    standard_hours = 0
    overtime_hours = 0
    double_time_hours = 0

    pay = 0.0
    hours_in_day = prompt_day_hours()
    hours_in_week += hours_in_day
    
    print(f"\tHours worked on {day}: {hours_in_day}")
    
    # Check if the hours worked on Sunday are eligible for double time.
    double_time = check_double_time(day)
    print(f"\tDouble time? {double_time}")

    # Day hours
    if hours_in_day > STANDARD_HOURS_PER_DAY:
        standard_hours = STANDARD_HOURS_PER_DAY
        overtime_hours = hours_in_day - STANDARD_HOURS_PER_DAY

        double_time_hours_left = hours_in_day - DOUBLE_TIME_HOURS_PER_DAY
        if double_time_hours_left > 0:
            double_time_hours = double_time_hours_left
    else:
        standard_hours = hours_in_day

    # Week hours
    if hours_in_week > STANDARD_HOURS_PER_WK:
        standard_hours = hours_in_week - hours_in_day
        overtime_hours = hours_in_week - STANDARD_HOURS_PER_WK

    # Calculate double time for the week.
    if double_time:
        double_time_hours = hours_in_day - STANDARD_HOURS_PER_DAY

    # Calculate the pay for the day based on the hours worked.
    pay = calc_standard_pay() + calc_overtime_pay() + calc_double_time_pay()
    
    paycheck.append({
        "day": day,
        "hours_worked": hours_in_day,
        "hours": {
            "standard_hours": standard_hours, 
            "overtime_hours": overtime_hours, 
            "double_time_hours": double_time_hours
        }, 
        "pay": pay
    })

    # Calculate the pay for the day and add it to the total pay.
    gross_pay += pay

    print(f"\tPay for {day}: ${pay:.2f} for {hours_in_day} hours worked.")
    print(f"\tPay for the week: ${gross_pay:.2f} for {hours_in_week} hours worked (so far).")

# Print results
show_paycheck()
 
# End of the program
