import random
import libs.utils as utils

# All chronological type of question logic found here.

def create_chronological(list_of_terms):
    options_dict = {}
    for i in range(len(list_of_terms)):
        key = chr(ord("A") + i)
        term_to_order = list_of_terms[i]
        options_dict[key] = term_to_order

    return options_dict

def get_chron_answer(options_dict, study_dict):
    answer_list = []
    for key in study_dict:
        letter = utils.get_dict_key(options_dict, key)
        answer_list.append(letter)

    return answer_list

def check_chron_answer(user_answer, answer):
    if user_answer == "q":
        return 0
    
    user_answer = user_answer.split(",")

    for i in range(len(user_answer)):
        if not(user_answer[i]):
            continue

        user_answer[i] = user_answer[i].strip().upper()

    if user_answer == answer:
        print("Correct.\n")

    if user_answer != answer:
        print("Incorrect. The correct order was: ", end="")

        for i in range(len(answer)):
            if i != len(answer) - 1:
                print(answer[i], end=", ")
            else:
                print(answer[i])
                print()

def chronological(study_dict):
    list_of_keys = list(study_dict.keys())
    random.shuffle(list_of_keys)
    print("Order the following terms in chronological / logical order: ")

    options_dict = create_chronological(list_of_keys)
    utils.print_words_from_options_dict(options_dict)

    # Get user input and check answer.
    user_answer = input("Which of the following are correct? Enter a list of comma-separated numbers (ie. B,A,D,C,F,E): ")
    if user_answer == "q":
        return 0
    
    answer = get_chron_answer(options_dict, study_dict)
    check_chron_answer(user_answer, answer)