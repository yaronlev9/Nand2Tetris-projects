class Parser:
    """
      Class for reading vm instructions and translating them
      into asm
      """
    STATIC_START = 16
    TEMP_START = 5

    def __init__(self):
        """
        Ctor
        _file: file to parse (read, not write)
        _data: store parsed data to write later
        _result: store translated data
        _commands: all legal operations
        _counter: counts the comparison operations
        _segments: all segments
        _asm segments: the asm segments
        """
        self._file = None
        self._data = []
        self._result = []
        self._counter = 0
        self._return_counter = 0
        self._cur_func = None
        self._commands = {'add': ['@SP',
                                  'AM=M-1',
                                  'D=M',
                                  'A=A-1',
                                  'M=M+D'],
                          'sub': ['@SP',
                                  'AM=M-1',
                                  'D=M',
                                  'A=A-1',
                                  'M=M-D'],
                          'neg': ['D=0',
                                  '@SP',
                                  'A=M-1',
                                  'M=D-M'],
                          'and': ['@SP',
                                  'AM=M-1',
                                  'D=M',
                                  'A=A-1',
                                  'M=M&D'],
                          'or': ['@SP',
                                 'AM=M-1',
                                 'D=M',
                                 'A=A-1',
                                 'M=M|D'],
                          'not': ['@SP',
                                  'A=M-1',
                                  'M=!M']}
        self._segments = {'temp', 'that', 'this', 'local', 'argument'}
        self._asm_segments = ['LCL', 'ARG', 'THIS', 'THAT']

    def comparison_format(self, command):
        """
        Format for comparison commands translation
        :param command:
        :return the asm string:
        """
        if command == 'eq':
            # assembly translation for eq
            return '@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE'+str(self._counter)+'\nD;JNE\n@SP\nA=M-1\nM=-1\n@SKIP' + \
                str(self._counter) + '\n0;JMP\n(FALSE'+str(self._counter) + ')\n@SP\nA=M-1\nM=0\n(SKIP' + \
                str(self._counter) + ')\n'
        elif command == 'lt':
            # assembly translation for lt
            return '@SP\nAM=M-1\nA=A-1\nD=M\n@POS_X'+str(self._counter)+'\nD;JGE\n(NEG_X'+str(self._counter) + \
                   ')\n@SP\nA=M\nD=M\n@TRUE'+str(self._counter) + '\nD;JGE\n@END'+str(self._counter) + \
                   '\n0;JMP\n(POS_X' + \
                   str(self._counter) + ')\n@SP\nA=M\nD=M\n@FALSE'+str(self._counter) + '\nD;JLT\n(END' + \
                   str(self._counter) + ')\n@SP\nA=M\nD=M\nA=A-1\nD=M-D\n@TRUE' + str(self._counter) + \
                   '\nD;JLT\n(FALSE' + \
                   str(self._counter) + ')\nD=0\n@SET'+str(self._counter) + '\n0;JMP\n(TRUE' + str(self._counter) + \
                   ')\nD=-1\n(SET'+str(self._counter) + ')\n@SP\nA=M-1\nM=D\n'
        elif command == 'gt':
            # assembly translation for gt
            return '@SP\nAM=M-1\nA=A-1\nD=M\n@POS_X' + str(self._counter) + '\nD;JGE\n(NEG_X'+str(self._counter) + \
                   ')\n@SP\nA=M\nD=M\n@FALSE' + str(self._counter) + '\nD;JGE\n@END' + str(self._counter) + \
                   '\n0;JMP\n(POS_X' + \
                   str(self._counter) + ')\n@SP\nA=M\nD=M\n@TRUE' + str(self._counter) + '\nD;JLT\n(END' + \
                   str(self._counter) + ')\n@SP\nA=M\nD=M\nA=A-1\nD=M-D\n@TRUE' + str(self._counter) + \
                   '\nD;JGT\n(FALSE'+str(self._counter) + ')\nD=0\n@SET' + str(self._counter) + '\n0;JMP\n(TRUE' + \
                   str(self._counter) + ')\nD=-1\n(SET' + str(self._counter) + ')\n@SP\nA=M-1\nM=D\n'

    def push_formant1(self, segment):
        """
        First format for push translation
        :param segment:
        :return the asm string:
        """
        return '@'+segment+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

    def push_formant2(self, segment, num):
        """
        Second format for push translation
        :param segment:
        :param num:
        :return the asm string:
        """
        memory = int(num)
        if segment == 'temp':
            seg = 'R5'
            memory = int(num) + Parser.TEMP_START
            return "@" + str(memory) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == 'that':
            seg = 'THAT'
        elif segment == 'this':
            seg = 'THIS'
        elif segment == 'local':
            seg = 'LCL'
        else:
            seg = 'ARG'
        return '@'+str(memory)+'\nD=A\n@'+seg+'\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

    def pop_formant1(self, segment):
        """
        First format for pop translation
        :param segment:
        :return the asm string:
        """
        return '@'+segment+'\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'

    def pop_formant2(self, segment,num):
        """
        Second format for pop translation
        :param segment:
        :param num:
        :return the asm string:
        """
        if segment == 'temp':
            memory = int(num) + Parser.TEMP_START
            return "@"+str(memory)+"\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == 'that':
            seg = 'THAT'
        elif segment == 'this':
            seg = 'THIS'
        elif segment == 'local':
            seg = 'LCL'
        else:
            seg = 'ARG'
        return '@' + seg + '\nD=M\n@' + num + '\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'


    def write_init(self):
        """
        Return function initialization lines
        :return:
        """
        line1 = "@256\nD=A\n@SP\nM=D\n"
        line2 = self.write_call("Sys.init", 0)
        return line1 + line2


    def write_call(self, func_name, num_args):
        """
        Write call lines
        :param func_name:
        :param num_args:
        :return:
        """
        # Construct label according to name of function and arguments
        return_label = func_name + "$" + "ret" + str(self._return_counter)
        line = "@" + return_label + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # Save caller state
        for item in self._asm_segments:
            line += "@" + item + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        # Jump to return
        line += "@SP\nD=M\n@"+str(int(num_args)+int(5))+"\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@" + \
            func_name + "\n0;JMP\n(" + return_label + ")\n"
        self._return_counter +=1
        return line


    def write_return(self):
        """
        Write return statement
        :return:
        """
        pop_arg_0 = '@ARG\nD=M\n@0\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'
        line =  "@LCL\nD=M\n@R14\nM=D\n@5\nD=A\n@R14\nD=M-D\nA=D\nD=M\n@R15\nM=D\n" + pop_arg_0 + \
                "@ARG\nD=M\n@SP\nM=D+1\n"
        line += self.return_pointers('THAT')
        line += self.return_pointers('THIS')
        line += self.return_pointers('ARG')
        line += self.return_pointers('LCL')
        line += "@R15\nA=M\n0;JMP\n"
        return line

    def return_pointers(self,segment):
        """
        returns the pointers to their correct place
        :param segment:
        :return:
        """
        return "@R14\nAM=M-1\nD=M\n@"+segment+"\nM=D\n"

    def write_lable(self, label_name):
        """
        Define label name according to encapsulating function
        :param label_name:
        :return:
        """
        return "(" + label_name + ")\n"

    def write_if_goto(self, label_name):
        """
        Define if goto according to label
        :param label_name:
        :return:
        """
        return "@SP\nAM=M-1\nD=M\n@" + label_name + "\nD;JNE\n"


    def write_goto(self, label_name):
        """
        Define goto according to label
        :param label_name:
        :return:
        """
        return "@" + label_name + "\n0;JMP\n"


    def write_function(self, func_name, num_args):
        """
        Write function lines
        :param func_name:
        :param num_args:
        :return:
        """
        line = "(" + func_name + ")\n"
        # Create space in stack for function arguments
        for i in range(int(num_args)):
            line += "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        return line


    def is_valid_line(self, line):
        """
        Make sure line is valid vm line
        :param line:
        :return:
        """
        temp = line.split(' ')
        # check if arithmetic command
        if (temp[0] in self._commands or temp[0] in {'eq', 'gt', 'lt'}) and temp[0] not in {'push', 'pop'}:
            return len(temp) == 1
        elif temp[0] in {'push', 'pop'}:
            if len(temp) > 1:
                if (temp[1] in self._segments or temp[1] in {'pointer', 'static', 'constant'}) and len(temp) == 3:
                    return True
                elif temp[1] not in self._segments and len(temp) == 2:
                    return 0 <= temp[1] <= 32767
        elif temp[0] in {'label', 'goto', 'if-goto'}:
            return len(temp) == 2
        elif temp[0] in {'call','function'}:
            return len(temp) == 3
        elif temp[0] == 'return':
            return len(temp) == 1
        return False

    def read(self, filepath):
        """
        Read vm file while removing comments and blank lines
        :param filepath:
        :return:
        """
        if filepath.endswith('.vm'):
            with open(filepath, 'r') as self._file:
                # Remove unnecessary lines
                for line in self._file:
                    temp = ' '.join(line.split('//')[0].split())
                    if self.is_valid_line(temp):
                        self._data.append(temp)
                self._file.close()

    def write(self, filename):
        """
        Write stored data into file represented by filename
        :param filename:
        """
        if not filename.endswith('.asm'):
            return
        result = open(filename, 'w')
        for line in self._result:
            result.write(line)
        result.close()

    def vm_to_asm_line(self, line):
        """
        Translate single line from asm to binary
        :param line:
        :return the binary string:
        """
        temp = line.split(' ')
        # if not comparison command or push pop command
        if temp[0] in self._commands and temp[0] not in {'push', 'pop','lt','gt','eq'}:
            for line in self._commands[temp[0]]:
                self._result.append(line + '\n')
        elif temp[0] in {'eq', 'gt', 'lt'}: #if comparison command
            self._result.append(self.comparison_format(temp[0]))
            self._counter += 1
        elif temp[0] in {'push','pop'}:
            if temp[0] == 'push':
                if temp[1] in self._segments:
                    self._result.append(self.push_formant2(temp[1],temp[2]))
                elif temp[1] == 'static':
                    if self._cur_func == None:
                        self._result.append(self.push_formant1(str(int(temp[2])+Parser.STATIC_START)))
                    else:
                        self._result.append(self.push_formant1(
                            self._cur_func.split('.')[0] + '.' + str(int(temp[2]) + Parser.STATIC_START)))
                elif temp[1] == 'pointer' and temp[2] == '0':
                    self._result.append(self.push_formant1('THIS'))
                elif temp[1] == 'pointer' and temp[2] == '1':
                    self._result.append(self.push_formant1('THAT'))
                elif temp[1] == 'constant':
                    self._result.append('@'+str(temp[2])+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            else: #if pop command
                if temp[1] in self._segments:
                    self._result.append(self.pop_formant2(temp[1],temp[2]))
                elif temp[1] == 'static':
                    if self._cur_func == None:
                        self._result.append(self.pop_formant1(str(int(temp[2])+Parser.STATIC_START)))
                    else:
                        self._result.append(self.pop_formant1(
                            self._cur_func.split('.')[0] + '.' + str(int(temp[2]) + Parser.STATIC_START)))
                elif temp[1] == 'pointer' and temp[2] == '0':
                    self._result.append(self.pop_formant1('THIS'))
                elif temp[1] == 'pointer' and temp[2] == '1':
                    self._result.append(self.pop_formant1('THAT'))
        elif temp[0] == 'label':
            label_name = temp[1]
            if self._cur_func != None:
                label_name = self._cur_func + "$" + temp[1]
            self._result.append(self.write_lable(label_name))
        elif temp[0] == 'function':
            self._cur_func = temp[1]
            self._result.append(self.write_function(temp[1], temp[2]))
        elif temp[0] == 'return':
            self._result.append(self.write_return())
        elif temp[0] == 'call':
            self._result.append(self.write_call(temp[1], temp[2]))
        elif temp[0] == 'goto':
            label_name = temp[1]
            if self._cur_func != None:
                label_name = self._cur_func + "$" + temp[1]
            self._result.append(self.write_goto(label_name))
        elif temp[0] == 'if-goto':
            label_name = temp[1]
            if self._cur_func != None:
                label_name = self._cur_func + "$" + temp[1]
            self._result.append(self.write_if_goto(label_name))


    def vm_to_asm(self):
        """
        Translate stored data from vm to asm
        """
        self._result.append(self.write_init())
        for i in range(len(self._data)):
            if self._data[i] == "end_file\n":
                self._cur_func = None
                continue
            self._result.append('//'+self._data[i]+'\n')
            self.vm_to_asm_line(self._data[i])
