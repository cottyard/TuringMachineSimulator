from abc import ABCMeta, abstractmethod


class ExtensibleList:
    def __init__(self, default_value):
        self.list = []
        self.default_value = default_value

    def __getitem__(self, index):
        try:
            return self.list[index]
        except IndexError:
            return self.default_value

    def __setitem__(self, index, value):
        try:
            self.list[index] = value
        except IndexError:
            if index < 0:
                raise NotSupportedIndex
            to_add = index + 1 - len(self.list)
            self.list.extend([self.default_value] * to_add)
            self.list[index] = value

    def __iter__(self):
        return iter(self.list)


class Tape:
    figures = ('1', '0')
    def __init__(self):
        self._tape = ExtensibleList(' ')
        self._figure_count = 0

    def show_all(self):
        print ''.join(self._tape).rstrip()

    def show_output(self):
        print ''.join(filter(lambda s: s in Tape.figures, self._tape))

    def write(self, square, symbol):
        self._tape[square] = symbol
        if symbol in Tape.figures:
            self._figure_count += 1

    def erase(self, square):
        if self._tape[square] in Tape.figures:
            self._figure_count -= 1
        self._tape[square] = ' '

    def read(self, square):
        return self._tape[square]

    def figure_count(self):
        return self._figure_count


class TuringMachine:
    __metaclass__ = ABCMeta
    @abstractmethod
    def r(self):
        pass
    @abstractmethod
    def l(self):
        pass
    @abstractmethod
    def p(self, symbol):
        pass
    @abstractmethod
    def e(self):
        pass


class Machine(TuringMachine):
    def __init__(self):
        self.tape = None
        self.position = None
        self.config = None
        self.state = None

    def install_tape(self, tape, position):
        self.tape = tape
        self.position = position

    def install_configuration(self, config, begin_state):
        self.config = config
        self.state = begin_state

    def r(self):
        self.position += 1

    def l(self):
        if self.position <= 0:
            raise InvalidMachineOperation('trying moving off the tape head')
        self.position -= 1

    def p(self, symbol):
        self.tape.write(self.position, symbol)

    def e(self):
        self.tape.erase(self.position)

    def show_position(self):
        print ' ' * self.position + '^'

    def scanned_symbol(self):
        return self.tape.read(self.position)

    def show_mconfig(self):
        if self.config is not None:
            print 'state:', self.state

    def move_to_next_state(self):
        self.state = self.config.move(
            self.state,
            self.scanned_symbol(),
            self
        )

    def run(self, output_length=None):
        if output_length is None:
            self.move_to_next_state()
        else:
            while self.tape.figure_count() < output_length:
                self.move_to_next_state()


class InvalidMachineOperation(Exception):
    pass


class NotSupportedIndex(Exception):
    pass