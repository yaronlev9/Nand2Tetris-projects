from Parser import *
import sys
import os

def parse(filename, target_file):
    """
    Given file/directory, parse it
    :param filename:
    :param target_file:
    """
    parser = Parser()
    parser.read(filename)
    parser.vm_to_asm()
    parser.write(target_file)

def main():
    """
    Main function for running parsing program
    """
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            new_name = arg + '/' + arg.split('/')[-1] + ".asm"
            parser = Parser()
            for filename in os.listdir(arg):
                filename = os.path.join(arg, filename)
                if filename.endswith('.vm'):
                    parser.read(filename)
                    parser._data.append("end_file\n")
            parser.vm_to_asm()
            parser.write(new_name)
        elif os.path.isfile(arg):
            parse(arg, arg.replace('.vm', '.asm'))

if __name__ == '__main__':
    """
    Main function for running parsing program
    """
    main()
