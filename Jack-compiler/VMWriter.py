class VMWriter:
    """
    Writes VM code
    """
    def __init__(self):
        """
        Ctor
        _result: a list of all the lines to be written in the new file
        """
        self._result = []

    def write(self, filename):
        """
        Write stored data into file represented by filename
        :param filename:
        """
        result = open(filename, 'w')
        for line in self._result:
            result.write(line)
        result.close()

    def write_push(self, segment, index):
        """
        Writes a VM push command
        :param segment:
        :param index:
        :return:
        """
        self._result.append("push " + segment + " "+ str(index)+"\n")

    def write_pop(self, segment, index):
        """
        Writes a VM pop command
        :param segment:
        :param index:
        :return:
        """
        self._result.append("pop " + segment + " "+ str(index)+"\n")

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command:
        :return:
        """
        self._result.append(command+"\n")

    def write_label(self, label):
        """
        Writes a VM label command
        :param label:
        :return:
        """
        self._result.append("label " + label+"\n")

    def write_goto(self, label):
        """
        Writes a VM goto command
        :param label:
        :return:
        """
        self._result.append("goto " + label+"\n")

    def write_if(self, label):
        """
        Writes a VM if command
        :param label:
        :return:
        """
        self._result.append("if-goto " + label+"\n")

    def write_call(self, name, n_args):
        """
        Writes a VM call command
        :param name:
        :param n_args:
        :return:
        """
        self._result.append("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        """
        Writes a VM function command
        :param name:
        :param n_locals:
        :return:
        """
        self._result.append("function " + name + " " + str(n_locals) + "\n")

    def write_return(self):
        """
        Writes a VM return command
        :return:
        """
        self._result.append("return\n")

    def write_memory(self):
        """
        Writes to memory
        :return:
        """
        self._result.append("call Memory.alloc 1\n")

    def write_true(self):
        """
        Writes the true operations
        :return:
        """
        self.write_push("constant", 0)
        self.write_arithmetic("not")

    def write_this(self):
        """
        Writes the this operations
        :return:
        """
        self.write_push("pointer", 0)

    def write_false_or_null(self):
        """
        Writes the false or null operations
        :return:
        """
        self.write_push("constant", 0)

    def write_keywordConstants(self,keyword):
        """
        calls the right function based on the keyword
        :param keyword:
        :return:
        """
        if keyword == "true":
            self.write_true()
            return
        elif keyword == "this":
            self.write_this()
        else:
            self.write_false_or_null()


