
from misc import *
import crypt
import time

def load_words(filename,regexp):
    """Load the words from the file filename that match the regular
       expression regexp.  Returns a list of matching words in the order
       they are in the file."""
       
    myList = [] #initiate empty list to store words
    
    #Read file begin here
    fileInput = open(filename, "r")
    file = fileInput.read()
    fileInput.close()
    
    file = file.split(None) #split the NONE
    pattern = re.compile(regexp) #take in user input RegExp
    
    #then we read what inside the file
    for f in file:    
        if (pattern.match(f)): #if we found it
            myList.append(f)   #Add it to the list
    return myList
  


def transform_reverse(str):
    reverse_list = [] #Empty List
    reverse_string = "" #Empty string to store reverse string

    x = len(str)-1 #total string length - 1

    #making a new string by concatenating string[n-1] + string[n-2] + ...+ String[0]
    while (x >= 0):
        reverse_string = reverse_string + str[x]
        x = x -1

    #Add it to the list  
    reverse_list.append(str)
    reverse_list.append(reverse_string)
    
    return reverse_list



def transform_capitalize(str):
    
    x = [] 

    #Use recursive with the help of helper function
    #Here is how it work:
    #let say our input string is abcd
    #we will get Abcd then recurse on Abcd which is ABcd then recursive on that
    #if we keep doing that then at the end we will have all the combination
     
    def helperFun(n,list,str):
            list.append(str) #add it to the list
            for i in range(n,len(str)):
                temp = str[0:i] + str[i].upper() + str[i+1:]
                helperFun(i+1, list, temp) #recurse begin on the next char of the string
            return list

    return helperFun(0,x,str) #call the recursive function 
        
    
    

def transform_digits(str):
    #add the map dictionary
    l33tDict = {'o':['0'], 'z':['2'], 'a':['4'], 'b':['6','8'], 'i':['1'], 'l':['1'], 'e':['3'], 's':['5'], 't':['7'], 'g':['9'], 'q':['9']}
    myList = [] #initiate an empty list

    #This function is almost exactly the same as the transform_capitalize
    #Main different is that you have to check if there is something inside
    #the dictionary list before transforimg it. If there is none, then
    #dont mess around with it.
    def helperFun(n,list,str):
            list.append(str)
            for i in range(n,len(str)):
                if(l33tDict.has_key(str[i].lower())):
                    numList = l33tDict[str[i].lower()]
                    for j in range(0, len(numList)):
                        temp = str[0:i] + numList[j] + str[i+1:]
                        helperFun(i+1, list, temp)
            return list
    return helperFun(0,myList,str)
                 
        

def check_pass(plain,enc):
    """Check to see if the plaintext plain encrypts to the encrypted
       text enc"""
       
    salt = enc[0]+enc[1] #get the first 2 letters for salt
    encrypted = crypt.crypt(plain,salt) #start the encryption
    if(encrypted == enc): #if match then return true else false
        return True
    else:
        return False

def load_passwd(filename):
    """Load the password file filename and returns a list of
       dictionaries with fields "account", "password", "UID", "GID",
       "GECOS", "directory", and "shell", each mapping to the
       corresponding field of the file."""
    dictList = [] #Init empty dict 
    inputFile = open(filename,'r') #read in file
    file = inputFile.readlines()
    inputFile.close()

    pattern = re.compile(r':*') #we want to split the :
    
    #loop through the lines in files and add it to the dictionary
    #Finally, we add it to the list because we want to return a
    #list that contain a bunch of dictionary file
    for f in file:
        myDict = {}
        listArray = pattern.split(f)
        myDict['account'] = listArray[0]
        myDict['shell'] = listArray[6]
        myDict['UID'] = listArray[2]
        myDict['GID'] = listArray[3]
        myDict['GECOS'] = listArray[4]
        myDict['directory'] = listArray[5]
        myDict['password'] = listArray[1]
        dictList.append(myDict)

    return dictList

def crack_pass_file(fn_pass,words,out):
    """Crack as many passwords in file fn_pass as possible using words
       in the file words"""

    #Pretty self-explanatory because we only use function we defined so far

    writeFile = open(out, "w") #prepare for writing
    wordList = load_words(words,r"\w{6,8}$") #open wordlist
    encryptedPass = load_passwd(fn_pass) #open pass list

    #Regular Check
    for plain in wordList:
        for enc in encryptedPass:
            if(check_pass(plain,enc['password'])):
                writeFile.write(enc['account'] + "=" + plain + '\n')
                writeFile.flush()
                encryptedPass.remove(enc)

    #Transform Reverse Check
    for plain in wordList:
        list_reverse = transform_reverse(plain)
        for enc in encryptedPass:
            if(check_pass(list_reverse[1],enc['password'])):
                writeFile.write(enc['account'] + "=" + list_reverse[1] + '\n')
                writeFile.flush()
                encryptedPass.remove(enc)


    #Transform digits Check
    for plain in wordList:
        list_digits = transform_digits(plain)
        list_digits.pop(0) #already checked the first element
        for x in list_digits:
            for enc in encryptedPass:
                if(check_pass(x,enc['password'])):
                    writeFile.write(enc['account'] + "=" + x + '\n')
                    writeFile.flush()
                    encryptedPass.remove(enc)
                    
    #Transform Capitalize Check
    for plain in wordList:
        list_capitalize = transform_capitalize(plain)
        list_capitalize.pop(0) #already checked the first element
        for x in list_capitalize:
            for enc in encryptedPass:
                if(check_pass(x,enc['password'])):
                    writeFile.write(enc['account'] + "=" + x + '\n')
                    writeFile.flush()
                    encryptedPass.remove(enc)


    #Transform Reverse Capitalization and Reverse Digits
    for plain in wordList:
        list_reverse = transform_reverse(plain)
        list_cap_rev = transform_capitalize(list_reverse[1]) #reverse + capitalize
        list_dig_rev = transform_digits(list_reverse[1]) #reverse + digit
        list_cap_rev.pop(0)
        for x in list_cap_rev:
            for enc in encryptedPass:
                if(check_pass(x,enc['password'])):
                    writeFile.write(enc['account'] + "=" + x + '\n')
                    writeFile.flush()
                    encryptedPass.remove(enc)
        for x in list_dig_rev:
            for enc in encryptedPass:
                if(check_pass(x,enc['password'])):
                    writeFile.write(enc['account'] + "=" + x + '\n')
                    writeFile.flush()
                    encryptedPass.remove(enc)

     #Transform Capitalize Digits
    for plain in wordList:
        list_capitalize = transform_capitalize(plain)
        for x in list_capitalize:
            list_digits = transform_digits(x)
            for y in list_digits:
                for enc in encryptedPass:
                    if(check_pass(y,enc['password'])):
                        writeFile.write(enc['account'] + "=" + y + '\n')
                        writeFile.flush()
                        encryptedPass.remove(enc)
    

    writeFile.close()
    
start = time.time()
crack_pass_file("passwd.txt","words.txt","account.txt")
elapsed = (time.time() - start)
print elapsed
