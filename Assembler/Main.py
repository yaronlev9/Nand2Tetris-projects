from Parser import *
import sys
import os

def parse(filename):
    """
    Given file/directory, parse it
    :param filename:
    """
    parser = Parser()
    parser.read(filename)
    parser.asm_to_binary()
    parser.write(filename.replace('.asm', '.hack'))

def main():
    """
    Main function for running parsing program
    """
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for filename in os.listdir(arg):
                filename = os.path.join(arg, filename)
                if filename.endswith('.asm'):
                    parse(filename)
        elif os.path.isfile(arg):
            parse(arg)

if __name__ == '__main__':
    """
    Main function for running parsing program
    """
    main()
