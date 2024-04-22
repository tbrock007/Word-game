import random
import sys
from collections import Counter

# Function to load words from the file
def load_words(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            words.append(line.strip().lower())
    return words

# Function to find valid words
def valid_words(all_words, letters, min_len, max_len):
    valids = []
    letter_count = Counter(letters)
    for word in all_words:
        if min_len <= len(word) <= max_len and Counter(word) <= letter_count:
            valids.append(word)
    return valids

# Function to display the current guesses
def display_guesses(current_guesses, word_counts, max_len, min_len):
    for i in range(min_len, max_len + 1):
        to_display = []
        for guess in current_guesses:
            if len(guess) == i:
                to_display.append(guess)
        to_display.sort()
        # Fill the rest with placeholders
        while len(to_display) < word_counts[i]:
            to_display.append('-' * i)
        print(to_display)

def main():
    # Load the words from the file
    words = load_words("words-1.txt")

    # Get the word length range from the user
    min_length, max_length = map(int, input("Enter the word length range (min,max): ").split(','))

    # Check if a word is passed as command-line argument
    if len(sys.argv) > 1:
        base_word = sys.argv[1]
        if not (min_length <= len(base_word) <= max_length):
            print("The provided word doesn't fit the length range.")
            return
    else:
        # Pick a random word
        base_word = random.choice([w for w in words if min_length <= len(w) <= max_length])

    guessed_words = []
    all_valid_words = valid_words(words, base_word, min_length, max_length)

    # Count the valid words of each length
    word_counts = {}
    for length in range(min_length, max_length + 1):
        word_counts[length] = sum(1 for word in all_valid_words if len(word) == length)

    while True:
        # Shuffle the base word
        shuffled_word = list(base_word)
        random.shuffle(shuffled_word)
        print("\nCurrent word: " + ''.join(shuffled_word) + "\n")
        display_guesses(guessed_words, word_counts, max_length, min_length)
        
        guess = input("Your guess (or 'q' to quit): ").lower()

        if guess == 'q':
            break
        if guess in all_valid_words and guess not in guessed_words:
            print("Nice! You got one!\n")
            guessed_words.append(guess)
        else:
            print("Oops, try again or guess another word!\n")

    print("\nWords you guessed:")
    display_guesses(guessed_words, word_counts, max_length, min_length)

    print("\nAll possible words were:")
    print(sorted(all_valid_words))

if __name__ == "__main__":
    main()
