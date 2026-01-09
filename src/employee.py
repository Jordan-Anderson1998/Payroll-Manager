from abc import ABC, abstractmethod
from typing import Any, Final
import re
import doctest
from random import randint
import logging
from logging import getLogger
import warnings
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


__ALL__:Final = ['Enforcer', 'IntEnforcer', 'NameEnforcer', 'EmailEnforcer', 'AddressEnforcer', 'names']

names:list[str] = [
    "Liam", "Noah", "Ava", "Mia", "Zoe",
    "Emma", "Olivia", "Lucas", "Ethan", "Mason",
    "Aria", "Nora", "Chloe", "Layla", "Ellie",
    "Caleb", "Isaac", "Henry", "Wyatt", "Levi",
    "Hazel", "Stella", "Violet", "Sadie", "Clara",
    "Miles", "Julian", "Asher", "Owen", "Felix",
    "Ruby", "Ivy", "Elena", "Naomi", "Daphne",
    "Silas", "Jasper", "Rowan", "Aiden", "Soren",
    "Talia", "Maren", "Freya", "Corin", "Rylan",
    "Kira", "Lena", "Tessa", "Ariel", "Milo", 'Alexander'
    ,'Graham', 'Emmanuel', 'Isa', 'Jeremiah', 'Wong', 'Chung'
]

class Enforcer(ABC):

    def __set_name__(self, owner, name):
        self._name = f'_{name}'

    def __get__(self, instance, owner):
        if not instance:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if self.verify(value):
            setattr(instance, self._name, value)

    def __repr__(self):
        return self._name

    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def verify(self, value: Any):
        raise NotImplementedError


class AgeEnforcer(Enforcer):

    def verify(self, value) -> bool:
        """ Verify that the employee age is over 18 and under 65

        Args:
            arg1 (:obj:`type`): Positional parameter 1
                desc
            arg2 (:obj:`type`): keyword-only required argument

        Returns:
            (:obj)

        Raises:
            (:type)

        Examples:
              >>> a = AgeEnforcer()
              >>> a.verify(18)
              True
              >>> a.verify(60)
              True
              >>> a.verify(66)
              False
              >>> a.verify(0)
              False
        """
        # employee must be older than 18 and under 65
        return True if 18 <= value <= 65 else False

    def __repr__(self):
        return f'{self.__class__.__name__}({self._name})'

class NameEnforcer(Enforcer):

    def verify(self, value) -> bool:
        """ Verify that the employee name is over 3 characters and under or equal to 15 characters.

        Args:
            arg1 (:obj:`value`): Name to check
                desc

        Returns:
            (:obj bool)

        Raises:
            (:type)

        Examples:
              >>> n = NameEnforcer()
              >>> n.verify('Joe')
              True
              >>> n.verify('Jordan')
              True
              >>> n.verify('')
              False
              >>> n.verify('Jordan Gregory Anderson')
              False
        """
        return True if 3 <= len(value) <= 15 else False

    def __repr__(self):
        return f'{self.__class__.__name__}({self._name})'


class EmailEnforcer(Enforcer):

    def verify(self, value: str) -> bool:
        """ Use regex to validate email address.
            regex pattern:
            ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$
            Examples:
            Valid:
            "user@example.com"
            "first.last@sub.domain.co"
            Invalid:
            "user@"
            "@domain.com"
            "user@domain"
            This pattern:

            Requires at least one character before and after the @
            Allows dots and hyphens in the domain part
            Requires a top-level domain with 2+ letters (e.g. .com, .net, .io)

        Args:
            arg1 (:obj:`str`): Email to be checked
                desc

        Returns:
            (:obj bool)

        Examples:
              >>> e = EmailEnforcer()
              >>> e.verify('jordan.anderson@gmail.com')
              True
              >>> e.verify('joeblow@hotmail.ca')
              True
              >>> e.verify('')
              False
              >>> e.verify('notanemail!!__')
              False
        """
        ## TODO getting syntax warning  "\." is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\."? A raw string is also an option.
        email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

        return True if email_pattern.match(value) else False

    def __repr__(self):
        return f'{self.__class__.__name__}({self._name})'


class PostalCodeEnforcer(Enforcer):

    def verify(self, value) -> bool:
        """ Use regex to validate Postal Code.

        The pattern must match Capital Letter | Digit | Capital Letter | White Space | Digit | Capital Letter | Digit

        Args:
            arg1 (:obj:`value`): Postal Code to be checked

        Returns:
            (:obj bool)

        Raises:
            (:type)

        Examples:
              >>> pc = PostalCodeEnforcer()
              >>> pc.verify('S4S 0A2')
              True
              >>> pc.verify('S0H 3G0')
              True
              >>> pc.verify('')
              False
              >>> pc.verify('A34L09')
              False
        """

        pattern = re.compile(r'[A-Z]\d[A-Z]\s\d[A-Z]\d')

        return True if pattern.match(value) else False


class Employee:

    # overriding descriptors
    age = AgeEnforcer()
    name = NameEnforcer()
    email = EmailEnforcer()
    postal_code = PostalCodeEnforcer()

    def __init__(self, age: int, name: str, email: str, postal_code: str):
        self.age = age
        self.name = name
        self.email = email
        self.postal_code = postal_code
        self.employee_id:str|None = None

    def make_new_employee_id(self, chars: int):
        self.employee_id = ''
        for _ in range(chars):
            self.employee_id += str(randint(0, 9))
        logger.info(f'Making new employee id for {self.name}')

    def is_eligible_to_work(self) -> bool:
        return True if self.employee_id else False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"'Age': {self.age}, 'Name': {self.name}, 'Email': {self.email}, 'Postal Code': {self.postal_code}"


if __name__ == '__main__':

    # another way of testing the classes without having to instantiate an instance each time
    # doctest.testmod(extraglobs={'pc': PostalCodeEnforcer(),
    #                             'e': EmailEnforcer(),
    #                             'n': NameEnforcer(),
    #                             'a': AgeEnforcer(),})

    # ignore syntax warning for regex
    # warnings.filterwarnings('ignore')
    doctest.testmod()

    jordan = Employee(age=27, name="Jordan", email="jordan.anderson@gmail.com", postal_code="S4S 0A2")
    jordan.make_new_employee_id(10)

    print(jordan)

    pass