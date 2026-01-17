import os
import sqlite3
import logging
from logging import getLogger
# import clr

from src.employee import Employee
from tools.decorators.deco import output_transformer

"""
NOTSET 0 
indicates that ancestor loggers are to be consulted to determine the effective level. 
If that still resolves to NOTSET, then all events are logged. 
When set on a handler, all events are handled.
DEBUG 10
Detailed information, typically only of interest to a developer trying to diagnose a problem.
INFO 20
Confirmation that things are working as expected.
WARNING 30
An indication that something unexpected happened, or that a problem might occur in the 
near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR 40
Due to a more serious problem, the software has not been able to perform some function.
logging.CRITICAL 50
A serious error, indicating that the program itself may be unable to continue running.

    Handler	                    Purpose
    
    StreamHandler	            Sends logs to streams like sys.stdout or sys.stderr. Default console output.
    FileHandler	                Writes logs to a file on disk.
    NullHandler	                Consumes logs silently. Used in libraries to avoid “No handler found” warnings.
    WatchedFileHandler	        Like FileHandler, but checks for external file rotation (Unix).
    RotatingFileHandler	        Writes to file and rotates when size limit reached (maxBytes).
    TimedRotatingFileHandler	Rotates log files based on time interval (daily, hourly, weekly, etc.).
    SocketHandler	            Sends logs over TCP/UDP to a remote machine.
    DatagramHandler	            Sends log records as UDP datagrams.
    SMTPHandler	                Sends log records by email using SMTP.
    HTTPHandler	                Sends logs to web servers using HTTP GET/POST.
    QueueHandler	            Enqueues log records into a queue.Queue (for multiprocessing/thread-safe logging).
    SysLogHandler	            Sends records to a Unix syslog service or remote syslog server.
    NTEventLogHandler	        Logs to the Windows event log.
    MemoryHandler	            Buffers logs in memory, flushing to another handler based on criteria.
    BufferingHandler	        Base class for buffering handlers (not usually used directly).



| Symbol                    | Meaning                                            |
| ------------------------- | -------------------------------------------------- |
| **`%(asctime)s`**         | Human-readable time when the LogRecord was created |
| **`%(created)f`**         | Unix timestamp (float seconds since epoch)         |
| **`%(msecs)d`**           | Milliseconds portion of `%(asctime)s`              |
| **`%(relativeCreated)d`** | Milliseconds since logging started                 |
| **`%(levelname)s`**       | Log level name (e.g. INFO, ERROR)                  |
| **`%(levelno)d`**         | Log level number (e.g. 20 for INFO)                |
| **`%(name)s`**            | Logger name                                        |
| **`%(message)s`**         | The logged message (after formatting arguments)    |
| **`%(pathname)s`**        | Full path of source file                           |
| **`%(filename)s`**        | Base file name                                     |
| **`%(module)s`**          | Module name of the source file                     |
| **`%(funcName)s`**        | Function name containing the logging call          |
| **`%(lineno)d`**          | Line number in source code                         |
| **`%(process)d`**         | Process ID                                         |
| **`%(processName)s`**     | Process name                                       |
| **`%(thread)d`**          | Thread ID                                          |
| **`%(threadName)s`**      | Thread name                                        |
| **`%(stack_info)s`**      | Stack frame information (if available)             |
| **`%(exc_info)s`**        | Exception traceback                                |
| **`%(exc_text)s`**        | Text form of exception (generated automatically)   |
"""

# All constants and controls for logging system should be controlled here

logger = getLogger(__name__)

logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s line %(lineno)d:  %(asctime)s:  %(stack_info)s:  %(name)s:%(message)s')

file_handler = logging.FileHandler('employee.log')  # from instrumentation file
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

"""
Logger Levels

DEBUG
INFO
WARNING
ERROR
CRITICAL

"""




class PayrollHub:
    def __init__(self):
        self.employee_list:list[Employee] = []
        self.database_table_name:str|None = None

    @output_transformer(str.upper)
    def add_employee(self, employee:Employee) -> str:
        self.employee_list.append(employee)
        logger.info(f'Added employee: {employee} to employee list')

        return f'Added {employee.name} to employee list'

    def calculate_payroll(self, employee: Employee, weekly_hours: int, hourly_wage: float) -> Employee:

        # if employee in records and has an employee id calculate payroll
        if employee in self.employee_list and employee.is_eligible_to_work():
            employee.payout = weekly_hours * hourly_wage
        else:
            ##TODO BUG
            if employee not in self.employee_list:
                logger.debug(f'{employee.name} not in {self.employee_list}')
                raise ValueError(f'Employee {employee.name} not found in employee list')
            else:
                logger.debug('Employee ID', employee.employee_id)
                raise ValueError(f'Employee is not eligible to work, likely because they do not have an employee ID')

        return employee

    def print_employee_list(self) -> None:
        for employee in self.employee_list:
            print(employee)

    def add_employee_info_to_database(self, database_path: str, database_name: str, employee: Employee) -> None: # , table_name: str
        # os.chdir('..')
        os.chdir(database_path)

        employee_info:list = [

            employee.name,
            employee.age,
            employee.employee_id,
            employee.email,
            employee.postal_code
            
        ]

        if database_name in os.listdir():
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            try:
                cursor.execute('CREATE TABLE Employee (name, age, employee_id, email, postal_code)')
                logger.debug('New Created Table: Employee')
                cursor.execute('INSERT INTO Employee (name, age, employee_id, email, postal_code) VALUES (?, ?, ?, ?, ?)', employee_info)
                logger.debug('Inserted values into table Employee')
                logger.info('Commiting changes')
                connection.commit()
                logger.info('Closing database')
                connection.close()
            except sqlite3.OperationalError:
                cursor.execute('INSERT INTO Employee (name, age, employee_id, email, postal_code) VALUES (?, ?, ?, ?, ?)', employee_info)
                logger.debug(f'Inserted Values {employee_info} into existing Table')
                logger.info('Commiting changes')
                connection.commit()
                logger.info('Closing database')
                connection.close()
                
        #     # make employee table
        #     if table_name != self.database_table_name:
        #         try:
        #             ##TODO not the right syntax for sqlite3 | placeholders ? should be used instead of a formatted string
        #             cursor.execute(f'CREATE TABLE {table_name} (name, age, employee_id, email, postal_code)')
        #             cursor.execute(f"""
        #             INSERT INTO employee(name, age, employee_id, email, postal_code)
        #             VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info['employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
        #             """)
        #             self.database_table_name = table_name
        #         # if table already exists
        #         except sqlite3.OperationalError:

        #             cursor.execute("""
        #                            INSERT INTO {table_name} (name, age, employee_id, email, postal_code)
        #                            VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info[
        #                                     'employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
        #                            """)

        #     else:
        #         cursor.execute("""
        #         INSERT INTO table_name (name, age, employee_id, email, postal_code) VALUES ({employee_info['name']}, {employee_info['age']}, {employee_info['employee_id']}, {employee_info['email']}, {employee_info['postal_code']})
        #         """)
        # else:
        #     raise FileNotFoundError(f'Database "{database_name}" not found in Directory {database_path}')

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
    pay_hub.add_employee_info_to_database(database_path='data', database_name='employee.db', employee=jordan)

    pass
