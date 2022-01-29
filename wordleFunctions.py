import multiprocessing as mp
from debugpy import trace_this_thread
import numpy as np
from typing import Callable

from getWords import *


def wordle(target_word_idx: int, guess: str) -> dict:
    # For a chosen target word (identified by index), make a guess
    # This function will output in a dictionary:
    #   - "correct_guess" [boolean]: Whether the guess was correct or not,
    #   - "correct_letters" [set]: The letters in the guess that were correct
    #   - "incorrect_letters" [set]: The letters in the guess that were incorrect
    #   - "correct_letter_locations" [list]: The letters in the guess that were correct and in the right place,
    #       e.g. ['m', '', 'd', '', ''] for guessing "medal" for the target word "modem"

    if not (len(guess) == 5):
        raise AssertionError("Guess needs to have 5 letters")
    if not (guess in (word_answers + word_allowed)):
        raise AssertionError("Guess is not in the word list")

    target_word = word_answers[target_word_idx]
    target_letters = list(target_word)

    guess_letters = list(guess)

    correct_locations = [target_letters[j] ==
                         guess_letters[j] for j in range(5)]
    correct_letter_locations = [(guess_letters[j] if (
        target_letters[j] == guess_letters[j]) else "") for j in range(5)]

    correct_letters = set(target_letters).intersection(set(guess_letters))

    incorrect_letters = set(guess_letters) - correct_letters

    result = {"correct_guess": np.prod(correct_locations) == 1,
              "correct_letters": correct_letters,
              "incorrect_letters": incorrect_letters,
              "correct_letter_locations": correct_letter_locations}

    return result


g_max_guesses = 100


def playWordle(bestWord: Callable, target_word_idx: int):
    # Play the wordle game using a function that returns the best word to use
    banned_letters = set()
    banned_words = set()
    correct_letters = set()
    correct_letter_locations = ['', '', '', '', '']
    num_guesses = 0
    guesses = []
    while True:
        best_word = bestWord(banned_letters, banned_words,
                             correct_letters, correct_letter_locations)
        guesses.append(best_word)
        num_guesses = num_guesses + 1

        result = wordle(target_word_idx, best_word)

        if result["correct_guess"]:
            break
        elif num_guesses > g_max_guesses:
            break

        banned_letters = banned_letters.union(result["incorrect_letters"])
        banned_words = banned_words.union([best_word])
        correct_letters = correct_letters.union(result["correct_letters"])

        new_cll = np.where(
            (np.array(correct_letter_locations) == '') & (
            np.array(result["correct_letter_locations"]) != ''))[0]
        if len(new_cll) > 0:
            for j in new_cll:
                correct_letter_locations[j] = result["correct_letter_locations"][j]


    game_result = {"num_guesses": num_guesses, "guesses": guesses, "banned_letters": banned_letters,
                   "banned_words": banned_words, "correct_letters": correct_letters}
    return game_result


def algScoreSerial(bestWord, num_words=20):
    # Play wordle with the chosen bestWord word choice algorithm
    # Return the total score for all games (lower is better)

    score = 0
    num_forfeited = 0
    np.random.seed(0)
    target_word_idxs = np.random.choice(
        range(num_answers), size=min(num_words, num_answers), replace=False)
    target_word_idxs = range(num_answers)

    for target_word_idx in target_word_idxs:
        result = playWordle(bestWord, target_word_idx)

        if result["num_guesses"] > g_max_guesses:
            num_forfeited += 1
        else:
            score += result["num_guesses"]
    return score, num_forfeited


def algScore(bestWord, num_words=20):
    # Play wordle with the chosen bestWord word choice algorithm
    # Return the total score for all games (lower is better)

    score = 0
    num_forfeited = 0

    np.random.seed(0)
    target_word_idx = np.random.choice(
        range(num_answers), size=min(num_words, num_answers), replace=False)

    with mp.Pool(mp.cpu_count()) as pool:
        result = pool.starmap(playWordle, zip(
            [bestWord]*num_words, target_word_idx))

    num_guesses = [a["num_guesses"] for a in result]

    for j in range(len(num_guesses)):
        if num_guesses[j] > g_max_guesses:
            num_guesses[j] = 0
            num_forfeited += 1

    score = sum(num_guesses)
    return score, num_forfeited


if __name__ == "__main__":
    target_word_idx = 1245
    print(f"{word_answers[target_word_idx]}")
    result = wordle(target_word_idx, "medal")
    pass
