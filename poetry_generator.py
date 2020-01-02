import nltk
import pronouncing
import random
import time

my_corpus = nltk.corpus.webtext.words('overheard.txt')
bigrams = nltk.bigrams(my_corpus)
cfd = nltk.ConditionalFreqDist(bigrams)

# This function takes two inputs:
# source - a word represented as a string
# num - an integer
# The function will generate num random related words using
# the CFD based on the bigrams in our corpus, starting from
# source. So, the first word will be generated from the CFD
# using source as the key, the second word will be generated
# using the first word as the key, and so on.
# If the CFD list of a word is empty, then a random word is
# chosen from the entire corpus.
# The function returns a num-length list of words.
def random_word_generator(source = None, num = 1):
    result = []
    while source == None or not source[0].isalpha():
        source = random.choice(my_corpus)
    word = source
    result.append(word)
    while len(result) < num:
        if word in cfd:
            init_list = list(cfd[word].keys())
            choice_list = [x for x in init_list if x[0].isalpha()]
            if len(choice_list) > 0:
                newword = random.choice(choice_list)
                result.append(newword)
                word = newword
            else:
                word = None
                newword = None
        else:
            newword = None
            while newword == None or not newword[0].isalpha():
                newword = random.choice(my_corpus)
            result.append(newword)
            word = newword
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns the number of syllables in word as an
# integer.
# If the return value is 0, then word is not available in the CMU
# dictionary.
def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    count_list = [pronouncing.syllable_count(x) for x in phones]
    if len(count_list) > 0:
        result = max(count_list)
    else:
        result = 0
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of words that rhyme with
# the input word.
def get_rhymes(word):
    result = pronouncing.rhymes(word)
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of strings. Each string in the list
# is a sequence of numbers. Each number corresponds to a syllable
# in the word and describes the stress placed on that syllable
# when the word is pronounced.
# A '1' indicates primary stress on the syllable
# A '2' indicates secondary stress on the syllable
# A '0' indicates the syllable is unstressed.
# Each element of the list indicates a different way to pronounce
# the input word.
def get_stresses(word):
    result = pronouncing.stresses_for_word(word)
    return result

# This function generates each line of the poem
def generate_line():#IMPORTANT:according to examples, must include an instance that the word generated randomly is not in the Pronouncing library.
    starttime= time.time()
    lineup = []
    first = random_word_generator(None,2)[1]
    while(len(get_rhymes(first))<=6):#this should eliminate the issue where there are not enough rhyming words and we get into an infinite loop
        first = random_word_generator(None,2)[1]
    syllcount = count_syllables(first)
    previous = first
    lineup.append(first)
    #print(first)
    while(syllcount<6):
        #print("Current syllable count is " + str(syllcount))
        if(time.time()-starttime>2.5):#ensuring that we do not take too much time
            #print("We are here now.")
            return None
        possibilities=list(set(random_word_generator(previous)).intersection(set(get_rhymes(previous))))
        if(len(possibilities)==0):
            possibilities = get_rhymes(previous)
        if(len(possibilities)==0):
            possibilities = random_word_generator(previous)
        new_word = possibilities[random.randrange(len(possibilities))]
        #print(new_word)
        nsylls = count_syllables(new_word)
        if(nsylls==0):
            pass
        else:
            if(syllcount+nsylls>6):
                continue
            elif(syllcount+nsylls==6):
                syllcount+=nsylls
                #print("We got it!")
                lineup.append(new_word)
                break
            syllcount+=nsylls
            #print("Added syllables")
            previous = new_word
            lineup.append(new_word)

    return " ".join(lineup)


# This function constructs poem
def generate_poem():#POEM GENERATED WILL BE OF 4 lines. Each line will have 6 syllables. Each word in a line must rhyme with the previous word in that line. Consecutive lines need not rhyme 
    lineobjs = []
    for x in range(4):
        line = generate_line()
        while(line==None):
            line=generate_line()
        lineobjs.append(line)
    return '\n'.join(lineobjs)

def test():
    keep_going = True
    while keep_going:
        word = input("Please enter a word (Enter '0' to quit): ")
        if word == '0':
            keep_going = False
        elif word == "":
            pass
        else:
            print(cfd[word].keys(), cfd[word].values())
            print()
            print("Random 5 words following", word)
            print(random_word_generator(word, 5))
            print()
            print("Pronunciations of", word)
            print(pronouncing.phones_for_word(word))
            print()
            print("Syllables in", word)
            print(count_syllables(word))
            print()
            print("Rhymes for", word)
            print(get_rhymes(word))
            print()
            print("Stresses for", word)
            print(get_stresses(word))
            print()

if __name__ == "__main__":
    #test()
    my_poem = generate_poem()
    print(my_poem)
