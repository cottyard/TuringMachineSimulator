from machine import *
from configuration import *
from msvcrt import getch
import time

def complete_configuration(machine):
    machine.tape.show_all()
    machine.show_position()
    machine.show_mconfig()

m = Machine()
m.install_tape(Tape(), 0)
c = Configuration(config_escalated_ones)
m.install_configuration(c, 'init')

while True:
    complete_configuration(m)
    print '=====================\n'
    m.run()
    getch()