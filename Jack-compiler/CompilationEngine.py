from Symbol import *
from SymbolTable import *
from VMWriter import *
"""
Class for reading the commands and compiles it
"""
class CompilationEngine:
    op = {'+': 'add', '-': 'sub', '*': "call Math.multiply 2", '/': "call Math.divide 2",
          '&amp;': 'and', '|': 'or','&lt;': 'lt', '&gt;': 'gt', '=': 'eq', '&quot;':None}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, tokenizer):
        """
        Ctor
        _writer: a VM writer object
        _cur_class: the current class
        _cur_func: the current function
        _cur_func_type: the current function type
        _subroutine_table: a symbol table of the subroutine
        _class_table: a list of the symbols in the class
        _tokenizer: the tokenizer object
        _result: a list that is written in the output file
        counters: the kind counters
        label_counters: the label counters
        """
        self._writer = VMWriter()
        self._cur_class = None
        self._cur_func = None
        self._cur_func_type = None
        self._subroutine_table = None
        self._class_table = []
        self._tokenizer = tokenizer
        self._result = []
        self.counters = {'static': 0, 'field': 0, 'argument': 0, 'local': 0}
        self.label_counters = {"if":0,"while":0}
        self.compileClass()

    def write(self, filename):
        """
        Write stored data into file represented by filename
        :param filename:
        """
        self._writer.write(filename)

    def reset_label(self):
        """
        resets the labels to 0
        :return:
        """
        for i in self.label_counters:
            self.label_counters[i] = 0

    def terminal(self, type, token):
        """
        write the terminal rule
        :param type:
        """
        self._result.append("<"+type+"> "+token+" </"+type+">\n")

    def get_next(self):
        """
        gets the next token and type
        :return type:
        :return token:
        """
        if self._tokenizer.has_more_tokens():
            type, token = self._tokenizer.get_token()
            return type, token
        else:
            return

    def get_current(self):
        """
        gets the current token and type
        :return type:
        :return token:
        """
        type, token = self._tokenizer.get_token()
        return type, token

    def compileClass(self):
        """
        compiles a complete class.
        """
        type, token = self.get_next()
        self.terminal(type, token)  # get 'class' keyword
        type, token = self.get_next()
        self._cur_class = token
        self.terminal(type, token)  # get class name
        type, token = self.get_next()
        self.terminal(type, token)  # get '{' symbol
        type, token = self.get_next()
        while self.isClassVarDec(token):
            self.compileClassVarDec()
            type, token = self.get_next()
        while self.isSubroutineDec(token):
            self.reset_label()
            self.compileSubroutineDec()
            type, token = self.get_next()
            if token == '}':
                break
        self.terminal(type, token) # get '}' symbol

    def isClassVarDec(self,token):
        """
        checks if the beginning of a classVerDec returns true or false
        """
        if token == "field" or token == "static":
            return True
        return False

    def isSubroutineDec(self,token):
        """
        checks if the beginning of a subroutineDec returns true or false
        """
        if token == "method" or token == "function" or token == "constructor":
            return True
        return False

    def compileClassVarDec(self):
        """
        compiles a classVerDec
        """
        type, token = self.get_current()
        var_kind = token
        self.terminal(type, token)  # get 'static' or 'field'
        type, token = self.get_next()
        var_type = token
        self.terminal(type, token)  # get var type
        type, token = self.get_next()
        var_name = token
        self.terminal(type, token)  # get var name
        self._class_table.append(Symbol(var_name,var_type,var_kind,self.counters[var_kind]))
        self.counters[var_kind] +=1
        type, token = self.get_next()
        while token == ",":
            self.terminal(type, token)  # get ',' symbol
            type, token = self.get_next()
            self.terminal(type, token) # get var name
            var_name = token
            self._class_table.append(Symbol(var_name,var_type,var_kind,self.counters[var_kind]))
            self.counters[var_kind] +=1
            type, token = self.get_next()
        self.terminal(type, token)  # get ';' symbol

    def compileSubroutineDec(self):
        """
        compiles a subroutineDec
        """
        type, token = self.get_current()
        self._subroutine_table = SymbolTable(self._class_table)
        self._cur_func_type = token
        self.terminal(type, token)  # get subroutine
        type, token = self.get_next()
        if self._cur_func_type == "method":
            self._subroutine_table.add_symbol(Symbol("this",self._cur_class,"argument", 0))
            self._subroutine_table.get_counters()["argument"] += 1
        self.terminal(type, token)  # get subroutine return type
        type, token = self.get_next()
        self._cur_func = token
        self.terminal(type, token)  # get subroutine name
        type, token = self.get_next()
        self.terminal(type, token)  # get '(' symbol
        type, token = self.get_next()
        self.compileParameterList()
        type, token = self.get_current()
        self.terminal(type, token)  # get ')' symbol
        self.compileSubroutineBody()

    def compileParameter(self):
        """
        compiles a parameter
        """
        type, token = self.get_current()
        argument_type = token
        self.terminal(type, token)  # get parameter type
        type, token = self.get_next()
        argument_name = token
        self._subroutine_table.add_symbol(Symbol(argument_name,argument_type,"argument",
                                                 self._subroutine_table.get_counters()["argument"]))
        self._subroutine_table.get_counters()["argument"] +=1
        self.terminal(type, token)  # get parameter name

    def compileParameterList(self):
        """
        compiles a parameter list
        """
        type,token = self.get_current()
        if token ==")":
            return
        self.compileParameter()
        type, token = self.get_next()
        while token == ",":
            self.terminal(type, token) # get ',' symbol
            type, token = self.get_next()
            self.compileParameter()
            type, token = self.get_next()

    def compileSubroutineBody(self):
        """
        compiles a subroutineBody
        """
        type, token = self.get_next()
        self.terminal(type, token)  # get '{' symbol
        type, token = self.get_next()
        while token == "var":
            self.compileVarDec()
            type, token = self.get_next()
        self._writer.write_function(self._cur_class + '.' + self._cur_func,
                                    self._subroutine_table.get_counters()["local"])
        if self._cur_func_type == "constructor":
            self._writer.write_push("constant", self.counters["field"])
            self._writer.write_memory()
            self._writer.write_pop("pointer", 0)
        elif self._cur_func_type == "method":
            self._writer.write_push("argument", 0)
            self._writer.write_pop("pointer", 0)
        self.compileStatements(type, token)
        type, token = self.get_current()
        self.terminal(type, token)  # get '}' symbol

    def compileVarDec(self):
        """
        compiles a varDec.
        """
        type, token = self.get_current()
        self.terminal(type, token)  # get 'var' keyword
        type, token = self.get_next()
        var_type = token
        self.terminal(type, token)  # get var type
        type, token = self.get_next()
        var_name = token
        self._subroutine_table.add_symbol(Symbol(var_name,var_type,"local",
                                                 self._subroutine_table.get_counters()["local"]))
        self._subroutine_table.get_counters()["local"] +=1
        self.terminal(type, token)  # get var name
        type, token = self.get_next()
        while token == ",":
            self.terminal(type, token)  # get ',' symbol
            type, token = self.get_next()
            var_name = token
            self._subroutine_table.add_symbol(Symbol(var_name,var_type,"local",
                                                     self._subroutine_table.get_counters()["local"]))
            self._subroutine_table.get_counters()["local"] +=1
            self.terminal(type, token)  # get var name
            type, token = self.get_next()
        self.terminal(type, token)  # get ';' symbol

    def compileStatements(self,type,token):
        """
        compiles the statements
        """
        while token in ["do","let","if","while","return"]:
            if   token == "do":
                self.compileDo(type, token)
            elif token == "let":
                self.compileLet(type, token)
            elif token == "if":
                self.compileIf(type, token)
                type,token = self.get_current()
                continue
            elif token == "while":
                self.compileWhile(type, token)
            elif token == "return":
                self.compileReturn(type, token)
            type, token = self.get_next()

    def compileDo(self, type, token):
        """
        compiles a do statement
        """
        self.terminal(type, token)  # get 'do' keyword
        self.compileSubroutineCall()
        type, token = self.get_next()
        self.terminal(type, token)  # get ';' symbol

    def compileLet(self, type, token):
        """
        compiles a let statement
        """
        self.terminal(type, token)  # get 'let' keyword
        type, token = self.get_next()
        symbol = self._subroutine_table.get_symbol(token)
        self.terminal(type, token)  # get var name
        type, token = self.get_next()
        if token =="[":  #case of varName[expression]
            self.terminal(type, token)  # get '[' symbol
            type, token = self.get_next()
            self.compileExpression()
            self._writer.write_push(symbol.get_kind(),symbol.get_number())
            self._writer.write_arithmetic("add")
            type, token = self.get_current()
            self.terminal(type, token) # get ']' symbol
            type, token = self.get_next()
            self.terminal(type, token)  # get '='
            self.get_next()
            self.compileExpression()
            self._writer.write_pop("temp",0)
            self._writer.write_pop("pointer",1)
            self._writer.write_push("temp",0)
            self._writer.write_pop("that",0)
        else:
            self.terminal(type, token)  # get '='
            self.get_next()
            self.compileExpression()
            self._writer.write_pop(symbol.get_kind(), symbol.get_number())
        type, token = self.get_current()
        self.terminal(type, token)  # get ';' symbol

    def compileWhile(self, type,token):
        """
        compiles a while statement
        """
        start_while = "WHILE_EXP"+str(self.label_counters["while"])
        end_while = "WHILE_END" + str(self.label_counters["while"])
        self.label_counters["while"] += 1
        self.terminal(type, token)  # get 'while' keyword
        type, token = self.get_next()
        self.terminal(type, token)  # get '(' symbol
        type, token = self.get_next()
        self._writer.write_label(start_while)
        self.compileExpression()
        self._writer.write_arithmetic("not")
        self._writer.write_if(end_while)
        type, token = self.get_current()
        self.terminal(type, token)  # get ')' symbol
        type, token = self.get_next()
        self.terminal(type, token)  # get '{' symbol
        type, token = self.get_next()
        self.compileStatements(type,token)
        self._writer.write_goto(start_while)
        self._writer.write_label(end_while)
        type, token = self.get_current()
        self.terminal(type, token)  # get '}' symbol

    def compileReturn(self, type,token):
        """
        compiles a return statement.
        """
        self.terminal(type, token)  # get 'return' keyword
        type, token = self.get_next()
        if self.isExpression(type, token):
            self.compileExpression()
            type, token = self.get_current()
        else:
            self._writer.write_push("constant",0)
        self._writer.write_return()
        self.terminal(type, token)  # get ';' symbol

    def compileIf(self,type,token):
        """
        compiles an if statement
        """
        self.terminal(type, token)  # get 'if' keyword
        type, token = self.get_next()
        self.terminal(type, token)  # get '(' symbol
        type, token = self.get_next()
        self.compileExpression()
        num = self.label_counters["if"]
        true_label = "IF_TRUE"+str(num)
        false_label = "IF_FALSE" + str(num)
        self.label_counters["if"] += 1
        self._writer.write_if(true_label)
        self._writer.write_goto(false_label)
        self._writer.write_label(true_label)
        type, token = self.get_current()
        self.terminal(type, token)  # get ')' symbol
        type, token = self.get_next()
        self.terminal(type, token)  # get '{' symbol
        type,token = self.get_next()
        self.compileStatements(type,token)
        type, token = self.get_current()
        self.terminal(type, token)  # get '}' symbol
        type, token = self.get_next()
        if token == "else":
            else_label = "IF_END"+ str(num)
            self._writer.write_goto(else_label)
            self._writer.write_label(false_label)
            self.terminal(type, token)  # get 'else' keyword
            type, token = self.get_next()
            self.terminal(type, token)  # get '{' symbol
            type, token = self.get_next()
            self.compileStatements(type,token)
            self._writer.write_label(else_label)
            type, token = self.get_current()
            self.terminal(type, token)   # get '}' symbol
            type, token = self.get_next()
        else:
            self._writer.write_label(false_label)

    def compileExpression(self):
        """
        compiles an expression.
        """
        self.compileTerm()
        type, token = self.get_current()
        while token in self.op:
            operation = token
            self.terminal(type, token) # get op symbol
            type, token = self.get_next()
            self.compileTerm()
            self._writer.write_arithmetic(self.op[operation])
            type, token = self.get_current()

    def isExpression(self,type,token):
        """
        checks if the beginning of an expression returns true or false
        """
        return type == "integerConstant" or type == "stringConstant" or type == "identifier" \
               or token in self.unaryOp or token in self.keywordConstant or token == '('

    def compileTerm(self):
        """
        compiles a term
        """
        type, token = self.get_current()
        if type =="integerConstant":
            self._writer.write_push("constant",token)
            type, token = self.get_next()
            return
        elif type =="stringConstant":
            self._writer.write_push("constant",len(token))
            self._writer.write_call("String.new", 1)
            for letter in token:
                self._writer.write_push("constant", ord(letter))
                self._writer.write_call("String.appendChar", 2)
            type, token = self.get_next()
            return
        elif token in self.keywordConstant:
            self.terminal(type, token)  # get constant
            self._writer.write_keywordConstants(token)
            type, token = self.get_next()
            return
        elif type == "identifier":
            self.terminal(type, token)  # get class/var name
            name = token
            symbol = self._subroutine_table.get_symbol(name)
            type, token = self.get_next()
            if token == "[":  # case of varName[expression]
                self.terminal(type, token)  # get '[' symbol
                self.get_next()
                self.compileExpression()
                self._writer.write_push(symbol.get_kind(),symbol.get_number())
                self._writer.write_arithmetic("add")
                self._writer.write_pop("pointer", 1)
                self._writer.write_push("that",0)
                type, token = self.get_current()
                self.terminal(type, token)  # get ']' symbol
                type, token = self.get_next()
                return
            elif token == "(":
                self._writer.write_push("pointer",0)
                name = self._cur_class+'.'+name
                counter = 1
                self.terminal(type, token)  # get '(' symbol
                counter += self.compileExpressionList()
                type, token = self.get_current()
                self.terminal(type, token)  # get ')' symbol
                self._writer.write_call(name, counter)
                type, token = self.get_next()
                return
            elif token == ".":  # case of subroutine call
                counter = 0
                self.terminal(type, token)  # get '.' symbol
                if symbol:
                    self._writer.write_push(symbol.get_kind(), symbol.get_number())
                    counter = 1
                    name = symbol.get_type()
                name += token
                type, token = self.get_next()
                name += token
                self.terminal(type, token)  # get subroutine name
                type, token = self.get_next()
                self.terminal(type, token)  # get '(' symbol
                counter += self.compileExpressionList()
                type, token = self.get_current()
                self.terminal(type, token)  # get ')' symbol
                self._writer.write_call(name, counter)
                self.get_next()
                return
            self._writer.write_push(symbol.get_kind(),symbol.get_number())
            return
        elif token in self.unaryOp:
            self.terminal(type, token)  # get unary operation symbol
            self.get_next()
            self.compileTerm()
            if token == "-":
                self._writer.write_arithmetic("neg")
            else:
                self._writer.write_arithmetic("not")
            return
        elif token == "(":
            self.terminal(type, token) # get '(' symbol
            type, token = self.get_next()
            self.compileExpression()
            type, token = self.get_current()
            self.terminal(type, token)  # get ')' symbol
            type, token = self.get_next()
            return
        return


    def compileSubroutineCall(self):
        """
        compiles the subroutineCall.
        """
        counter = 0
        type, token = self.get_next()
        self.terminal(type, token)  # get class/subroutine/var
        symbol = self._subroutine_table.get_symbol(token)
        name = token
        type, token = self.get_next()
        if token == ".":  # case of className.subroutineName
            self.terminal(type, token)  # get '.' symbol
            type, token = self.get_next()
            if symbol:
                counter = 1
                self._writer.write_push(symbol.get_kind(), symbol.get_number())
                name = symbol.get_type() + '.' + token
            else:
                name += "."+token
            self.terminal(type, token)  # get subroutine name
            type,token = self.get_next()
        else:
            self._writer.write_push("pointer",0)
            name = self._cur_class+"."+name
            counter = 1
        self.terminal(type, token)  # get '(' symbol
        counter += self.compileExpressionList()
        self._writer.write_call(name,counter)
        self._writer.write_pop("temp",0)
        type, token = self.get_current()
        self.terminal(type, token)  # get ')' symbol

    def compileExpressionList(self):
        """
        compiles the expressionList.
        """
        counter = 0
        type, token = self.get_next()
        if self.isExpression(type, token):
            counter += 1
            self.compileExpression()
        type, token = self.get_current()
        while token == ",":  # case of multiple expressions
            self.terminal(type, token) # get ',' symbol
            type, token = self.get_next()
            counter += 1
            self.compileExpression()
            type, token = self.get_current()
        return counter