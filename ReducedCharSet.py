# ReducedCharSet.py
# Frank Mock
#
# The Reduced Character Set only uses 64 characters.
# This is so that each character in this dictionary
# can be represented by only 6 bits. Upper case
# letters are converted to lower case.

class ReducedCharSet:
    def __init__(self):

        self.smallCharCode = {"0":0, "1":1, "2":2, "3":3,
                              "4":4, "5":5, "6":6, "7":7,
                              "8":8, "9":9, "a":10, "b":11,
                              "c":12, "d":13, "e":14, "f":15,
                              "g":16, "h":17, "i":18, "j":19,
                              "k":20, "l":21, "m":22, "n":23,
                              "o":24, "p":25, "q":26, "r":27,
                              "s":28, "t":29, "u":30, "v":31,
                              "w":32, "x":33, "y":34, "z":35,
                              " ":36, ",":37, ".":38, ";":39,
                              "!":40, "@":41, "#":42, "$":43,
                              "%":44, "^":45, "&":46, "*":47,
                              "(":48, ")":49, "-":50, ":":51,
                              "'":52, "!":53, "?":54, "$":55,
                              "+":56, "=":57, "<":58, ">":59,
                              "/": 60, "\\":61, "\"":62, "\n":63}
    
    # This method expects a single character (one digit string)
    # and will return the integer that it maps to in the RCS
    # dictionary. The lower case value of capital letters are 
    # returned. The value of ? is returned if the character is 
    # not in the dictionary    
    def ordRcs(self, s):
        x = s[0] # only accept a single character
        c = ord(x) # To check for capital letters
        
        if x in self.smallCharCode:
            return self.smallCharCode[x]
        elif c >= 65 and c < 90:
            lc = x.lower()
            return self.smallCharCode[lc] # s[0] is capital letter
        else:
            return self.smallCharCode["?"] #return value for ?
    
    # Returns the key for the parameter num    
    def getRcsValue(self, num):
        for key in self.smallCharCode:
            if self.smallCharCode[key] == num:
                return key
                
    # Returns 6 bit binary number of RCS code of c
    def ordRcsToBinary(self, c):
        a = self.ordRcs(c[0])
        return format(a, '06b')        
        