# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""

# global variable list
g_credit_score = 0
g_monthly_debt = 0
g_monthly_income = 0
g_loan_amount = 0
g_home_value = 0
g_qualifying_loan_list = []
g_all_loan_list = []

# import necessary modules and classes
import os                   # misc operating system module which may be used for path-related operations. Currently using pathlib instead
import csv                  # module to read/write CSV data
import sys                  # module used to exit the program(s) in the runtime environment (gitbash, eg.)
import fire                 # module used to create a command-line interface (CLI) in Python
import questionary          # module used to pose questions to the user, and accept user answers to the questions
from pathlib import Path    # module and class used for path-related operations.

# references to app "utility" functions
from qualifier.utils.fileio import load_csv                                                                 # helper function for loading and saving CSV files.
from qualifier.utils.calculators import (calculate_monthly_debt_ratio,calculate_loan_to_value_ratio)        # financial calculator functions needed to determine loan qualifications.

# references to app "filter" functions
from qualifier.filters.max_loan_size import filter_max_loan_size        # used to filter loans based upon loan amount
from qualifier.filters.credit_score import filter_credit_score          # used to filter loans based upon credit score
from qualifier.filters.debt_to_income import filter_debt_to_income      # used to filter loans by DTI ratio
from qualifier.filters.loan_to_value import filter_loan_to_value        # used to filter loans by LTV ratio

        

def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    # request path from user as set variable to path
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    
    # check for path viability, and exit program if path is not viable
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")
    return load_csv(csvpath)



def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """
    global g_credit_score
    global g_monthly_debt
    global g_monthly_income
    global g_loan_amount
    global g_home_value

    # request and capture user-entered loan criteria
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    # set local variables equal to user-entered information
    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    # set global variables equal to user-entered information
    g_credit_score = int(credit_score)
    g_monthly_debt = float(debt)
    g_monthly_income = float(income)
    g_loan_amount = float(loan_amount)
    g_home_value = float(home_value)
    
    print(g_credit_score)
    return credit_score,debt,income,loan_amount,home_value



def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """
    global g_qualifying_loan_list
    global g_all_loan_list

    g_all_loan_list = bank_data

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")
    
    g_qualifying_loan_list = bank_data_filtered
    
    return bank_data_filtered



def save_qualifying_loans(qualifying_loans):
    """Assesses number of qualifying loans (if any) and obtains desired file info from user

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """

    g_qualified_loan_list = qualifying_loans    

    # set variable equal to number of qualifying loans
    loan_count = len(qualifying_loans)

    # assess number of loans
    if int(loan_count) <= 0:    # if there are no qualifying loans, inform user and exit program
        print(f"There are {loan_count} qualifying loans, and no CSV file to save. Exiting program...")
        sys.exit        
    
    # if there are qualifying loans, provide user the option to save list of qualifying loans, or to exit system
    else:
        save_data_to_csv = questionary.select(f"There are {loan_count} qualifying loans. Would you like to save the list of qualifying loans to a CSV ?",choices=["yes","no"]).ask()
        if save_data_to_csv == "no":
            print(f"You have chosen not to save the list of qualifying loans to a CSV. Program ending...")
            sys.exit
        
        # if user opts to save qualifying loans to a CSV, ask for desired path for CSV file
        else:
            save_csv_path = questionary.text("Please enter the full path to which a CSV of the qualifying loans will be saved:").ask()
            test_save_csv(save_csv_path,qualifying_loans)



def test_save_csv(save_csv_path,qualifying_loan_list):
    """Verifies and saves the qualifying loans to a CSV file to the location specified by the user

    Args:
        save_csv_path (path): The user-indicated file path for the CSV.
        qualifying_loan_list (list of lists): The qualifying bank loans.
    """
    
    # set variable to user-indicated file path
    write_csv_path = Path(save_csv_path)

    # verify user-indicated path with user and ask whether to save the file, or exit program without saving file
    last_chance_save = questionary.select(f"You have chosen to save the CSV file to {write_csv_path}. Is this correct ?",choices=["yes","no"]).ask()
    
    # if user does not want to save CSV, exit program
    if last_chance_save == "no":
        print("Exiting program...")
        sys.exit
    
    # if user wants to save file, write all rows of qualifying loan list to CSV file and save
    else:
        with open(write_csv_path,'w',newline = '') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in qualifying_loan_list:
                csvwriter.writerow(row)

    print(f"Your CSV file containing the qualifying rows has been successfully saved to {write_csv_path} !")  

    test_response = questionary.select("Do you want to run a quick test to ensure the loan filtering process ?",choices=["yes","no"]).ask()

    if test_response == "no":
        print("Exiting program...")
        sys.exit
    else:
        test_filters()



def test_filters():
    """Determine for which loans the user failed to qualify, and list reason(s)

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        g_all_loan_list (list): A list of bank data.
        g_credit_score (int): The applicant's current credit score.
        g_monthly_debt (float): The applicant's total monthly debt payments.
        g_monthly_income (float): The applicant's total monthly income.
        g_loan_amount (float): The total loan amount applied for.
        g_home_value (float): The estimated home value.

    Returns:
        A list of the banks not willing to underwrite the loan, and reason

    """
    
    # reference to global variables
    global g_credit_score
    global g_monthly_debt
    global g_monthly_income
    global g_loan_amount
    global g_home_value

    # instantiate empty list for non-qualifying loans
    nonqualifying_loan_list = []    
    
    # compile list of non-qualifying loans, based upon loan qualification criteria
    for row in g_all_loan_list:
        if int(g_credit_score) < int(row[4]):
            nonqualifying_loan_list.append(row)
        elif int(g_loan_amount) > int(row[1]):
            nonqualifying_loan_list.append(row)
        elif float(g_monthly_debt) / float(g_monthly_income) > float(row[3]):
            nonqualifying_loan_list.append(row)
        elif float(g_loan_amount) / float(g_home_value) > float(row[2]):
            nonqualifying_loan_list.append(row)

    # set variable to hold # of non-qualifying loans
    nonqualifying_loan_count = len(nonqualifying_loan_list)        
    
    print(f"There are {nonqualifying_loan_count} non-qualifying_loans:")
    print()
    
    # for each non-qualifying loan, display reason for non-qualification
    for loan in nonqualifying_loan_list:
        if int(g_credit_score) < int(loan[4]):
            print(f"The credit score of {g_credit_score} was below the minimum allowed ({loan[4]}) for {loan[0]}.")            
        elif int(g_loan_amount) > int(loan[1]):
            print(f"The loan amount of {g_loan_amount} was above the maximum allowed ({loan[1]}) for {loan[0]}.")            
        elif float(g_monthly_debt)/float(g_monthly_income) > float(loan[3]):
            print(f"The debt-to-income ratio was above the maximum allowed ({loan[3]}) for {loan[0]}.")
        else:
            print(f"The loan-to-value ratio was above the maximum allowed ({loan[2]}) for {loan[0]}.")
    
def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)
    

if __name__ == "__main__":
    fire.Fire(run)
