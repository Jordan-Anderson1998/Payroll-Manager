import pytest
from src.employee import *

def test_email():
    email_enforcer = EmailEnforcer()

    assert email_enforcer.verify('jordan.anderson@something.com') == True
    assert email_enforcer.verify('legit_email@yahoo.com') == True
    assert email_enforcer.verify('') == False
    assert email_enforcer.verify('notarealemail!!__') == False


def test_integer():
    int_enforcer = AgeEnforcer()

    for i in range(18):
        # if under 18
        assert int_enforcer.verify(i) == False

    for i in range(18, 65, 1):
        # if between 18 and 65
        assert int_enforcer.verify(i) == True

    # if over 65
    assert int_enforcer.verify(66) == False

    # assert int_enforcer.verify(18) == True
    # assert int_enforcer.verify(17) == False

def test_name():
    name_enforcer = NameEnforcer()

    assert name_enforcer.verify('Jordan') == True

    for name in names:
        assert name_enforcer.verify(name) == True

    # cannot use full name, names must be broken down into first, middle, last
    assert name_enforcer.verify('Jordan Gregory Anderson') == False
    assert name_enforcer.verify('') == False
    assert name_enforcer.verify('*' * 50) == False
