import re

"""
Class for reading a file and tokenizes the commands
"""
class JackTokenizer():

    def __init__(self, filename):
        """
        Ctor
        _file: file to tokenize
        _data: a list of all the commands
        _types: a list of all the types in the file
        _tokens: a list of all the tokens in the file
        _xml: an xml file with all the token and types
        _tokens_iterator: an iterator of the tokens
        _token_types_iterator: an iterator of token types
        _current_token: the current token
        _current_token_type: the current token type
        _token_types: the token types
        _keywords: the keywords
        """
        self._file = open(filename, 'r')
        self._data = []
        self._types = []
        self._tokens = []
        self._xml = ['<tokens>']
        self._tokens_iterator = iter(self._tokens)
        self._token_types_iterator = iter(self._types)
        self._current_token = ""
        self._current_token_type = ""
        self._token_types = {'keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant'}
        self._keywords = {'class', 'method', 'function', 'constructor', 'int', 'boolean', 'char',
                         'void', 'var', 'static', 'field', 'let', 'do', 'if', 'else', 'while',
                         'return', 'true', 'false', 'null', 'this'}
        self._symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|',
                         '<', '>', '=', '~'}

    def has_more_tokens(self):
        """
        Returns true or false based on self._token_iterator next value and advances
        :return:
        """
        try:
            self._current_token = next(self._tokens_iterator)
            self._current_token_type = next(self._token_types_iterator)
            return True
        except:
            return False

    def get_token(self):
        """
        gets the current token and the current token type
        :return:
        """
        return self._current_token_type, self._current_token

    def is_keyword(self, token):
        """
        Check if given token is a keyword
        :param token:
        :return:
        """
        return token in self._keywords

    def is_symbol(self, token):
        """
        Check if given token is symbol
        :param token:
        :return:
        """
        return token in self._symbols

    def is_identifier(self, token):
        """
        Check if given token is an identifier
        :param token:
        :return:
        """
        return len(token) >= 1 and not token[0].isdigit() and re.match(r'^[A-Za-z0-9_]+', token) is not None and \
               not self.is_keyword(token)

    def is_int_val(self, token):
        """
        Check if token is an int value
        :param token:
        :return:
        """
        return token.isdigit() and 0 <= int(token) <= 32767

    def is_string_val(self, token):
        """
        Check if given token is a string value
        :param token:
        :return:
        """
        return len(token) >= 2 and \
               (token[0] == '\"' and token[-1] == '\"' and '\"' not in token[1:-1] and '\n' not in token[1:-1])

    def token_type(self, token):
        """
        Checking token type for private use
        :param token:
        :return:
        """
        if self.is_keyword(token):
            return 'keyword'
        elif self.is_symbol(token):
            return 'symbol'
        elif self.is_identifier(token):
            return 'identifier'
        elif self.is_int_val(token):
            return 'integerConstant'
        elif self.is_string_val(token):
            return 'stringConstant'
        else:
            return

    def filter_lines(self):
        """
        Read jack file while removing comments and blank lines
        :param filepath:
        :return:
        """
        # Remove unnecessary lines
        start_flag = False
        for line in self._file:
            seg1 = "" # segment that makes up line up to '/*'
            seg2 = "" # segment that makes up line after '*/'
            temp = line.strip() # remove whitespace/newline before/after line

            # Regex checks for comments inside string literals
            matcher1 = re.match('.*\"[^\"]*//[^\"]*\".*', temp)
            matcher2 = re.match('.*\"[^\"]*/\*{1,2}[^\"]*\".*', temp)
            matcher3 = re.match('.*\"[^\"]*\*/[^\"]*\".*', temp)
            if matcher1 is not None or matcher2 is not None or matcher3 is not None:
                self._data.append(temp[:])
                continue

            arr = temp.split('/*')
            if len(arr) > 1:
                start_flag = True
                seg1 = arr[0]
            if start_flag:
                arr = temp.split('*/')
                if len(arr) > 1:
                    seg2 = arr[1]
                    start_flag = False
                result = seg1[:]+seg2[:]
                if len(result):
                    self._data.append(seg1[:]+seg2[:])
            else:
                temp = ' '.join(temp.split('//')[0].split())
                if len(temp):
                    self._data.append(temp[:])

    def convert_lt_gt_quot_amp(self, char):
        """
        '<' -> &lt
        '>' -> &gt
        '"' -> &quot
        '&' -> &amp
        :param char:
        :return:
        """
        if char == '<':
            return '&lt;'
        elif char == '>':
            return '&gt;'
        elif char == '\"':
            return '&quot;'
        elif char == '&':
            return '&amp;'

    def split_line_by_symbols(self, line):
        """
        Split line by jack symbols
        :param line:
        :return:
        """
        result = list()

        idx = 0
        temp = ""
        while idx < len(line):
            # Split by whitespace (whitespace in string constants handled later)
            if line[idx] == ' ':
                result.append(temp)
                temp = ""
            # Split by symbols
            elif line[idx] in self._symbols and line[idx] != '\"':
                if len(temp):
                    result.append(temp)
                    result.append(line[idx])
                    temp = ""
                else:
                    result.append(line[idx])
            # Only catches left hand quotation mark, closing mark found inside
            elif line[idx] == '\"':
                next_idx = line.find('\"', idx + 1)
                while line[next_idx-1] == '\\':
                    next_idx = line.find('\"', next_idx)
                segment = line[idx:next_idx+1]
                result.append(segment)
                temp = ""
                idx = next_idx + 1 # skip after closing mark
                continue
            else:
                temp += line[idx]
            idx += 1

        return result

    def tokenize(self):
        """
        Read through filtered lines and construct tokens and xml file
        :return:
        """
        self.filter_lines()

        for line in self._data:
            # Seperate line into relevant tokens
            segments = self.split_line_by_symbols(line)
            for seg in segments:
                cur_type = self.token_type(seg)
                # Valid token type
                if cur_type is not None:
                    self._types.append(cur_type)
                    self._tokens.append(seg)
                    if cur_type not in {'stringConstant', 'integerConstant'}:
                        cur_type = cur_type.lower()
                    else:
                        if cur_type == 'stringConstant':
                            cur_type = 'stringConstant'
                            self._tokens[-1] = self._tokens[-1].strip('\"')
                            seg = seg.strip('\"')
                        else:
                            cur_type = 'integerConstant'
                    if seg in {'<', '>', '\"', '&'}:
                        self._tokens[-1] = self.convert_lt_gt_quot_amp(seg)
                        seg = self.convert_lt_gt_quot_amp(seg)
                    self._xml.append('<'+cur_type+'> '+seg+' </'+cur_type+'>')
                # Throw exception if cur_type is None seg is not whitespace
                elif len(seg.strip()):
                    print(seg)
                    raise InvalidTokenException
        self._xml.append('</tokens>')


class InvalidTokenException(Exception):
    """
    Exception to be raised when string does not match any valid token
    """
    pass
