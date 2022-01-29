from getWords import *

# For each word, get the list of unique letters in it
word_letter_set = [list(set(list(_))) for _ in all_words]

"""
## Strategy 1
- Use all answers and allowed words
- Guess words based on banned letters and words only
- Uses word score based on letter frequency regardless of position
"""


def bestWord1(banned_letters: set = set(), banned_words: set = set(), correct_letters: set = set(), correct_letter_locations: list = ['', '', '', '', '']) -> str:
    # Make a copy of letter scoring without banned letters
    ls = dict(letter_score)
    for b in banned_letters:
        ls[b] = 0

    # Calculate the letter score for each word
    word_score = []
    for w in word_letter_set:
        score = sum([ls[_] for _ in w])
        word_score.append(score)

    # Get the word indices of the banned words
    banned_word_idx = [all_words.index(_) for _ in banned_words]
    # Set banned word scores to zero
    for j in banned_word_idx:
        word_score[j] = 0

    best_idx = np.argmax(word_score)

    best_word = all_words[best_idx]

    return best_word


"""
## Strategy 2
- Use all answers and allowed words
- Uses word score based on letter frequency
- Upweights the word scores when letters are known for corresponding words
"""


def bestWord2(banned_letters: set = set(), banned_words: set = set(), correct_letters: set = set(), correct_letter_locations: list = ['', '', '', '', '']) -> str:
    # Make a copy of letter scoring without banned letters
    ls = dict(letter_score)
    for b in banned_letters:
        ls[b] = 0

    mult_CL = 10
    for b in correct_letters:
        ls[b] *= mult_CL

    # Calculate the letter score for each word
    word_score = []
    for w in word_letter_set:
        score = sum([ls[_] for _ in w])
        word_score.append(score)

    # Get the word indices of the banned words
    banned_word_idx = [all_words.index(_) for _ in banned_words]
    # Set banned word scores to zero
    for j in banned_word_idx:
        word_score[j] = 0

    best_idx = np.argmax(word_score)

    best_word = all_words[best_idx]

    return best_word


"""
## Strategy 3
- Use all answers and allowed words
- Uses word score based on letter frequency
- Upweights the word scores when letters are known for corresponding words
- Upweights the word scores when letters positions are known for corresponding words
"""


def bestWord3(banned_letters: set = set(), banned_words: set = set(), correct_letters: set = set(), correct_letter_locations: list = ['', '', '', '', '']) -> str:
    # Make a copy of letter scoring
    ls = dict(letter_score)
    # lsp = dict(letter_score_pos)

    # Remove scores for banned letters
    for b in banned_letters:
        ls[b] = 0

    mult_CL = 10
    for b in correct_letters:
        ls[b] *= mult_CL

    word_mult = []
    for j in range(num_answers+num_allowed):
        wm = np.sum(
                np.array(list(all_words[j])) ==
                np.array(correct_letter_locations)
            )
        word_mult.append(1 + wm)

    # Calculate the sum of the letters scores for each word
    word_score = []
    for j in range(num_answers+num_allowed):
        w = word_letter_set[j]
        score = sum([ls[_] for _ in w])
        word_score.append(score * word_mult[j])

    # Get the word indices of the banned words
    banned_word_idx = [all_words.index(_) for _ in banned_words]
    # Set banned word scores to zero
    for j in banned_word_idx:
        word_score[j] = 0

    best_idx = np.argmax(word_score)

    best_word = all_words[best_idx]

    return best_word


if __name__ == "__main__":
    print("asd")
