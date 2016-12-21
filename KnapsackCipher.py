from random import randint
from ReducedCharSet import ReducedCharSet

# KnapsackCipher.py
# Frank Mock
#
# This class implements the Knapsack Cipher Algorithm
# Using the methods of this class will allow a program
# to encrypt plaintext and decrypt the plaintext.
# There is a conditional in the constructor to allow the
# plaintext to be passed at the time a Knapsack object 
# is instantiated. If this is done, the ciphertext is
# generated and stored when the object is created.

class KnapsackCipher:
    def __init__(self, msg=None):
        if msg is None:
            self.rcs = ReducedCharSet()
            self.msg = ""
            self.__msgLength = 0
            self.__sik = [] # Part of Private Key
            self.__sikSize = 18 # a compromise
            self.__gk = []  # Public Key
            self.__m = 3
            self.__n = 0
            self.__multInv = 0 # Part of Private Key
            self.__sikSum = 0 # the sum of the elements in the SIK
            self.createSik(self.__sikSize)
            self.createGk()
            self.setMutiInverse(self.__m, self.__n)
            self.msg6BitBinaryStr = ""
            self.__encrypted = ""
            self.decrypted = ""
        else:
            self.rcs = ReducedCharSet()
            self.msg = msg
            self.__msgLength = len(msg)
            self.__sik = [] # Part of Private Key
            self.__sikSize = 18 # a compromise
            self.__gk = []  # Public Key
            self.__m = 3
            self.__n = 0
            self.__multInv = 0 # Part of Private Key
            self.__sikSum = 0 # the sum of the elements in the SIK
            self.createSik(self.__sikSize)
            self.createGk()
            self.setMutiInverse(self.__m, self.__n)
            self.msg6BitBinaryStr = ""
            self.msgToBinary()
            self.__encrypted = ""
            self.decrypted = ""
            self.encryptMessage()
            self.decryptMessage()
        
    
    # Sets the msg6BitBinaryStr instance variable.
    # msg6BitBinaryStr is a Reduced Character Set (RCS) 
    # 6-bit binary string of the message that is to be 
    # encrypted. The resulting string of ones and zeros 
    # is used with the GK during encryption.    
    def msgToBinary(self):
        s = ""
        for a in self.msg:
            s += self.rcs.ordRcsToBinary(a)
        self.msg6BitBinaryStr = s
                    
    # Sets the encrypted instance variable.
    # This method converts the msg6BitBinaryStr form of the message 
    # into cipher text.  
    def encryptMessage(self):
        b = self.msg6BitBinaryStr
        length = len(b)
        # pad b with "0"s if not a multiple of self.__sikSize
        x = length % self.__sikSize
        diff = self.__sikSize - x
        for j in range(diff):
            b += "0"
        c = 0
        lst = []
        count = 0
        # Sum the elements in GK that line up with 1 bits
        for i in range(len(b)): # i starts at 0
            m = i % self.__sikSize
            count += 1
            if b[i] == "1":
                c += self.__gk[m]
            # Every 18 comparisons add value of c to list
            if count % self.__sikSize == 0:
                lst.append(c)
                c = 0 # reset c
        # convert the list of integers to a string
        cipherLst = ""
        l = len(lst)
        for n in lst:
            cipherLst += str(n)
            l -= 1
            if l != 0:
                cipherLst += " "
        self.encrypted = cipherLst # set encrypted field



    #Takes plaintext and converts it to ciphertext using the
    #knapsack cipher
    #Returns the ciphertext as a String
    def encryptMsg(self, plaintext):
        self.msg = plaintext
        self.__msgLength = len(plaintext)
        self.msgToBinary() #sets the 6-bit binary string used for encryption
        b = self.msg6BitBinaryStr
        length = len(b)
        # pad b with "0"s if not a multiple of self.__sikSize
        x = length % self.__sikSize
        diff = self.__sikSize - x
        for j in range(diff):
            b += "0"
        c = 0
        lst = []
        count = 0
        # Sum the elements in GK that line up with 1 bits
        for i in range(len(b)): # i starts at 0
            m = i % self.__sikSize
            count += 1
            if b[i] == "1":
                c += self.__gk[m]
            # Every 18 comparisons add value of c to list
            if count % self.__sikSize == 0:
                lst.append(c)
                c = 0 # reset c
        # convert the list of integers to a string
        cipherLst = ""
        l = len(lst)
        for n in lst:
            cipherLst += str(n)
            l -= 1
            if l != 0:
                cipherLst += " "
        self.encrypted = cipherLst # set encrypted field
        return self.encrypted


    # Decrypts the cipher-text and sets the self.decrypted field
    def decryptMessage(self):
        decryptedMsg = ""
        # turn cipher text into a list
        l = self.encrypted.split(" ")
        dList = []
        # decrypt each block of cipher text using SIK
        for e in range(len(l)):
            # Calculate the number to use with SIK
            num = (int(l[e]) * self.__multInv) % self.__n
            last = len(self.__sik) - 1
            decrypted = ""
            remaining = num
            for i in range(len(self.__sik)):
                if self.__sik[last] <= remaining:
                    decrypted += "1"
                    remaining -= self.__sik[last]
                else:
                    decrypted += "0"
                last -= 1
            decrypted = decrypted[::-1] # reverse the binary string
            dList.append(decrypted)
            decrypted = ""
                        
        decryptIntList = []
            
        for s in dList:
            x = ""
            first = 0
            last = 6
            for i in range(3):
                # x holds a 6-bit RCS binary string
                x = s[first:last]
                first += 6
                last += 6
                
                # convert binary string into an int
                exp = len(x) - 1
                p = 0
                myInt = 0
                for j in x:
                    if j == "1":
                        p = 2**exp
                        myInt += p
                    exp -= 1
                decryptIntList.append(myInt)
                decryptedMsg += self.rcs.getRcsValue(myInt)
                
        # Up to 3 0s may appear at end of decrypted plain text due to 
        # padding that may have occurred during encryption
        # Remove added 0s        
        for i in range(3):
            if decryptedMsg.endswith("0"):
                decryptedMsg = decryptedMsg.replace(decryptedMsg, decryptedMsg[0:-1])

        self.decrypted = decryptedMsg
 

    #Decrypts the ciphertext passed as a parameter
    #Returns the plaintext as a string
    def decryptMsg(self, cipherText):
        decryptedMsg = ""
        # turn cipher text into a list
        l = cipherText.split(" ")
        dList = []
        # decrypt each block of cipher text using SIK
        for e in range(len(l)):
            # Calculate the number to use with SIK
            num = (int(l[e]) * self.__multInv) % self.__n
            last = len(self.__sik) - 1
            decrypted = ""
            remaining = num
            for i in range(len(self.__sik)):
                if self.__sik[last] <= remaining:
                    decrypted += "1"
                    remaining -= self.__sik[last]
                else:
                    decrypted += "0"
                last -= 1
            decrypted = decrypted[::-1] # reverse the binary string
            dList.append(decrypted)
            decrypted = ""
                        
        decryptIntList = []
            
        for s in dList:
            x = ""
            first = 0
            last = 6
            for i in range(3):
                # x holds a 6-bit RCS binary string
                x = s[first:last]
                first += 6
                last += 6
                
                # convert binary string into an int
                exp = len(x) - 1
                p = 0
                myInt = 0
                for j in x:
                    if j == "1":
                        p = 2**exp
                        myInt += p
                    exp -= 1
                decryptIntList.append(myInt)
                decryptedMsg += self.rcs.getRcsValue(myInt)
                
        # Up to 3 0s may appear at end of decrypted plain text due to 
        # padding that may have occurred during encryption
        # Remove added 0s        
        for i in range(3):
            if decryptedMsg.endswith("0"):
                decryptedMsg = decryptedMsg.replace(decryptedMsg, decryptedMsg[0:-1])

        return decryptedMsg
 
    
    # Creates a Super Increasing Knapsack    
    def createSik(self,size):
        p = 0
        total = 0
        s = randint(1,3) # starting SIK value
        for i in range(size):
            self.__sik.append(s)
            total = s + p
            p = total
            s = total + randint(1,3)
        self.__sikSum = total
        
    # Set the SIK to the list l given that l
    # is of the correct size
    def setSIK(self, l):
        if len(l) < 1:
            return
        else:
            self.__sik = l
    
    # Returns the SIK        
    def getSIK(self):
        return self.__sik
            
    # Set the SIK sum to the value s
    def setSIKSum(self, s):
        if s > 0:
            self.__sikSum = s
        else:
            return
    # Returns the SIK sum
    def getSIKSum(self):
        return self.__sikSum
                   
    # Creates a General Knapsack which is the Public Key        
    def createGk(self):
        n = self.__sikSum + 1
                
        if(self.getGcd(self.__m, n) != 1):
            while self.getGcd(self.__m, n) != 1:
                n += 1        
        self.__n = n
        
        for i in range(len(self.__sik)):
            self.__gk.append((self.__m * self.__sik[i]) % self.__n)
    
    # Returns the GK       
    def getGK(self):
        return self.__gk
    
    # Set the GK to the passed  GK list
    def setGK(self, gkList):
        self.__gk = gkList
        
    # The multiplicitive inverse of __m in the integers modulo __n.
    # Note: __m and __n must be relatively prime
    # Sets the self.__multInv field
    # self.__multInv is x such that  __m * x == 1 mod __n
    def setMutiInverse(self, m, n):
        i = 0
        if(self.getGcd(m, n) == 1):
            for x in range(1, n):
                r = (x * m) % n
                if r == 1:
                    i = x
                    break
        else:
            raise ValueError('%d has no inverse mod %d' % (m, n))
        self.__multInv = i
    
    # Sets the multiplicative inverse to the value m   
    def setMultiInverse(self, m):
        self.__multInv = m
        
    # Returns the value of self.multiInv
    def getMultiInverse(self):
        return self.__multInv
    
    # Set the value of __n to n
    def setN(self, n):
        if n > 0:
            self.__n = n
            
    # Returns the value of N
    def getN(self):
        return self.__n
                
    # This method helps determine if two methods are relatively prime
    # by finding their greatest common denominator.       
    def getGcd(self, n1, n2):
        gcd = 1
        k = 2
        while k <= n1 and k <= n2:
            if n1 % k == 0 and n2 % k == 0:
                gcd = k
            k += 1
        return gcd
    
    # Set the value of encrypted
    def setEncrypted(self, e):
        self.__encrypted = e
    
    # To_String method that displays all the values of this object
    def __str__(self):
        s = ""
        s += "Plain Text: " + self.msg + "\n"
        s += "SIK: " + str(self.__sik) + "\n"
        s += "SIK Sum: " + str(self.__sikSum) + "\n"
        s += "__m: " + str(self.__m) + "\n"
        s += "__n: " + str(self.__n) + "\n"
        s += "multiplicative inv. of __n and __m: " + str(self.__multInv) + "\n"
        s += "GK: " + str(self.__gk) + "\n"
        s += "Message in 6-bit RCS binary: " + self.msg6BitBinaryStr + "\n"
        s += "Encrypted message: " + self.__encrypted + "\n"
        s += "Decrypted message: " + self.decrypted
        return s
        