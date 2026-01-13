import tkinter as tk
from tkinter import ttk, Tk
from tkinter import messagebox
from employee import Employee
from payroll_hub import PayrollHub

import logging
from logging import getLogger

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

file_handler = logging.FileHandler('.log')  # from instrumentation file
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

class Model:
    """
    Model is responsible for instantiating the payroll hub, which controls the methods for dealing with employees.
    """

    def __init__(self, hub: PayrollHub = None):
        self.hub = hub

    def add_hub(self, hub: PayrollHub):
        self.hub = hub


class Controller:

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self._found_employee:bool = False
        self.employee:None|Employee = None
        self._minimum_wage:float = 15.0

    def search_for_employee_click_event_handler(self) -> None:
        """ Iterate through the employee list in the central hub and check input against the names in employee list.

        Args:
            arg1 (:obj:`type`): Positional parameter 1
                desc
            arg2 (:obj:`type`): keyword-only required argument

        Returns:
            (:obj)

        Raises:
            (:type)

        Examples:
              TODO Incomplete doctest
              >>>pass
              >>>pass
        """
        hub = self.model.hub
        view = self.view

        # get the input for the entry and check against the employee list
        employee_check = view.employee_lookup_entry.get()
        logger.debug(f'Searching for employee: {employee_check}')

        for employee in hub.employee_list:
            # if employee name is found in employee list
            if employee_check in employee.name:
                logger.debug(f'Employee found: {employee_check}')
                self.employee = employee
                view.current_employee_selected.insert(tk.END, employee_check)
                messagebox.showinfo(f'Found employee {employee_check}')
                self._found_employee = True
        else:
            logger.debug(f'Employee: {employee_check} not found in employee list: {hub.employee_list}')
            view.current_employee_selected.insert(tk.END, f'Employee {employee_check} not found')
            messagebox.showinfo(f'Employee {employee_check} not found')
            self._found_employee = False

    def find_new_employee_click_event_handler(self):
        """ Enable the button to add an employee if employee is found in records, else button is disabled.
            If button is pressed, append emplyoee to central hub records.

        Args:
            arg1 (:obj:`type`): Positional parameter 1
                desc
            arg2 (:obj:`type`): keyword-only required argument

        Returns:
            (:obj)

        Raises:
            (:type)

        Examples:
              TODO Incomplete doctest
              >>>pass
              >>>pass
        """
        view = self.view
        hub = self.model.hub

        if not self._found_employee:
            view.add_new_employee_button.state(tk.DISABLED)
            messagebox.showinfo('Did not find employee')
            logger.info('Button to add employee is disabled because employee was not found.')
        else:
            # hub.add_employee(view.current_employee_selected.get(tk.END))
            view.add_new_employee_button.state(tk.ACTIVE)
            messagebox.showinfo('Found employee')
            logger.debug(f'Employee: {view.current_employee_selected.get(tk.END)} added to employee list')

    def add_weekly_hours_click_event_handler(self):
        """ If employee is found in records, add a new attribute to employee 'hours' that contains the hours inputted.

        Args:
            arg1 (:obj:`type`): Positional parameter 1
                desc
            arg2 (:obj:`type`): keyword-only required argument

        Returns:
            (:obj)

        Raises:
            (:type)

        Examples:
              TODO Incomplete doctest
              >>>pass
              >>>pass
        """
        view = self.view
        hub = self.model.hub
        employee = self.employee

        if self._found_employee:
            # add new field hours to employee
            employee.hours = int(view.add_weekly_hours_for_employee_entry.get())

    def calculate_weekly_pay_click_event_handler(self):
        employee = self.employee
        hub = self.model.hub
        view = self.view

        if self._found_employee:
            try:
                employee_with_pay = hub.calculate_payroll(employee, employee.hours, self._minimum_wage)
                view.weekly_pay_owed.insert(tk.END, str(employee_with_pay.payout))
            except AttributeError:
                logger.warning(f'{employee.name} does not have their hours in the system yet or is not eligible for pay \n employee might not have an employee ID.')
                logger.debug(f'{employee.name} eligible to work: {employee.is_eligible_to_work()}')

    def make_new_employee_id(self, num_of_chars: int):
        if self.employee:
            self.employee.make_new_employee_id(chars=num_of_chars)
        else:
            raise AttributeError(f'<self.employee> is not an attribute of {self} object \n Add employee before making employee ID.')

    def __str__(self):
        return 'Controller'

    def __repr__(self):

        return f'{self.model=}, {self.view=}, {self.employee=}'

