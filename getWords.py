import numpy as np
import collections

# Words that are answers
word_answers = list(np.loadtxt("wordle-answers-alphabetical.txt",
                               comments="#", delimiter="\n", unpack=False, dtype=str))
# Words that are accepted, not including answers
word_allowed = list(np.loadtxt("wordle-allowed-guesses.txt",
                               comments="#", delimiter="\n", unpack=False, dtype=str))

num_answers = len(word_answers)
num_allowed = len(word_allowed)

# Separate into letters
# E.g. letter[0] is the list of all first letters of the words
letter_answers = list(zip(*[list(_) for _ in word_answers]))
letter_allowed = list(zip(*[list(_) for _ in word_allowed]))

# Flattened list of letters (all letters regardless of position)
all_letter_answers = [item for sublist in letter_answers for item in sublist]
all_letter_allowed = [item for sublist in letter_allowed for item in sublist]

all_letters_pos = [list(letter_answers[_]) +
                   list(letter_allowed[_]) for _ in range(5)]
all_letters = list(all_letter_answers) + list(all_letter_allowed)
all_words = word_answers + word_allowed


# Scoring system

# letter_score [dict]: A scoring system for letters based on their popularity
count_letters = collections.Counter(all_letters)
letter_score = dict(count_letters.most_common())


# letter_score_pos [list(dict, dict, dict, dict, dict)]: A scoring system for letters based on their popularity in each position
letter_score_pos = []
for j in range(5):
    count_letters = collections.Counter(all_letters_pos[j])
    letter_score_pos.append(dict(count_letters.most_common()))

    
