"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")


    parser = Parser(input_file)

    symbol_table = SymbolTable()
    # first pass 

    
    while parser.has_more_commands():
        command_type = parser.command_type()
        if command_type == "L_COMMAND":
            label = parser.symbol()
            if not symbol_table.contains(label):
                symbol_table.add_entry(label, symbol_table.avalable_memory)
        elif command_type == "A_COMMAND":
            symbol_table.avalable_memory += 1
        elif command_type == "C_COMMAND":
            symbol_table.avalable_memory += 1
        parser.advance()

    # second pass
    parser.current_command_counter = 0
    #parser.advance()

    coder = Code()
    while parser.has_more_commands():
        parser.advance()

        command_out = ""
        command_type = parser.command_type()
        print(parser.current_command, parser.current_command_counter) # debug

        if command_type == "A_COMMAND":
            input_name = parser.current_command[1:]
            if not input_name.isnumeric():
                if not symbol_table.contains(input_name):
                    symbol_table.add_entry(input_name, symbol_table.avalable_memory)
                    num = str(bin(symbol_table.get_address(input_name))).replace("0b", "").zfill(15)
                    command_out = f"0{num}\n"
                else:
                    num = str(bin(symbol_table.get_address(input_name))).replace("0b", "").zfill(15)
                    command_out = f"0{num}\n"
            else:
                num = str(bin(int(input_name)).replace("0b", "").zfill(15))
                command_out = f"0{num}\n"
        
        elif command_type == "C_COMMAND":
            comp = coder.comp(parser.comp())
            dest = coder.dest(parser.dest())
            jump = coder.jump(parser.dest())
            print(parser.comp(),parser.dest(),parser.jump())
            command_out = f"111{comp}{dest}{jump}\n"
        
        print(command_out)
        output_file.write(command_out)
    return



if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
