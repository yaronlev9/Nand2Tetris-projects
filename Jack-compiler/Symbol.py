"""
Class for each Symbol with 4 attributes
"""
class Symbol:

    def __init__(self, name, type, kind, number):
        """
        Ctor
        _name: the name of the symbol
        _type: the type of the symbol
        _kind: the kind of the symbol
        _number: the number of the symbol
        """
        self._name = name
        self._type = type
        self._kind = kind
        self._number = number

    def get_kind(self):
        """
        returns the kind of the symbol
        :return: self._kind
        """
        if self._kind == 'field':
            return 'this'
        return self._kind

    def get_number(self):
        """
        returns the number of the symbol
        :return: self._number
        """
        return self._number

    def get_type(self):
        """
        returns the type of the symbol
        :return: self._type
        """
        return self._type

    def get_name(self):
        """
        returns the name of the symbol
        :return: self._name
        """
        return self._name