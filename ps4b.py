# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import os
os.chdir('C:\Python Code\MIT - Intro to Python\PSets\ps4')

import string
from ps4a import *

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
wordlist = load_words(WORDLIST_FILENAME)

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = wordlist
        

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        validwords = self.valid_words[:]
        return validwords

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        shift_dict = {}
        
        lowercase_alphabet = string.ascii_lowercase
        UPPERCASE_ALPHABET = string.ascii_uppercase
        #loop through the lowercase alphabet. Add each letter as a key to our dictionary
        #the corresponding key will be the shifted value
        
        for letter in lowercase_alphabet:
            # to 25 as indexing runs from 0 to 25
            if lowercase_alphabet.index(letter) + shift > 25:
                # how far is the letter from the end
                distance_from_end = len(lowercase_alphabet) - 1 - lowercase_alphabet.index(letter)
                
                # subtracting 1 again as we start from 0 i.e. if we start from z and shift 1,
                # we would want to be on 0
                new_index = shift - distance_from_end - 1 
                
            else:
                new_index = lowercase_alphabet.index(letter) + shift
                
            shifted_letter = lowercase_alphabet[new_index]
            shift_dict[letter] = shifted_letter
        
        #repeat for uppercase
        for letter in UPPERCASE_ALPHABET:
            # to 25 as indexing runs from 0 to 25
            if UPPERCASE_ALPHABET.index(letter) + shift > 25:
                # how far is the letter from the end
                distance_from_end = len(UPPERCASE_ALPHABET) - 1 - UPPERCASE_ALPHABET.index(letter)
                
                # subtracting 1 again as we start from 0 i.e. if we start from z and shift 1,
                # we would want to be on 0
                new_index = shift - distance_from_end - 1 
                
            else:
                new_index = UPPERCASE_ALPHABET.index(letter) + shift
                
            shifted_letter = UPPERCASE_ALPHABET[new_index]
            shift_dict[letter] = shifted_letter
        
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
                
        #create an empty string to which we will append
        caesar_cipher = ""
        shift_dict = self.build_shift_dict(shift)
        #loop through characters in the message and 'code' the ones that are in th alphabet
        for character in self.get_message_text():
            if character in shift_dict.keys():
                caesar_cipher += shift_dict[character]
                
            else:
                caesar_cipher += character
                
        return caesar_cipher

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''

        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        copy_encryption_dict = self.encryption_dict.copy()
        
        return copy_encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        #convert the encrypted story into just lower case words
        story_words = self.get_message_text().split()
        
        #create an empty dictionary to store how many valid words there are per shift number
        shiftvalidwords = {}
        
        #loop through the possible shift numbers
        for shift_number in range(0,26):
            
            #initialise a value of zero for the number of words that are in our word list
            number_of_words = 0
            
            #loop through all the words in the encrypted text to check if they're valid words after applying the shift
            for possible_word in story_words:
                #decrypt the word with the shift. First need to make it a Message object so the apply_shift function can be used on it
                word = Message(possible_word)
                decrypt_word = word.apply_shift(26 - shift_number)
                
                #check if it's valid; if so add one to our number_of_words count
                if is_word(self.valid_words, decrypt_word):
                    number_of_words += 1    
            
            #add the number of valid words for that shift number to our dictionary
            shiftvalidwords[shift_number] = shiftvalidwords.get(shift_number,0) + number_of_words
        
        #find the key in our dictionary with the maximum value
        best_shift = max(shiftvalidwords, key = shiftvalidwords.get)
        #decrypt the message using the best_shift
        message = Message(self.get_message_text())
        decrpyted_message = message.apply_shift(26 - best_shift)
        
        return (26 - best_shift, decrpyted_message)
        
        

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    test1 = PlaintextMessage('hello World!£!£', 0)
    print('Expected Output: hello World!£!£')
    print('Actual Output:', test1.get_message_text_encrypted())
    
    test2 = CiphertextMessage('hello World!£!£')
    print('Expected Output:', (26, 'hello World!£!£'))
    print('Actual Output:', test2.decrypt_message())
    
    test3 = PlaintextMessage('hello World!£!£', 2)
    print('Expected Output: jgnnq Yqtnf!£!£')
    print('Actual Output:', test3.get_message_text_encrypted())
    
    test4 = CiphertextMessage('jgnnq Yqtnf!£!£')
    print('Expected Output:', (24, 'hello World!£!£'))
    print('Actual Output:', test4.decrypt_message())
    
    test5 = PlaintextMessage('hello World', 1)
    print('Expected Output: ifmmp Xpsme')
    print('Actual Output:', test5.get_message_text_encrypted())
    
    test6 = CiphertextMessage('ifmmp Xpsme')
    print('Expected Output:', (25, 'hello World'))
    print('Actual Output:', test6.decrypt_message())
    
    #TODO: best shift value and unencrypted story 
    
    encrypted_story = CiphertextMessage(get_story_string())
    print(encrypted_story.decrypt_message())
