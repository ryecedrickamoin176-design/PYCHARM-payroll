"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
                Employee Payroll Program
                    Section: 1ECEB
                    Group no. 1
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>
Group Leader: Amoin, Rye Cedrick

Group Members:
Riyos, Florence Rhian
Alvarez, Walter Henry G.
Mendoza, Trince Mike Ken M.
Sanchez. Dave Elvin A.
Hipolito, Ferdinand Jr A.

Currency: Philippine Peso (PHP)
Data Storage: JSON File
<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
import decimal
import json
import re
import os
import calendar
from datetime import datetime, date
from dis import Positions
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from operator import truediv

#Constant

Data_File = "payroll_data.json"
CENTAVO = Decimal("0.01")

Departments = ["Human Resouces", "Finance", "Information Technology", "Markering", "Operations"]
Positions =["Manager", "Supervisor", "Asisstant", "Staff"]

#Stores employee informationand payroll records

class Employee:
    def __init__(self, employee_no, employee_first_name, employee_last_name, tin, sss, philHealth,
                 department, position, hourlyRate ):

            self.employee_no = employee_no
            self.employee_first_name = employee_first_name
            self.employee_last_name = employee_last_name
            self.tin = tin
            self.sss = sss
            self.philHealth = philHealth
            self.department = department
            self.position = position
            self.hourlyRate = str(hourlyRate)
            self.payrollEntries = []

    #Converts employee information into JSON data
    def toDict(self):
        return {"employee_no": self.employee_no,
                "employee_first_name": self.employee_first_name,
                "employee_last_name": self.employee_last_name,
                "tin": self.tin,
                "sss": self.sss,
                "philHealth": self.philHealth,
                "department": self.department,
                "position": self.position,
                "hourlyRate": self.hourlyRate,
                "payrollEntries": self.payrollEntries
                }

#Calculates employee salary, overtime, deduction, and net pay
class Payroll:
    def __init__(self, pay_period_date, coverage_start, coverage_end, regular_hours, overtime_hours):
        self.pay_period_date = pay_period_date
        self.coverage_start = coverage_start
        self.coverage_end = coverage_end
        self.regular_hours = str(regular_hours)
        self.overtime_hours = str(overtime_hours)

    #calculates all payroll amounts
    def calculate(self, hourlyRate):
        rate = Decimal(str(hourlyRate))
        regular_hours = Decimal(self.regular_hours)
        overtime_hours = Decimal(self.overtime_hours)

        regular_pay = (regular_hours * rate).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        overtime_rate = rate * Decimal("1.5")
        overtime_pay = (overtime_hours * overtime_rate).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        gross_pay = (regular_pay + overtime_pay).quantize(CENTAVO)
        withholding_tax = (gross_pay * Decimal("0.15")).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        sss_contribution = (gross_pay * Decimal("0.15")).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        philHealth_contribution =(gross_pay * Decimal("0.05")).quantize(CENTAVO, rounding=ROUND_HALF_UP)
        total_deduction = (withholding_tax + sss_contribution + philHealth_contribution)
        net_pay = gross_pay -total_deduction

        return {"regularpay": regular_pay, "overtimeRate": overtime_rate, "overtimePay": overtime_pay,
                "grosspay": gross_pay, "withholdingTax": withholding_tax, "ssscontribution": sss_contribution,
                "philHealthcontribution": philHealth_contribution, "total_deduction": total_deduction,
                "netpay": net_pay}

    def toDict(self):
        return{"pay_period_date": self.pay_period_date, "coverage_start": self.coverage_start,
               "coverage_end": self.coverage_end, "regular_hours": self.regular_hours,
               "overtime_hours": self.overtime_hours}
    
    
#Function:Load employees
#Retrieves previously saved employee records from JSON

def loadEmployees():
    if not os.path.exists(Data_File):
            return{}

    try:
        with open(Data_File) as file: data = json.load(file)

        employees = []

        for employee_no, details in data ["employees"].items():

            employee = Employee(employee_no,
            details["employee_first_name"],
            details["employee_last_name"],
            details["tin"],
            details["sss"],
            details["philHealth"],
            details["department"],
            details["position"],
            details["hourlyRate"],)


            employees.payrollEntries = details.get("payrollEntries", [])
            employees[employee_no] = employee

        return employees

    except (json.JSONDecodeError, KeyError, TypeError, OSError) as error:

        raise RuntimeError("The Payroll data file sis invalid or damaged")from error

#Save data of employees

def saveEmployees(employees):

    data = {"employees":{employee_no: employee.toDict() for employee_no, employee in employees.items()}}

    try:
        tempFile = Data_File + ".tmp"

        with open(tempFile, "w") as file: json.dump(data, file, indent=4)

        os.replace(tempFile, Data_File)

        return True

    except OSError as error:

        print("Error saving records", error)

        if os.path.exists(Data_File + ".tmp"):
            os.remove(Data_File + ".tmp")

        return False


