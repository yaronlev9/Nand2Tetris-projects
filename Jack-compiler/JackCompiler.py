from CompilationEngine import *
from JackTokenizer import *
import sys
import os

def analyze(filename):
    """
    Given file/directory, analyze it
    :param filename:
    """
    tokenizer = JackTokenizer(filename)
    tokenizer.tokenize()
    engine = CompilationEngine(tokenizer)
    engine.write(filename.replace('.jack', '.vm'))

def main():
    """
    Main function for running analyzing program
    """
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for filename in os.listdir(arg):
                filename = os.path.join(arg, filename)
                if filename.endswith('.jack'):
                    analyze(filename)
        elif os.path.isfile(arg):
            analyze(arg)

if __name__ == '__main__':
    """
    Main function for running parsing program
    """
    main()
