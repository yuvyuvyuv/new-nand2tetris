"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        
        input_lines = input_file.readlines()
        command_lines = []
        # delete whitespace 
        for line in input_lines:
            line = line[:line.find("//")]
            line = line.replace("\\n","")
            line = line.replace(" ","")
            if line != "":
                command_lines.append(line)
        
        self.command_lines = command_lines
        self.current_command_counter = 0
        self.current_command = command_lines[0]

        

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_command_counter + 1< len(self.command_lines)
        pass

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.current_command_counter += 1
            self.current_command = self.command_lines[self.current_command_counter]
        pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.current_command[0] == '@':
            return "A_COMMAND"
        elif self.current_command[0] == '(' and self.current_command[-1] == ')':
            return "L_COMMAND"
        else:
            return "C_COMMAND"
        pass

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type == "A_COMMAND":
            return self.current_command[1:]
        elif self.command_type == "L_COMMAND":
            return self.current_command[1:-1]
        pass

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        current_command = self.current_command
        command_type = self.command_type()

        start_index = current_command.find("=")
        end_index = current_command.find(";")

        if start_index == -1: start_index = 0
        if end_index == -1: end_index = None

        if command_type == "C_COMMAND":
            return current_command[start_index:end_index]

        pass

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command_type = self.command_type()
        end_index = self.current_command.find('=')
        if end_index == -1: end_index = 0
        if command_type == "C_COMMAND":
            return self.current_command[:end_index]
        
                
        pass

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        current_command = self.current_command
        command_type = self.command_type()

        start_index = current_command.find(";")
        if command_type == "C_COMMAND" and start_index != -1:
            jmp = current_command[start_index:]
        elif command_type == "C_COMMAND":
            jmp = ""
        if jmp == "":
            return "null"
        else:
            return jmp       
        pass