class View(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        """
        Possible layout:
        
        Label Row 0 Col 0
        row 1 col 0    row 1 col 1   row 1 col 3
        Entry ->       Button     -> Listbox
        
        Label Row 1 Col 0
        row 2 col 0   row 2 col 2   row 2 col 3
        Entry ->       Button      -> Listbox
        
        """

        # widgets
        self.employee_lookup_label = ttk.Label(text='Search for Employee')
        # self.employee_lookup_label.pack()
        self.employee_lookup_label.grid(padx=10, pady=10)
        self.employee_lookup_label.place(x=25, y=0)

        self.employee_lookup_entry = ttk.Entry(self)
        # self.employee_lookup_entry.place(x=0, y=50)
        # self.employee_lookup_entry.pack()
        self.employee_lookup_entry.grid(padx=10, pady=10)

        self.employee_lookup_button = ttk.Button(self, command=self.employee_lookup, text='Submit')
        # self.employee_lookup_button.pack()
        self.employee_lookup_button.grid(row=1, column=2, padx=5, pady=5)
        # self.employee_lookup_button.place(x=0, y=100)


        self.add_new_employee_label = ttk.Label(text='Add New Employee')
        # self.add_new_employee_label.place(x=0, y=0)
        #
        # self.add_new_employee_label.pack(side='left')
        self.add_new_employee_label.grid(padx=10, pady=10)
        self.add_new_employee_label.place(x=25, y=125)
        #
        self.add_new_employee_button = ttk.Button(self, command=self.add_new_employee, text='Submit')
        # self.add_new_employee_button.place(x=0, y=100)
        # self.add_new_employee_button.pack()
        self.add_new_employee_button.grid(row=2, column=2, padx=10, pady=10)
        # self.add_new_employee_button.place(x=75, y=55)

        #
        self.add_new_employee_entry = ttk.Entry(self)
        # self.add_new_employee_entry.place(x=0, y=150)
        # self.add_new_employee_entry.pack()
        self.add_new_employee_entry.grid(padx=10, pady=10)
        #
        self.current_employee_label = ttk.Label(text='Current Employee')

        self.current_employee_label.grid(padx=10, pady=10)
        self.current_employee_label.place(x=25, y=175)

        self.current_employee_selected = tk.Listbox(self)
        self.current_employee_selected.grid(padx=10, pady=10)

        self.add_new_hours_label = ttk.Label(text='Add New Hours')
        self.add_new_hours_label.grid(padx=10, pady=10)
        self.add_new_hours_label.place(x=25, y=350)

        self.add_new_hourly_wage_for_employee_entry = ttk.Entry(self)
        self.add_new_hourly_wage_for_employee_entry.grid(padx=10, pady=10)

        self.add_new_hourly_wage_for_employee_button = ttk.Button(self, text='Submit', command=self.add_new_hourly_wage_for_employee)
        self.add_new_hourly_wage_for_employee_button.grid(padx=10, pady=10)

        self.add_weekly_hours_label = ttk.Label(text='Add Weekly Hours')
        self.add_weekly_hours_label.grid(padx=10, pady=10)
        self.add_weekly_hours_label.place(x=25, y=435)

        self.add_weekly_hours_for_employee_entry = ttk.Entry(self)
        self.add_weekly_hours_for_employee_entry.grid(padx=10, pady=10)

        self.add_weekly_hours_for_employee_button = ttk.Button(self, command=self.add_weekly_hours_for_employee, text='Submit')
        self.add_weekly_hours_for_employee_button.grid(padx=10, pady=10)

        self.calculate_weekly_pay_label = ttk.Label(text='Calculate Weekly Pay')
        self.calculate_weekly_pay_label.grid(padx=10, pady=10)
        self.calculate_weekly_pay_label.place(x=25, y=520)

        self.calculate_weekly_pay_button = ttk.Button(self, command=self.calculate_weekly_pay, text='Submit')
        self.calculate_weekly_pay_button.grid(padx=10, pady=10)

        self.weekly_pay_owed = tk.Listbox(self)
        self.weekly_pay_owed.grid(padx=10, pady=10)

    def add_controller(self, controller: Controller):
        self.controller = controller

    def employee_lookup(self) -> None:
        if self.controller:
            self.controller.search_for_employee_click_event_handler()
        else:
            raise AttributeError(f'{self} does not have a controller')

    def add_new_employee(self):
        if self.controller:
            self.controller.search_for_employee_click_event_handler()
        else:
            raise AttributeError(f'{self} does not have a controller')

    def add_new_hourly_wage_for_employee(self):
        if self.controller:
            self.controller.add_weekly_hours_click_event_handler()
        else:
            raise AttributeError(f'{self} does not have a controller')

    def add_weekly_hours_for_employee(self):
        if self.controller:
            self.controller.add_weekly_hours_click_event_handler()
        else:
            raise AttributeError(f'{self} does not have a controller')

    def calculate_weekly_pay(self):
        if self.controller:
            self.controller.calculate_weekly_pay_click_event_handler()
        else:
            raise AttributeError(f'{self} does not have a controller')

    def __str__(self):
        return 'View'


class App(Tk):

    def __init__(self, screen_dimensions: str, title: str):
        super().__init__()

        self.geometry(screen_dimensions)
        self.title(title)

        model = Model()
        model.add_hub(hub=PayrollHub())
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)
        # view.grid(row=0, column=0, sticky="nsew")
        controller = Controller(model, view)

        view.add_controller(controller)

if __name__ == '__main__':
    app = App(screen_dimensions="1280x720", title="Employee Payroll")
    app.mainloop()
