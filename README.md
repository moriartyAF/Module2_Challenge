# Loan Qualification CLI

This exquisitely simple, yet powerful, CLI application simplifies the loan qualification assessment process by empowering the user to engage with command line prompts to enter and analyze loan information, as well as to save the information to a local drive/directory

---

## Technologies

This application incorporates the power of Python 3.8.8 with the following packages & modules:

* **fire**:         Used to create a command-line interface (CLI) in Python.
* **questionary**:  Used to pose questions to the user, and accept user answers to these questions
* **sys**:          Used to assist in exiting the programs in the runtime environment (gitbash, et al.)
* **csv**:          Used to read/write CSV files
* **os**:           Used for path-related operations (currently inactive)
* **pathlib**       Used for path-related operations (currently active)

---

## Installation Guide

Before running the application, the following dependencies must be installed:

    pip install fire
    pip install questionary

---

## Usage

In addition to the above installed dependencies, the execution of the application requires

  an accessible CSV file of the daily rate sheet
  a complete set of loan qualification criteria, including
    
    credit score
    monthly income
    monthly debt
    loan amount requested
    home value
    
The execution of the application requires inputting the following line of code into the CLI of choice:

    python app.py
    
A series of questionary-launched questions will fire requiring user input to complete the process, including the above loan qualification criteria.

Upon successful completion of the program, the following tasks will be completed automatically:

    a generation of a list of lenders whose loan eligibility criteria has been met by the loan applicant.
    the opportunity to save the list of lenders as a CSV file to a local network.
    the ability to audit the loan eligibility criteria for lenders for whom the applicant does not qualify.

---

## Contributors

    Moriarty Consulting LLC
    Columbia Engineering FinTech Boot Camp

---

## License

    University of Michigan, Ann Arbor, MI
