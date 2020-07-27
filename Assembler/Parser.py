class Parser:
    """
    Class for reading assembler instructions and translating them
    into binary code
    """

    def __init__(self):
        """
        Ctor
        _file: file to parse (read, not write)
        _data: store parsed data to write later
        _result: store translated data
        _next_mem_slot: keep track of index for storing labels/variables
        _symbol_table: all reserved keywords + new ones introduced in file
        _registers: all types of register arguments
        _commands: all legal operations
        _jumps: all jumps conditions
        """
        self._file = None
        self._data = []
        self._result = []
        self._next_mem_slot = 0
        self._symbol_table = {'SP': 0,
                              'LCL': 1,
                              'ARG': 2,
                              'THIS': 3,
                              'THAT': 4,
                              'R0': 0,
                              'R1': 1,
                              'R2': 2,
                              'R3': 3,
                              'R4': 4,
                              'R5': 5,
                              'R6': 6,
                              'R7': 7,
                              'R8': 8,
                              'R9': 9,
                              'R10': 10,
                              'R11': 11,
                              'R12': 12,
                              'R13': 13,
                              'R14': 14,
                              'R15': 15,
                              'SCREEN': 16384,
                              'KBD': 24576}
        self._registers = {'0': '000',
                           'M': '001',
                           'D': '010',
                           'MD': '011',
                           'A': '100',
                           'AM': '101',
                           'AD': '110',
                           'AMD': '111'}
        self._commands = {'0': '110101010',
                          '1': '110111111',
                          '-1': '110111010',
                          'D': '110001100',
                          'A': '110110000',
                          '!D': '110001101',
                          '!A': '110110001',
                          '-D': '110001111',
                          '-A': '110110011',
                          'D+1': '110011111',
                          'A+1': '110110111',
                          'D-1': '110001110',
                          'A-1': '110110010',
                          'D+A': '110000010',
                          'D-A': '110010011',
                          'A-D': '110000111',
                          'D&A': '110000000',
                          'D|A': '110010101',
                          'M': '111110000',
                          '!M': '111110001',
                          '-M': '111110011',
                          'M+1': '111110111',
                          'M-1': '111110010',
                          'D+M': '111000010',
                          'D-M': '111010011',
                          'M-D': '111000111',
                          'D&M': '111000000',
                          'D|M': '111010101',
                          'D<<': '010110000',
                          'A<<': '010100000',
                          'M<<': '011100000',
                          'D>>': '010010000',
                          'A>>': '010000000',
                          'M>>': '011000000'}
        self._jumps = {'0': '000',
                       'JGT': '001',
                       'JEQ': '010',
                       'JGE': '011',
                       'JLT': '100',
                       'JNE': '101',
                       'JLE': '110',
                       'JMP': '111'}

    def read(self, filepath):
        """
        Read from file represented by filepath
        :param filepath:
        """
        if filepath.endswith('.asm'):
            with open(filepath, 'r') as self._file:
                # Add all relevant lines, i.e. not comments ('//'), or empty lines,
                # or lines that don't start with '@', '(', or a valid register
                for line in self._file:
                    temp = line.split('//')[0].replace(' ', '').rstrip()
                    if len(temp) > 0 and (temp[0] == '@' or temp[0] == '(' or temp[0] in self._registers):
                        self._data.append(temp)
                self._file.close()

    def write(self, filename):
        """
        Write stored data into file represented by filename
        :param filename:
        """
        if not filename.endswith('.hack'):
            return
        result = open(filename, 'w')
        for line in self._result:
            result.write(line)
        result.close()

    def label_parse(self):
        """
        First read through the file, map labels and variables to memory slots
        """
        # map labels
        for line in self._data:
            if len(line) > 0 and line[0] == '(':
                temp = line.split(')')[0][1:]
                self._symbol_table[temp] = self._next_mem_slot
                self._next_mem_slot -= 1
            self._next_mem_slot += 1
        self._next_mem_slot = 16
        # map remaining variables or label a-commands
        for line in self._data:
            if len(line) > 0 and line[0] == '@':
                temp = line[1:].rstrip()
                if temp not in self._symbol_table and not temp.isdigit():
                    self._symbol_table[temp] = self._next_mem_slot
                    self._next_mem_slot += 1


    def asm_to_binary_line(self, line):
        """
        Translate single line from asm to binary
        :param line:
        :return the binary string:
        """
        # A-Command case
        if line[0] == '@':
            if line[1:].isdigit():
                a_comm = str("{:015b}".format(int(line[1:])))
            else:
                a_comm = str("{:015b}".format(self._symbol_table[line[1:]]))
            return '0'+a_comm+'\n'
        # Skip labels
        elif line[0] == '(':
            return ''
        # C-Command
        else:
            c_comm = '1' # Determine register on which we're operating
            reg = ''
            for prefix in self._registers:
                if line.startswith(prefix):
                    reg = prefix
            # Handle jump command case
            temp_line = line.split(';')
            if len(temp_line) > 2:
                return
            if len(temp_line[0]) == 1:
                c_comm += self._commands[temp_line[0][0]] + self._registers['0']
            elif temp_line[0] in list(self._commands)[-6:]: #checks if it's a shift operation with a jump and no dest
                c_comm += self._commands[temp_line[0]] + self._registers['0']
            elif temp_line[0][len(reg)] == '=': # Handle regular ALU operation
                if temp_line[0][len(reg)+1:] in self._commands:
                    c_comm += self._commands[temp_line[0][len(reg)+1:]] + self._registers[reg]
            # Add jump bits
            if len(temp_line) == 2:
                end = self._jumps[temp_line[1]]
            else:
                end = self._jumps['0']
            return c_comm+end+'\n'

    def asm_to_binary(self):
        """
        Translate stored data from asm to binary
        """
        self.label_parse()
        for i in range(len(self._data)):
            temp = self.asm_to_binary_line(self._data[i])
            if temp != '':
                self._result.append(temp)

