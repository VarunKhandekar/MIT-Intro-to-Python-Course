# Problem Set 4A
# Name: Varun Khandekar
# Collaborators: N/A
# Time Spent: N/A

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
    #Base case - the simplest possible string
    if len(sequence) == 1:
        return list(sequence)
    
    else:
        #remove the first letter of the string
        sequence_LessInitial = sequence[1:]
        removed_character = sequence[0]
        
        #rerun our function to get all possible permutations of our sequence without its first character
        possible_permutations_LessInitial = get_permutations(sequence_LessInitial)

        #create an empty dictionary to store possible permutations (dictionary so as to avoid duplicates)
        possible_permutations_dict = {}

        #loop through what we got from rerunning our function from 2 code lines above
        for perm in possible_permutations_LessInitial:
            
            #loop through each possible index in each 'perm' in possible_permutations_LessInitial
            #this is so we can find all the points to add in the first letter we removed earlier
            # +1 in the length so we include the position at the end of the string too
            for position in range(len(perm)+1):
                #add the removed letter in each of those positions
                permutation = perm[:position] + removed_character + perm[position:]
                
                #add the resulting string as a key to our dictionary
                possible_permutations_dict[permutation] = possible_permutations_dict.get(permutation, 0) + 1
                
        #get the keys of our dictionary as a list
        possible_permutations = list(possible_permutations_dict.keys())
        
        return possible_permutations





if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    print('Input:', 'abc')
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations('abc'))
    
    print('Input:', 'cat')
    print('Expected Output:', ['cat', 'act', 'atc', 'cta', 'tca', 'tac'])
    print('Actual Output:', get_permutations('cat'))
    
    print('Input:', 'ab')
    print('Expected Output:', ['ab', 'ba'])
    print('Actual Output:', get_permutations('ab'))
