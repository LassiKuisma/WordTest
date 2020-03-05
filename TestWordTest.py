import unittest
from unittest.mock import patch

from WordTest import split_lines, new_game_from_file, WordGame


class MyTestCase(unittest.TestCase):
    def test_split_lines(self):
        inp = ["yksi = one", "kaksi = two"]
        split = split_lines(inp)
        self.assertEqual(len(split), 2)
        self.assertEqual(split[0][0], "yksi")
        self.assertEqual(split[0][1], "one")
        self.assertEqual(split[1][0], "kaksi")
        self.assertEqual(split[1][1], "two")

    def test_split_lines_faulty_input(self):
        inp = ["yksi = one", "error is virhe", "cats = dogs"]
        split = split_lines(inp)
        self.assertEqual(len(split), 2)
        self.assertEqual(split[0][0], "yksi")
        self.assertEqual(split[0][1], "one")
        self.assertEqual(split[1][0], "cats")
        self.assertEqual(split[1][1], "dogs")

    @patch('WordTest.get_input', side_effect=['yksi', 'kaksi', 'wrong', '-', 'EXIT', 'n'])
    def test_gameplay_loop(self, inp):
        lines = split_lines(["yksi = one", "kaksi = two", "kolme = three"])
        game = WordGame(lines)
        game.start_game()
        word_one = next(x for x in game.learned_words if x.get_word() == "yksi")
        self.assertEqual(word_one.correct, 1)
        self.assertEqual(word_one.wrong, 0)

        word_two = next(x for x in game.learned_words if x.get_word() == "kaksi")
        self.assertEqual(word_two.correct, 1)
        self.assertEqual(word_two.wrong, 0)

        word_three = next(x for x in game.learned_words if x.get_word() == "kolme")
        self.assertEqual(word_three.correct, 0)
        self.assertEqual(word_three.wrong, 1)


if __name__ == '__main__':
    unittest.main()