#Prevents blanks or empty spaces

def getRequiredText(Prompt):
    while True:
        value = input(Prompt).strip()

        if value:
            return value
        else:
            print("Invalid input! This field is required or cannot be empty.")

#Accepts the ID format M2026-XXXX

def getEmployeeNo():
    while True:

        employee_no = input("Enter employee number (M2026-XXXX): ").strip().upper()



#Checks whether the ID/Number contains the required number of digits

def getGovernmentID(label, legnth):

    while True:
        value = input(f"Enter {label} ({legnth} digits): ").strip()

        if value.isdigit() and len(value) == legnth:
            return value

        else:
            print(f"Invalid {label}! This field must contain exactly {legnth} digits.")



#Rejects Zero, negative, and non-numeric values

def getPositiveNumber(prompt):
    while True:
        try:
            value = Decimal(input(prompt).strip())

            if value.is_finite() and value > 0:
                return value

            else:
                print("Invalid input! This field must contain a number greater than zero.")

        except InvalidOperation:
            print("Invalid input! Please enter a valid number.")

#Use a list of valid choices and rejects invalid option

def chooseFromList(title, choices):
    print(f"\nM<<<<<<<<<< {title} >>>>>>>>>>")

    for number, choice in enumerate(choices, start=1):
        print(f"{number}. {choice}")

    while True:
        try:
            selected = int(input("Enter your choice: "))

            if 1 <= selected <= len(choices):
                return choices[selected-1]
            else:
                print("Invalid choice! Please enter a valid choice.")
        except ValueError:
            print("Invalid choice! Please enter a valid choice.")

def getPayPeriod():
    while True:
        dateText: input("Enter Pay Period date(YYYY-MM-DD): ").strip()

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", dateText):
            print ("Invalid Format! Use YYYY-MM-DD format.")
            continue

        try:
            periodDate = date.fromisoformat(dateText)

        except ValueError:
            print("Invalid Calendar Date.")
            continue

        lastDay = calendar.monthrange(periodDate.year, periodDate.month)[1]

        if periodDate.day == 15:

            coverageStart = date(periodDate.year, periodDate.month, 1 )
            coverageEnd = periodDate

        elif periodDate == lastDay:
            coverageStart = date(periodDate.year, periodDate.month, 16)
            coverageEnd = periodDate

        else:
            print("Invalid pay period date. Enter only 15th" "or the last date of the month")
            continue
        return (periodDate, coverageStart, coverageEnd)

#Allows users to repeat an operation or return to the main menu

def askAnothertransaction():
    while True:
        answer = input("\nDo you want another transaction? (Y/N): ").strip().lower()

        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Invalid input! Please enter a valid input.")

#Collects and saves new Employee Info.

def registerEmployee(employees):

    print("\n<<<<<<<<<< REGISTER EMPLOYEE >>>>>>>>>>")

    employee_no = getEmployeeNo()
    #If else statement to prevent duplicate registration
    if employee_no in employees:
        print("Employee Number already exists.")

        return
    else:
        first_name = getRequiredText("Enter first name: ")
        last_name = getRequiredText("Enter last name: ")

        tin = getGovernmentID("Enter TIN: ", 12)
        sss = getGovernmentID("Enter SSS: ", 10)
        philhealth = getGovernmentID("Enter PHIL HEALTH: ", 12)

        department = chooseFromList("Department: ", Departments)
        position = chooseFromList("Position: ", Positions)
        hourlyRate = getPositiveNumber("Enter hourly rate: ")

        employee = Employee(employee_no, first_name,
                            last_name, tin, sss, philhealth, position,
                            hourlyRate)

        employees[employee_no] = employee

        if saveEmployees(employees):
            print("\nEmployee successfully registered!")

        else:
            del employees[employee_no]
            print("\nEmployee failed because saving was unsuccessful.")

            return

#Records employee working hours and saves payroll transactions

def payrollScreen(employees):
    print("<<<<<<<<<< PAYROLL SCREEN >>>>>>>>>>")

    employee_no = input("Enter employee number: ").strip().upper()

    #validates whether the employee is registered
    if employee_no not in employees:
        print("Invalid Employee number! Employee number not found")

        return
    employee = employees[employee_no]

    periodDate, coverageStart, coverageEnd = getPayPeriod()

    print("\n<<<<<<<<<< PAY PERIOD COVERAGE >>>>>>>>>>")

    print("Start Date", coverageStart)
    print("End Date", coverageEnd)

    #Prevents Duplicate payroll entries on the same pay period

    for entry in employee.entries:
        if entry["payPeriodDate"] == periodDate.isoformat():
            print("Payroll entry already exists for this period")

            return

    regular_hours = getPositiveNumber("Enter regular hours: ")
    overtime_hours = getPositiveNumber("Enter overtime hours: ")
    payroll = Payroll(periodDate.isoformat(), coverageStart.isoformat(),
                      coverageEnd.isoformat(), regular_hours, overtime_hours)
    employee.payrollEntries.append(payroll.toDict())

    if saveEmployees(employees):
        print("\nPayroll transaction successfully saved!")

    else:
        employees.payrollEntries.pop()
        print("Payroll transaction failed because saving was unsuccessful.")

