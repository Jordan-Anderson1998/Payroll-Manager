from employee import Employee
from payroll_hub import PayrollHub

class Model:
    """
    Model is responsible for instantiating the payroll hub, which controls the methods for dealing with employees.
    """

    def __init__(self, hub: PayrollHub = None):
        self.hub = hub

    def add_hub(self, hub: PayrollHub):
        self.hub = hub


class Controller:
    pass


class View:
    pass