# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import os

os.chdir("C:\Python Code\MIT - Intro to Python\PSets\PS3")

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    score = 0
    sum_points = 0
    word = str.lower(word)
    
    #Part 1 of the score computation
    for letter in word:
        sum_points += SCRABBLE_LETTER_VALUES[letter]
        
    #Part 2 of the score computation
    second_part = 7*len(word) - 3*(n - len(word))
    second_part = max(second_part, 1)
    
    #Calculate score
    score = sum_points*second_part
    
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    
    #wildcards are vowels so reduce vowel count by one
    num_vowels = int(math.ceil(n / 3)) - 1
    
    #number of wildcards "*"
    hand["*"] = 1
    
    #get as many vowels an num_vowels (already made to be one less vowel due to the wildcard earlier)
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #make word lower case
    word = str.lower(word)
    #initialise new hand, created a clone to avoid changing hand
    new_hand_working = hand.copy()
    
    #subtract 1 from the number in the hand if it appears in the word
    for letter in word:
        if letter in hand.keys():
            new_hand_working[letter] -= 1
    
    #if no more of that letter is in the hand, remove the letter
    new_hand = new_hand_working.copy()
    for key in new_hand_working:
        if new_hand_working[key] <= 0:
            new_hand.pop(key)
            
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    word = str.lower(word)
    check = True
    
    if '*' in word:
        # find the position of *
        asterisk_position = word.find('*')
        
        # create a list of possible words made by replacing * with a vowel
        possibility_check = []
        for vowel in VOWELS:
            possible_word = word[:asterisk_position] + vowel + word[asterisk_position + 1:]
            possibility_check.append(possible_word)
            if possible_word in word_list:
                break
    
        # initialise valid word counter
        valid_words = 0
        
        # increase valid_words by 1 every time there is a valid word
        for possible_word in possibility_check:
            if possible_word in word_list:
                valid_words += 1
        # if none of the possible words are valid, return False
        if valid_words == 0:
            check = False
            return check
    else:    
        if word not in word_list:
            check = False
            return check
   
    
    # loop through letters in word. if letter not in word, false
    # if letters in word exceeds letters in hand, false
    
    word_letter_count = {}
    for letter in word:
        word_letter_count[letter] = word_letter_count.get(letter,0) + 1
    
    for letter in word_letter_count:
        if letter not in hand.keys():
            check = False
            return check
        
        if word_letter_count[letter] > hand[letter]:
            check = False
            return check
    
    return check


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for number in hand.values():
        length += number
        
    return length
    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # Keep track of the total score
    total_score = 0
    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("Current hand:", end = ' ') 
        display_hand(hand) 
        # Ask user for input
        word = input("Please enter a word, or enter !! to indicate you are finished: ")
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list) == True:
                # Tell the user how many points the word earned,
                # and the updated total score
                n = calculate_handlen(hand)
                word_score = get_word_score(word, n)
                total_score += word_score
                print(word, "scored you", word_score, "points! Total score:", total_score, "points.")
                print()
                
            # Otherwise (the word is not valid):
            else: 
                # Reject invalid word (print a message)
                print("Sorry,", word, "is an invalid word. Please choose another word.")
                print()
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if word == "!!":
        print("The hand is over! You scored", total_score, "points!")
    else:
        print("You ran out of letters. You scored", total_score, "points!")
    
    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    # if the user provides a letter not in the hand, do nothing
    if letter not in hand.keys():
        return hand
    
    # if the user provides a letter in the hand...
    else:      
        # create a new vowels list based on what is not in the hand
        available_vowels = ""
        for vowel in VOWELS:
            if vowel not in hand.keys():
                available_vowels += vowel 
                
        # create a new consonants list based on what is not in the hand
        available_consonants = ""
        for consonant in CONSONANTS:
            if consonant not in hand.keys():
                available_consonants += consonant
                
        # create a combined vowels and consonants string of the above two new strings
        available_letters = available_vowels + available_consonants
        
        # create a working copy of hand
        new_hand = hand.copy()
        
        # count how many instances (x) of the chosen letter there are
        number_of_instances = new_hand[letter]
        
        # remove the letter from the working hand
        new_hand.pop(letter)
        
        # choose a new random letter from the combined list
        new_letter = random.choice(available_letters)
        
        # add x instances of that list to working dictionary
        new_hand[new_letter] = number_of_instances
        
    # now we can return the new dictionary
    return new_hand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    #keep track of the aggregate score
    aggregate_score = 0
    
    # ask user to nput how many hands they want to play
    hands_to_play = int(input("Enter total number of hands you want to play: "))
    print()
    
    #keep track of how many replays have been used
    replay_count = 0
    
    #keep going until all hands have been played
    while hands_to_play > 0:
        #deal a hand and show it to the user
        hand = deal_hand(HAND_SIZE)
        print("Current hand:", end = ' ')
        display_hand(hand)
        
        #check if the user wants to substitute a letter
        substitute = input("Would you like to substitute a letter (Yes or No)? ")
        print()
        
        #check if the response was yes or no. If yes ask the user which letter they want to substitute
        if str.lower(substitute) == "yes":
            letter = input("Which letter would you like to substitute? ")
            new_hand = substitute_hand(hand, letter)
            
            # now play the hand
            hand_score = play_hand(new_hand, word_list)
        
        #if no, play using the original hand that was dealt
        else:
            hand_score = play_hand(hand, word_list)
        
        print('-------------------------------------')
        
        #first see if the user can still replay the hand
        if replay_count < 1:
        #check if the user wants to replay that hand
            replay = input("Would you like to replay that hand (Yes or No)? ")
            print()
            
            # if yes, play the hand again (and it counts towards one of the hands), or go again with a fresh hand
            if str.lower(replay) == 'yes':
                #repeat the process from before
                hand_score = play_hand(hand, word_list)
                replay_count += 1
                print()
                print('You can no longer replay a hand.')
                print()
                print('-------------------------------------')
        #increase aggregate score by what was scored in that hand
        aggregate_score += hand_score
        
        #reduce the hands to play by 1
        hands_to_play -= 1    
            
    print('Your total score over all hands was:', aggregate_score)    
    #return the aggregate score to the user    
    return aggregate_score
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
