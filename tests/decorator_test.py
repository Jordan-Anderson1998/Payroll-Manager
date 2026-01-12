import pytest
from src.payroll_hub import *

def test_string_transformer_decorator():
    employee = Employee(name='Todd', age=21, email='something@spam.ca', postal_code='S0H 3G0')
    payroll_hub = PayrollHub()
    expected_output = f'Added {employee.name} to employee list'.upper()
    func_output = payroll_hub.add_employee(employee)

    assert expected_output == func_output
