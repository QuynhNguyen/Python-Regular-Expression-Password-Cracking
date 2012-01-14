#PA 5

import re

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions

def closest_to(l,v):
    """Return the element of the list l closest in value to v.  In the case of
       a tie, the first such element is returned.  If l is empty, None is returned."""
    if(l == []): 
        return None #if its empty list then return NONE
    else: 
        value = l[0] #Assume the first value is closest 
        closest = v - l[0] #Closest value range
        for element in l: #looping begin
            diff = v - element #get the different
            if(diff < 0): #We only want positive number
                diff = diff * -1 
            if(diff < closest): #if the new different is smallest then let switch
                closest = diff
                value = element #New value found
        return value
        

def make_dict(keys,values):
    """Return a dictionary pairing corresponding keys to values."""
    dictionary = {} #initialize dictionary library
    for key,value in zip(keys,values): #loop through the 2 lists
        dictionary[key] = value
    return dictionary
   
# file IO functions
def word_count(fn):
    """Open the file fn and return a dictionary mapping words to the number
       of times they occur in the file.  A word is defined as a sequence of
       alphanumeric characters and _.  All spaces and punctuation are ignored.
       Words are returned in lower case"""
    inputFile = open(fn, "r") #open the file with read permission
    textString = inputFile.read() #store everything into the string
    inputFile.close() #close the file once done
    occurences = {} #intialize the occurences dict
    p = re.compile(r'\W+') #set up regular expressionf or splitting
    textString = p.split(textString)
    
    for word in textString: #the usual for loop
        word = str.lower(word) #convert everything to lowercase
        if occurences.has_key(word): #if already exist then just add 1
            occurences[word] = occurences[word] + 1
        else:
            occurences[word] = 1 #else make it equal to 1
            
    occurences.pop('') #pop out the weird nothingness
    
    return occurences
    









