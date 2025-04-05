import json
import random

import hang


GAP = "    "
GAME_ATTEMPTS = len(hang.states) - 1
GAME_OVER = GAME_ATTEMPTS



def download_words(file_name):
    try:
        with open(file_name, "rt", encoding="utf-8") as file:
            words = file.read()
            return json.loads(words)
    except Exception as ex:
        print_error(ex)
        print(f"Can't download from file: {file_name}")
        exit(1)


def get_random_puzzle(words):
    if len(words) == 0:
        print_error("Список слов пуст!")
        exit(1)

    category = random.choice(list(words.keys()))
    word = random.choice(words[category])

    return (category.upper(), word.upper())


def get_not_empty_input(descr="", warning=None, repeat_descr=False):
    line = input(descr)
    descr = descr if repeat_descr else ""
    descr = descr if not warning else (warning + descr)

    while len(line) == 0:
        line = input(descr)

    return line


def get_user_guess(descr="-> "):
    user_input = get_not_empty_input(descr)
    warning_message = "Вы ввели недопустимый символ, можно вводить только буквы.\n"

    while not user_input[0].isalpha():
        print_warning(warning_message)
        user_input = get_not_empty_input(descr)

    return user_input[0].upper()


def print_game_result(res, word):
    if res:
        print(f"\n{GAP}Поздравляем, вы победили!\n")
    else:
        print_hang_state(GAME_OVER)
        print(f"Было загадано слово: {word}\n")


def print_user_field(user_field):
    data = "".join(user_field)
    for row in hang.make_field(data).split("\n"):
        print(f"{GAP}{row}")


def print_hang_state(errors_cnt):
    print(hang.states[errors_cnt])


def print_wrong_attempts(errors):
    print(f"{GAP}Ошибки ({len(errors)}): {','.join(errors)}")


def print_warning(message):
    print(f"[WARNING]: {message}")


def print_error(message):
    print(f"[ERROR]: {message}")


def open_letter(field, letter, word):
    idx = word.find(letter)

    while idx != -1:
        field[idx] = letter
        idx = word.find(letter, idx + 1)


def is_user_want_play(descr_line="-> "):
    answer = get_not_empty_input(descr_line)
    warning_message = "Вы ввели некорректный символ/строку, попробуйте еще!\n"

    while answer[0].upper() not in "ДНYN":
        print_warning(warning_message)
        answer = get_not_empty_input(descr_line)

    return answer[0].upper() in "ДY"


def is_game_over(wrong_attempts, user_field, word):
    if wrong_attempts >= GAME_ATTEMPTS:
        return True
    if "".join(user_field) == word:
        return True

    return False


def is_user_win(wrong_attempts, user_field, word):
    if wrong_attempts >= GAME_ATTEMPTS:
        return False
    if "".join(user_field) != word:
        return False

    return True


def new_game(puzzle):
    category, word = puzzle
    wrong_letters = set()
    user_field = ["*"] * len(word)

    while not is_game_over(len(wrong_letters), user_field, word):
        print_hang_state(len(wrong_letters))
        print_user_field(user_field)
        print(f"{GAP}Категория: {category}")
        print_wrong_attempts(sorted(wrong_letters))

        letter = get_user_guess(f"{GAP}Ваша буква: ")

        if letter not in word:
            wrong_letters.add(letter)
        else:
        	open_letter(user_field, letter, word)

    return is_user_win(len(wrong_letters), user_field, word)


def run_hangman_game(words):
    while is_user_want_play("Вы готовы сыграть? да/нет: "):
        puzzle = get_random_puzzle(words)
        res = new_game(puzzle)
        print_game_result(res, puzzle[1])


if __name__ == "__main__":
    words = download_words("words.json")
    run_hangman_game(words)
