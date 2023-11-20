"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        out = "000"
        if 'M' in mnemonic:
            out[2] = '1'
        elif 'D' in mnemonic:
            out[1] = '1'
        elif 'A' in mnemonic:
            out[0] = '1'
        return out

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        if 'M' in mnemonic:
            a_bit = 1
            mnemonic = mnemonic.replace('M', 'A')
        else:
            a_bit = 0
        # TO-DO:
        # - check case "A+D" vs. "D+A"
        comp_dict = {
            "0"   : "101010",
            "1"   : "111111",
            "-1"  : "111010",
            "D"   : "001100",
            "A"   : "110000",
            "!D"  : "001101",
            "!A"  : "110001",
            "-D"  : "001111",
            "-A"  : "110011",
            "D+1" : "011111",
            "A+1" : "110111",
            "D-1" : "001110",
            "A-1" : "110010",
            "D+A" : "000010",
            "D-A" : "010011",
            "A-D" : "000111",
            "D&A" : "000000",
            "D|A" : "010101"
        }
        return str(a_bit) + comp_dict[mnemonic]
        
    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        out = "000"
        # 'G' = positive
        # 'E' = zero
        # 'L' = negative 

        if mnemonic == "JNE":
            mnemonic = "JGL"
        if mnemonic == "JMP":
            mnemonic = "GEL"
        
        if 'G' in mnemonic:
            out[0] = '1'
        elif 'E' in mnemonic:
            out[1] = '1'
        elif 'L' in mnemonic:
            out[2] = '1'
        return out
