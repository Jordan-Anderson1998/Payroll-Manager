from employee import Employee
import os
import sqlite3
# import clr


class PayrollHub:
    def __init__(self):
        self.employee_list:list = []
        self.database_table_name:str|None = None

    def add_employee(self, employee:Employee) -> str:
        self.employee_list.append(employee)

        return f'Added {employee.name} to employee list'

    def calculate_payroll(self, employee: Employee, weekly_hours: int, hourly_wage: float) -> Employee:

        # if employee in records and has an employee id calculate payroll
        if employee in self.employee_list and employee.is_eligible_to_work():
            employee.payout = weekly_hours * hourly_wage
        else:
            raise ValueError(f'Employee {employee.name} not found in employee list')

        return employee

    def print_employee_list(self) -> None:
        for employee in self.employee_list:
            print(employee)

    def add_employee_info_to_database(self, database_path: str, database_name: str, employee: Employee, table_name: str) -> None:
        os.chdir('..')
        os.chdir(database_path)

        employee_info = {'name': employee.name,
                         'age': employee.age,
                         'employee_id': employee.employee_id,
                         'email': employee.email,
                         'postal_code': employee.postal_code,}

        if database_name in os.listdir():
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            # make employee table
            if table_name != self.database_table_name:
                try:
                    ##TODO not the right syntax for sqlite3 | placeholders ? should be used instead of a formatted string
                    cursor.execute(f'CREATE TABLE {table_name} (name, age, employee_id, email, postal_code)')
                    cursor.execute(f"""
                    INSERT INTO employee(name, age, employee_id, email, postal_code)
                    VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info['employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
                    """)
                    self.database_table_name = table_name
                # if table already exists
                except sqlite3.OperationalError:

                    cursor.execute("""
                                   INSERT INTO {table_name} (name, age, employee_id, email, postal_code)
                                   VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info[
                                            'employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
                                   """)

            else:
                cursor.execute("""
                INSERT INTO table_name (name, age, employee_id, email, postal_code) VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info['employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
                """)
        else:
            raise FileNotFoundError(f'Database "{database_name}" not found in Directory {database_path}')

    def add_employee_info_to_file(self, employee:Employee, file_name: str):
        if file_name not in os.listdir():
            # if file does not exist in directory
            with open(file_name, 'w') as f:
                f.write(f'{employee.name}, {employee.age}, {employee.employee_id}, {employee.email}, {employee.postal_code} \n')
        else:
            # append information if file already exists
            with open(file_name, 'a') as f:
                f.write(f'{employee.name}, {employee.age}, {employee.employee_id}, {employee.email}, {employee.postal_code} \n')


if __name__ == '__main__':
    jordan = Employee(age=27, name="Jordan", email="jordan.anderson@gmail.com", postal_code="S4S 0A2")
    jordan.make_new_employee_id(10)

    pay_hub = PayrollHub()
    pay_hub.add_employee(employee=jordan)
    pay = pay_hub.calculate_payroll(employee=jordan, weekly_hours=40, hourly_wage=15)
    print(pay)
    pay_hub.print_employee_list()

    pay_hub.add_employee_info_to_file(employee=jordan, file_name="employee_info.txt")
    pay_hub.add_employee_info_to_database(database_path='data', database_name='employee.db', employee=jordan, table_name='employee_info')
