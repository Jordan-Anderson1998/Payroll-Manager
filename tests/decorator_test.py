import pytest
from src.payroll_hub import *
from tools.decorators.deco import output_formatter

@output_formatter('$', True)
def print_currency() -> str:

    return '1000'

@output_formatter('!', False)
def print_statement() -> str:

    return 'Hello There'

def test_string_transformer_decorator():
    employee = Employee(name='Todd', age=21, email='something@spam.ca', postal_code='S0H 3G0')
    payroll_hub = PayrollHub()
    expected_output = f'Added {employee.name} to employee list'.upper()
    func_output = payroll_hub.add_employee(employee)

    assert expected_output == func_output


def test_output_transformer_decorator():

    assert print_currency() == '$1000'
    assert print_statement() == 'Hello There!'