class LearnedWord:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.correct = 0
        self.wrong = 0

    def get_word(self):
        return self.word

    def get_translation(self):
        return self.translation

    def get_amount_correct_guesses(self):
        return self.correct

    def get_amount_wrong_guesses(self):
        return self.wrong

    def increase_correct_guesses(self):
        self.correct = self.correct + 1

    def increase_wrong_guesses(self):
        self.wrong = self.wrong + 1

    def get_percent_correct(self):
        total = self.correct + self.wrong
        if total == 0:
            return 0
        return self.correct / total


# ===========================


class WordGame:
    def __init__(self, words):
        # list of tuples((word, translation), num times guessed correctly, num times guessed wrong)
        self.learned_words = []
        for w in words:
            self.learned_words.append(LearnedWord(w[0], w[1]))

    def start_game(self):
        print("Starting game!")
        print("=" * 20)
        print("I'm going to ask you to translate words. Type in EXIT (all upper case) to exit.")
        should_stop = False
        while not should_stop:
            for word in self.learned_words:
                # Flip the elements in tuple if user wants to do it other way (feature coming soon)
                word_pair = (word.get_translation(), word.get_word())
                result = self.ask_to_translate(word_pair[0], word_pair[1])
                if result == 2:
                    should_stop = True
                    break
                elif result == 0:
                    print("Good!")
                    word.increase_correct_guesses()
                else:
                    word.increase_wrong_guesses()
                    print("Wrong, the word is '%s'." % word_pair[1])
                    print("Type the word so you will remember it")
                    word_again = get_input(word_pair[0] + "=")
                    if word_again.lower() != word_pair[1].lower():
                        print("Check your spelling!")
                        self.notify_check_spelling(word_pair[1], word_again)
            # end of for-loop
        # end of while
        wants_stats = get_input("Game ended! Print stats on how well you did? [y/n]")
        if wants_stats == "y" or wants_stats == "yes":
            self.print_stats()

    def print_stats(self):
        print("Stats:")
        max_len_word = max(max(len(x.get_word()) for x in self.learned_words), len("Word"))
        max_len_trn = max(max(len(x.get_translation()) for x in self.learned_words), len("Translation"))
        print("%s %s %s %s %s" %
              ("Word".ljust(max_len_word),
               "Translation".ljust(max_len_trn),
               "Correct",
               "Wrong",
               "%"))

        sorted_words = sorted(self.learned_words, key=lambda b: b.get_percent_correct(), reverse=True)
        for word in sorted_words:
            print("%s %s %d       %d     %.1f%%" %
                  (word.get_word().ljust(max_len_word),
                   word.get_translation().ljust(max_len_trn),
                   word.get_amount_correct_guesses(),
                   word.get_amount_wrong_guesses(),
                   word.get_percent_correct() * 100.0))

    @staticmethod
    def ask_to_translate(word, translation):
        answer = get_input("\nTranslate '%s':" % word)
        if answer == "EXIT":
            return 2
        if answer.lower() == translation.lower():
            return 0
        else:
            return 1

    @staticmethod
    def notify_check_spelling(first, second):
        error_index = -1
        for i in range(max(len(first), len(second))):
            if i >= len(first) or i >= len(second):
                error_index = i
                break
            if first[i] != second[i]:
                error_index = i
                break
        print(first)
        print(second)
        print(" " * error_index + "^")


# ===========================

def new_game_from_file(path):
    print("Creating new game...")
    print("Loading file...")
    lines = load_words_from(path)
    print("File loaded! Parsing data...")
    spl = split_lines(lines)
    print("Data parsed!")
    # TODO: here we could ask if they want from lang_one -> lang_two or other way around
    return WordGame(spl)


def load_words_from(path):
    lines = []
    with open(path, "r", encoding='utf-8-sig') as file:
        for ln in file:
            ln = ln.replace("\n", "")
            if len(ln) > 0:
                lines.append(ln)
    return lines


# Split lines read from file into tuples containing word and its translation
# line: "One = yksi" -> ("One", "yksi")
def split_lines(lines):
    split_words = []
    for ln in lines:
        split_line = ln.split("=")
        if len(split_line) is not 2:
            print("Error reading line '%s', skipping it." % ln)
        else:
            left = split_line[0].strip()
            right = split_line[1].strip()
            split_words.append((left, right))
    return split_words


def get_input(text):
    return input(text)


if __name__ == '__main__':
    print("Welcome to WordTest program!")

    file_name = get_input("Give file name:")
    game = new_game_from_file(file_name)
    game.start_game()

    print("\nStopping program")

# EOF
