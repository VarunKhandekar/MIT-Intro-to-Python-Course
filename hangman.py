# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import os
import random
import string
os.chdir('C:\Python Code\MIT - Intro to Python\PSets\ps2')
WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for letter in secret_word:
        if letter in letters_guessed:
            check = True
        else:
            check = False
            break

    return check



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    word = ""
    for letter in secret_word:
        if letter in letters_guessed:
            word = word + letter +" "
        else:
            word = word + "_ "
            
    return word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    import string
    
    letters_left = ""
    alphabet = string.ascii_lowercase
    
    for letter in alphabet:
        if letter not in letters_guessed:
            letters_left = letters_left + letter
    
    return letters_left
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    #initialise values and create an inroduction for the user
    print("")
    print("Welcome to the game of hangman. I am thinking of a word that is", len(secret_word), "letters long.")
    print("-----------------------------------")
    guesses = 6
    
    print("You have 3 warnings each round. For every invalid guess, you will lose a warning.")
    print("If you lose 3 warnings in a round, you will lose a guess.")
    letters_guessed = []
    
    round_counter = 1
    
    while guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        warnings = 3
        print("----------------------------")
        print("ROUND", round_counter)
        print("You have", guesses, "guesses left.")
        print("Available letters:", available_letters)
        print("Please guess only one letter at a time.")
        
        #User input stage; ensure the user inputs a single letter, otherwise penalise them
        your_guess = input("Enter your guess: ")
        while str.lower(your_guess) not in available_letters or len(your_guess) != 1:
            warnings = warnings - 1
            
            #exit the loop if the user is out of warnings
            if warnings == 0:
                print("You are out of warnings. You lose a guess.")
                break
            #inform the user of how many warnings they have left
            else:
               print("This is not a valid choice. You have", warnings, "warnings left this round.")
            
            #give the user a different comment dependent on what mistake they made
            if len(your_guess) != 1:
                your_guess = input("Please choose one letter from the available letters: ")
            elif str.isalpha(your_guess) == False:   
                your_guess = input("This is not a letter. Please choose a letter from the available letters: ")
            elif str.lower(your_guess) not in available_letters:
                your_guess = input("You have picked this letter before. Please choose a letter from the available letters: ")
                
                
        #if the user failed to corrctly input a value, dock a guess from them, and restart the loop
        if warnings == 0:
            guesses = guesses - 1
            round_counter += 1
            continue
        
        #at this stage, letter is assumed to be valid. Add the letter to our guessed letters list
        letters_guessed.append(str.lower(your_guess))
        
        #check if letter is in secret word
        if str.lower(your_guess) in secret_word:
            print("Good guess!")  
            print("")
        #dock a guess if it's a fair guess but not in the word
        else:
            print("Unluckyyyyy")
            print("")
            guesses = guesses - 1
        # print("This is what you have so far:", get_guessed_word(secret_word, letters_guessed))
        # if str.lower(your_guess) in available_letters and len(your_guess) == 1: 
        #     letters_guessed.append(str.lower(your_guess))
        #     guesses = guesses - 1
        
        # if str.lower(your_guess) in secret_word and len(your_guess) == 1:
        #     print("Good guess!")  
        # else:
        #     print("Unluckyyyyy")
        print("This is what you have so far:", get_guessed_word(secret_word, letters_guessed))
        print("")
        
        #exit the loop if we have the word guessed
        if is_word_guessed(secret_word, letters_guessed) == True:
            break
        else:
            round_counter += 1
    
    #final thing the user sees    
    if is_word_guessed(secret_word, letters_guessed) == True:
        print("-----------------------")
        print("Congratulations, you win!")
        print("")
    else:
        print("-----------------------")
        print("You lose, better luck next time!")
        print("")
        print("The word was:", secret_word)
        
    total_score = guesses*len(set(secret_word))
    print("-----------------------")
    print("Your total score was:", total_score)
    return 
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    check = True
    my_word = my_word.replace(" ","")
    
    #if words are a different length, immediately exit
    if len(my_word) != len(other_word):
        check = False
               
    else:
        #initialise counter to index through other_word
        i = 0
        for letter in my_word:
            #see what happens if we encounter a "_" in my_word
            if letter == "_":
                #if we have a "_" and it represents a letter that's already been guessed, exit!
                if other_word[i] in my_word:
                    check = False
                    break
                #if we get to here, the "_" is valid; move to the next letter in my_word and other_word
                else:
                    i += 1
                    continue
            
            #see what happens if we encounter a letter in my_word
            #if it doesn't match th equivalently positioned letter in other_word, exit!
            elif letter != other_word[i]:
                check = False
                break
            #at this stage, the letter matches. Now ensure we move onto the next letter in other_word
            i += 1
    
    return check

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matching_words = []
    
    #print all matching words
    for word in wordlist:
        if match_with_gaps(my_word, word) == True:
            print(word)
            matching_words.append(word)
    
    #if there are no matches, matching_words will be empty
    if len(matching_words) == 0:
        print("No matches found")
    
    return

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
        #initialise values and create an inroduction for the user
    print("")
    print("Welcome to the game of hangman. I am thinking of a word that is", len(secret_word), "letters long.")
    print("-----------------------------------")
    guesses = 6
    
    print("You have 3 warnings each round. For every invalid guess, you will lose a warning.")
    print("If you lose 3 warnings in a round, you will lose a guess.")
    letters_guessed = []
    
    round_counter = 1
    
    while guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        warnings = 3
        print("----------------------------")
        print("ROUND", round_counter)
        print("You have", guesses, "guesses left.")
        print("Available letters:", available_letters)
        print("Please guess only one letter at a time.")
        print("Guess * for a hint.")
        
        #User input stage; ensure the user inputs a single letter, otherwise penalise them
        your_guess = input("Enter your guess: ")
        
        
    
        
        while str.lower(your_guess) not in available_letters or len(your_guess) != 1:
            
            #if the guess is a *, offer the hints, then continue with the code
            if your_guess == "*":
                my_word = get_guessed_word(secret_word, letters_guessed)
                print("Possible word matches are:")
                show_possible_matches(my_word)
                print("This is what you have so far:", get_guessed_word(secret_word, letters_guessed))
                break
            
            warnings = warnings - 1
            
            #exit the loop if the user is out of warnings
            if warnings == 0:
                print("You are out of warnings. You lose a guess.")
                break
            #inform the user of how many warnings they have left
            else:
               print("This is not a valid choice. You have", warnings, "warnings left this round.")
            
            #give the user a different comment dependent on what mistake they made
            if len(your_guess) != 1:
                your_guess = input("Please choose one letter from the available letters: ")
            elif str.isalpha(your_guess) == False:   
                your_guess = input("This is not a letter. Please choose a letter from the available letters: ")
            elif str.lower(your_guess) not in available_letters:
                your_guess = input("You have picked this letter before. Please choose a letter from the available letters: ")
                
                
        #if the user failed to corrctly input a value, dock a guess from them, and restart the loop
        if warnings == 0:
            guesses = guesses - 1
            round_counter += 1
            continue
        
        #at this stage, letter is assumed to be valid or a *. 
        
        #print stuff if the guess was a letter; continue on if it was a *
        if str.lower(your_guess) in available_letters:
            #Add the letter to our guessed letters list
            letters_guessed.append(str.lower(your_guess))
            
            #check if letter is in secret word
            if str.lower(your_guess) in secret_word:
                print("Good guess!")  
                print("")
            #dock a guess if it's a fair guess but not in the word
            else:
                print("Unluckyyyyy")
                print("")
                guesses = guesses - 1
 
            print("This is what you have so far:", get_guessed_word(secret_word, letters_guessed))
            print("")
        
        #exit the loop if we have the word guessed
        if is_word_guessed(secret_word, letters_guessed) == True:
            break
        else:
            round_counter += 1
    
    #final thing the user sees    
    if is_word_guessed(secret_word, letters_guessed) == True:
        print("-----------------------")
        print("Congratulations, you win!")
        print("")
    else:
        print("-----------------------")
        print("You lose, better luck next time!")
        print("")
        print("The word was:", secret_word)
        
    total_score = guesses*len(set(secret_word))
    print("-----------------------")
    print("Your total score was:", total_score)
    return 



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
