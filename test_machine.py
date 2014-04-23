from machine import *
from configuration import *
import doctest


def new_machine():
    m = Machine()
    m.install_tape(Tape(), 0)
    return m


def complete_configuration(machine):
    machine.tape.show_all()
    machine.show_position()
    machine.show_mconfig()

def case_hi():
    """
>>> m = new_machine()
>>> m.p('h')
>>> m.r()
>>> m.p('i')
>>> m.l()
>>> complete_configuration(m)
hi
^
    """


def send_str(m, string):
    for s in string:
        m.p(s)
        m.r()


def case_hello_world():
    """
>>> m = new_machine()
>>> send_str(m, 'hello, world!')
>>> complete_configuration(m)
hello, world!
             ^
    """


def case_one_third():
    """
>>> m = new_machine()
>>> c = Configuration(config_one_third)
>>> m.install_configuration(c, 'print-0')
>>> m.run(20)
>>> m.tape.show_output()
01010101010101010101
    """

def case_escalated_ones():
    """
>>> m = new_machine()
>>> c = Configuration(config_escalated_ones)
>>> m.install_configuration(c, 'init')
>>> m.run(21)
>>> m.tape.show_output()
001011011101111011111
    """

doctest.testmod()