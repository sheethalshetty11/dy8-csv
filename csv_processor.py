import csv
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


def read_employee_data(filename):
    employees = []

    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("CSV file is empty.")
                logging.warning("Empty CSV file.")
                return employees

            required_columns = ["id", "name", "department", "salary"]

            for column in required_columns:
                if column not in reader.fieldnames:
                    raise KeyError(column)

            row_num = 1

            for row in reader:
                try:
                    row["salary"] = float(row["salary"])
                    employees.append(row)
                except ValueError:
                    logging.warning(
                        f"Invalid salary '{row['salary']}' on row {row_num}, skipping"
                    )

                row_num += 1

        logging.info(f"Loaded {len(employees)} employees from {filename}")
        return employees

    except FileNotFoundError:
        print(f"File not found: {filename}")
        logging.error(f"File not found: {filename}")

    except KeyError as e:
        print(f"Missing column: {e}")
        logging.error(f"Missing column: {e}")

    return []


def generate_report(employees):
    if not employees:
        print("No employee data available.")
        logging.warning("No employee data available for report generation.")
        return

    salaries = [emp["salary"] for emp in employees]

    total_employees = len(employees)
    average_salary = sum(salaries) / total_employees
    highest_salary = max(salaries)
    lowest_salary = min(salaries)

    department_count = defaultdict(int)

    for emp in employees:
        department_count[emp["department"]] += 1

    print("\n===== Employee Report =====")
    print(f"Total Employees     : {total_employees}")
    print(f"Average Salary      : {average_salary:.2f}")
    print(f"Highest Salary      : {highest_salary:.2f}")
    print(f"Lowest Salary       : {lowest_salary:.2f}")

    print("\nDepartment-wise Count:")

    for dept, count in department_count.items():
        print(f"  {dept:<18}: {count}")

    logging.info("Report generated successfully")


def main():
    logging.info("Application started")

    filename = "employees.csv"
    employees = read_employee_data(filename)

    generate_report(employees)

    logging.info("Application exited")


if __name__ == "__main__":
    main()
