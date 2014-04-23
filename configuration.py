"""
state-name {symbol-type op[,op]* next-state}*

op -> L | R | Psymbol | E
next-state -> state-name
symbol-type -> None | Any | symbol | not symbol
"""


def P(symbol):
    return lambda machine: machine.p(symbol)

P1 = P('1')
P0 = P('0')
E = lambda machine: machine.e()
L = lambda machine: machine.l()
R = lambda machine: machine.r()

config_one_third = {
    'print-0': {
        ' ': ([P0, R], 'print-1')
    },
    'print-1': {
        ' ': ([P1, R], 'print-0')
    }
}


config_escalated_ones = {
    'init': {
        ' ': ([P('a'), R, P('a'), R, P0, R, R, P0, L, L], 'mark-1')
    },
    'mark-1': {
        '1': ([R, P('x'), L, L, L], 'mark-1'),
        '0': ([], 'print-1')
    },
    'print-1': {
        '0': ([R, R], 'print-1'),
        '1': ([R, R], 'print-1'),
        ' ': ([P1, L], 'rollback')
    },
    'rollback': {
        'x': ([E, R], 'print-1'),
        'a': ([R], 'print-0'),
        ' ': ([L, L], 'rollback')
    },
    'print-0': {
        '0': ([R, R], 'print-0'),
        '1': ([R, R], 'print-0'),
        ' ': ([P0, L, L], 'mark-1')
    }
}


# todo: write a configuration interpreter

class ConfigurationError(Exception):
    pass

class Configuration:
    def __init__(self, config):
        self.config = config

    def move(self, state, symbol, machine):
        try:
            action = self.config[state][symbol]
        except KeyError:
            raise ConfigurationError('at state %s, symbol %s' % (state, symbol))

        op_list, next_state = action
        for op in op_list:
            op(machine)
        return next_state
