class SymbolTable:
    """
    Symbol table for classes/subroutines
    """

    def __init__(self, class_table=None):
        """
        Ctor
        _class_table: a list of all the symbol in the class
        _symbols: a list of all the symbols in the subroutine
        _counters: the counters of the different kinds
        """
        self._class_table = class_table
        self._symbols = []
        self._counters = {'static': 0, 'field': 0, 'argument': 0, 'local': 0}

    def get_counters(self):
        """
        returns the counters
        :return: self._counters
        """
        return self._counters

    def get_symbol(self, name):
        """
        returns the symbol based on the name
        :param name:
        :return: symbol
        """
        for symbol in self._symbols:
            if symbol.get_name() == name:
                return symbol
        if self._class_table:
            for symbol in self._class_table:
                if name == symbol.get_name():
                    return symbol

    def add_symbol(self, symbol):
        """
        appends the symbol to the list of symbols
        :param symbol:
        :return:
        """
        self._symbols.append(symbol)