#Displays Employee information and all payroll transactions

def viewEmployee(employees):
    print("\n<<<<<<<<<< VIEW EMPLOYEE >>>>>>>>")

    employee_no = input("Enter employee number: ").strip().upper()

    if employee_no not in employees:
        print("Invalid Employee number! Employee number not found")

        return

    employee = employees[employee_no]

    print("\n<<<<<<<<<<< EMPLOYEE DETAILS >>>>>>>>>>")

    print("Employee Number", employee_employeeID)
    print("First Name", employee.first_name)
    print("Last Name", employee.last_name)
    print("TIN ID", employee.tin)
    print("SSS ID", employee.sss)
    print("PhilHealth ID", employee.philhealth)
    print("Assign Department", employee.department)
    print("Position", employee.position)

    print(f"Salary Rate per hour: PHP " f"{Decimal(employee.hourlyRate):,.2f}")

    #for loop for displaying all payroll records of the employee
    if not employee.payrollEntries:
        print("No payroll record available")

    for number, entry in enumerate(employee.payrollEntries, start=1):
        payroll = Payroll(
        entry["payPeriodDate"],
        entry["coverageStart"],
        entry["coverageEnd"],
        entry["regularHours"],
        entry["overtimeHours"],
        )

        result = payroll.calculate(employee.payrollEntries)

        print(f"\n<<<<<<<<<< PAYROLL {number } >>>>>>>>>")

        print("Pay Period Date:", entry["payPeriodDate"])

        print("Coverage Start Date:", entry["coverageStart"], "to", entry["coverageEND"])

        print("Regular Hours", entry["regularHours"])
        print("Overtime Hours", entry["overtimeHours"])

        print(f"Base Rate Per Hour: PHP " f"{Decimal(employee.hourlyRate):,.2f}")

        print (f"Overtime Rate Per Hour: PHP " f"{result['overtimeRate']:,.2f}")

        print(f"Total Regular Pay: PHP " f"{result['regularPay']:,.2f}")

        print(f"Total Overtime Pay: PHP " f"{result['overtimePay']:,.2f}")

        print(f"Total Gross Pay: PHP " f"{result['grossPay']:,.2f}")

        print("\n<<<<<<<<< DEDUCTIONS >>>>>>>>>>")

        print(f"Witholding Tax (15%): PHP " f"{result['withholdingTax']:,.2f}")

        print(f"SSS Contribution (2%): PHP " f"{result['sssContribution']:,.2f}")

        print(f"Total Dedeuctions: PHP " f"{result['totalDeductions']:,.2f}")

        print("\n========================================")

        print(f"Total Net Pay: PHP " f"{result['netPay']:,.2f}")

    print("\n========================================")

#Repeat Screen
#While loop to repeat the selected program

def repeatScreen(screenFunction, employees):
    while True:
        screenFunction(employees)

        if not askAnothertransaction():
            break

#Main Menu
#Uses MATCH-CASES

def mainMenu(employees):

    while True:

        print("\n" + "=" * 48)

        print("               Employee Payroll SYSTEM")
        print("                    Section 1ECEB")
        print("                        Group 1")

        print("=" * 48)

        print("1. Payroll")
        print("2. Register Employee")
        print("3. View Employee")
        print("4. Exit")

        print("=" * 48)

        try:
            choice = int(input("Enter your choice (1-4): "))

        except ValueError:
            print("Invalid choice! Please try again.")

            continue

        #Selection of operation based on the employee choice

        match choice:

            case 1: repeatScreen(payrollScreen, employees)
            case 2: repeatScreen(registerEmployee, employees)
            case 3: repeatScreen(viewEmployee, employees)
            case 4:
                    print("\nThank you for using our program")
                    print("GOODBYE")
                    break
            case _:
                print("Invalid choice! Please try again.")

#Loads the save data and starts the payroll system

def main():

    print("\nLoading Employee Payroll System....")

    try:
        employees = loadEmployees()

    except RuntimeError as error:
        print("ERROR:", error)

        print("Program terminated to protect existing records.")

        return

    print(f"Successfully loaded {len(employees)} employees record(s).")

    mainMenu(employees)

#Program starts and executes the main function when program is opened
if __name__ == "__main__":
    main()











































    























        




































            
            

