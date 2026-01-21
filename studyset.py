#Flashcards
#Enter key terms and definitions:


import csv
import random
from utils import clear_console


def enter_data():
    """Gets user to input study set and returns a dictionary."""
    print("Data Entry: Enter key terms and definitions as prompted.\nEnter 'done' to quit.")
    entry_dict = {}
    key = input("Input key term: ")
    while key != 'done':
        definition_list = [] 
        def_input = ""
        while True:
            def_input = input("Input definition(s) of key term or 'f' to finish this term: ")
            if def_input == "f":
                break
            definition_list.append(def_input)
        entry_dict[key] = definition_list
        key = input("Input key term: ")
    return entry_dict

def save_data_to_csv(entry_dict):
    name = input("Enter name of csv file to save: ")
    if not(name.endswith(".csv")):
        name += ".csv"
    with open(name, "a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        import os
        print(os.path.abspath(name))
        for key in entry_dict:
            list_to_write = []
            list_to_write = [key] + entry_dict[key]
            csv_writer.writerow(list_to_write)

def read_data_from_csv():
    """Takes csv file and reads csv file into test-ready dictionary."""
    csv_to_read = input("Input name of csv to read with extension: ")
    dict_read_from_csv = {}
    try:
        with open(csv_to_read, "r") as csv_to_read:
            csv_reader = csv.reader(csv_to_read, delimiter=",")
            for row in csv_reader:
                if not row:
                    continue
                else:
                    key = row[0]
                    definition = row[1:]
                    dict_read_from_csv[key] = definition
    except:
        print("File not found. Try again by pressing 'r' after the main menu prints. Use a valid file name.")
    return dict_read_from_csv

def check_answer(user_answer, answer, options_dict):
    try:
        user_answer.upper().strip()
        if answer == options_dict[user_answer]:
            print("Correct")
            print()
        else:
            user_answer = input("Incorrect. One last try: ")
            if answer == options_dict[user_answer]:
                print("Correct")
                print()
            else:
                print(f"The correct answer is {"\n".join(answer)}")
                print()
    except:
        print("Invalid entry. Moving to next question.\n")

def create_options(answer, option_view_object):
    """Randomly chooses MCQ answers from a list and returns dictionary of options A-E, including correct answer."""
    options_list = []
    options_list.append(answer)

    possible_answer_list = list(option_view_object)
    possible_answer_list.remove(answer)

    for i in range(4):
        new_option = random.choice(possible_answer_list)
        possible_answer_list.remove(new_option)
        options_list.append(new_option)

    random.shuffle(options_list)

    key_list = ["A", "B", "C", "D", "E"]
    options_dict = {}

    for i in range(len(key_list)):
        options_dict[key_list[i]] = options_list[i]

    return options_dict

def print_from_options_dict(options_dict):
    """Prints options A-E from an options dict, separating answer lists onto new lines for printing."""
    for key in options_dict:
        print(f"{key}: {"\n".join(options_dict[key])}")

def multiple_choice(study_dict):
    list_of_keys = list(study_dict.keys())
    for i in range(len(study_dict)):
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_options(answer, study_dict.values())

        print_from_options_dict(options_dict)
        user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
        
        if user_answer == "q":
            return 0
        
        check_answer(user_answer, answer, options_dict)

def get_dict_key(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key

def print_words_from_options_dict(options_dict):
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def check_answer_one_word(user_answer, answer, options_dict):
    try:
        user_answer.upper().strip()
        if answer == options_dict[user_answer]:
            print("Correct")
            print()
        else:
            user_answer = input("Incorrect. One last try: ")
            if answer == options_dict[user_answer]:
                print("Correct")
                print()
            else:
                print(f"The correct answer is {answer}")
                print()
    except:
        print("Invalid entry. Moving to next question.\n")

def multiple_choice_flipped(study_dict):
    list_of_values = list(study_dict.values())
    for i in range(len(study_dict)):

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Print question.
        print("Question", i + 1)
        for row in definition:
            print(row)
        
        # Set up answer and options.
        answer = get_dict_key(study_dict, definition)
        options_dict = create_options(answer, study_dict.keys())
        print_words_from_options_dict(options_dict)

        # Get and check user answer.
        user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
        if user_answer == "q":
            return 0
        check_answer_one_word(user_answer, answer, options_dict)

def create_select_all(answer, study_dict_view_object):
    """Takes all possible answers to create a dictionary of select all options with wrong and right answers."""
    study_dict_choices = [item for item in study_dict_view_object]
    study_dict_choices.remove(answer)
    select_all_choices = []

    for list in study_dict_choices:
        for item in list:
            select_all_choices.append(item)

    random.shuffle(select_all_choices)
    select_all_choices = select_all_choices[:6]
    select_all_choices.extend(answer)
    random.shuffle(select_all_choices)
    select_all_options_dict = {}

    for i in range(len(select_all_choices)):
        key = i + 1
        select_all_options_dict[key] = select_all_choices[i]

    return select_all_options_dict

def print_select_all(options_dict):
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def check_select_all_answer(user_answer, answer, options_dict):
    # Turn user answer string into user answer list.
    user_answer = user_answer.split(",")
    # Remove blank entries from the user answer list.
    user_answer = [int(i) for i in user_answer if i.isspace() != True]
    user_answer.sort()
    user_total = 0
    user_correct_answers = []
    user_incorrect_answers = []
    correct_total = len(answer)

    for num in user_answer:
        if options_dict[num] in answer:
            user_total += 1
            user_correct_answers.append(num)
        else:
            user_incorrect_answers.append(num)

    if user_total == correct_total and len(user_incorrect_answers) == 0:
        print(f"Correct! You selected {user_total}/{correct_total} correct answers and 0 wrong answers!")

    elif user_total == correct_total and len(user_incorrect_answers) != 0:
        print(f"Almost there! You selected {user_total}/{correct_total} correct\
             answers and {len(user_incorrect_answers)} wrong answers!")
        print(f"The following answers were incorrect: {", ".join(user_incorrect_answers)}")   

    elif user_total != correct_total and len(user_incorrect_answers) != 0:
        print(f"Incorrect. You selected {user_total}/{correct_total} correct answers \
              and {len(user_incorrect_answers)} wrong answers!")
        print(f"The correct answers included:\n{"\n".join(answer)}")
        print(f"You additionally selected these wrong answers:")

        for i in range(len(user_incorrect_answers)):
            if i == len - 1:
                print(user_incorrect_answers[i])
            else:
                print(f"{user_incorrect_answers[i]}, ")
    else:
         print(f"Incorrect. You selected {user_total}/{correct_total} correct answers and 0 wrong answers.")
         print(f"The correct answers included:\n{"\n".join(answer)}")

def select_all(study_dict):
    list_of_keys = list(study_dict.keys())

    for i in range(len(study_dict)):
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_select_all(answer, study_dict.values())

        print_select_all(options_dict)
        user_answer = input("Which of the following are correct? Enter a list of comma-separated numbers (ie. 1,3,7): ")
        
        if user_answer == "q":
            return 0
        
        check_select_all_answer(user_answer, answer, options_dict)

def process_text(user_answer):
    """Returns lowercased, spaceless string containing only letters without numbers or punctuation."""
    user_answer = user_answer.strip().lower()
    user_answer_list = user_answer.split("")
    
    user_answer_processed = ""
    
    for letter in user_answer:
        if letter.isalnum() and not (letter.isdigit()):
            user_answer_processed += letter
    
    return user_answer_processed

def check_written_answer(user_answer, answer):
    """Checks written answers against actual answers and prints relevant messages."""
    user_answer = process_text(user_answer)
    answer_processed = process_text(answer)
    if user_answer == answer_processed:
        print("Correct.\n")
    
    elif user_answer in answer_processed:
        print(f"Close. The answer was '{answer}'.\n")
    
    elif answer_processed in user_answer:
        print(f"Almost there. The answer is just '{answer}'.\n")

    else:
        print(f"Incorrect. The answer is '{answer}'.\n")

def print_keys(study_dict):
    """Prints all the keys of the dictionary each on its own line."""
    print("Word bank:")
    
    for key in study_dict:
        print(key)

def write(study_dict):
    """Sets up the 'write' test mode and checks answers."""
    list_of_keys = list(study_dict.keys())
    
    for i in range(len(study_dict)):
        
        # Prints word bank and chooses the key term, removing from list of terms to test.
        print_keys(study_dict)
        print()
        key_term = random.choice(list_of_keys)
        list_of_keys.remove(key_term)
        answer = study_dict[key_term]

        print("Question", i + 1, end=" ")

        # Prints the definition neatly on multiple lines if necessary.
        for i in range(len(study_dict[key_term])):
            if i == len(study_dict[key_term]) - 1:
                print(study_dict[key_term][i])
            else:
                print(study_dict[key_term][i], end=", ")

        # Get user input and check if correct.
        user_answer = input("Type the key term which corresponds to the given definition: ")
        
        if user_answer == "q":
            return 0
        
        check_written_answer(user_answer, answer)

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
        letter = get_dict_key(options_dict, key)
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
    print_words_from_options_dict(options_dict)

    # Get user input and check answer.
    user_answer = input("Which of the following are correct? Enter a list of comma-separated numbers (ie. B,A,D,C,F,E): ")
    if user_answer == "q":
        return 0
    
    answer = get_chron_answer(options_dict, study_dict)
    check_chron_answer(user_answer, answer)

def flashcard(study_dict):
    for key in study_dict:
        print("Press 'f' to flip, 'd' to move on to the next term, and 'q' to return to the main menu.")
        print(key, end=": ")
        user_input = input().strip().lower()
        while user_input == 'f':
            for i in range(len(study_dict[key])):
                print(study_dict[key][i])
            user_input = input("Press 'f' to flip, 'd' to move on to the next term, and 'q' to return to the main menu: ")
            if user_input == 'd':
                break
            if user_input == "q":
                return 0
            else:
                print(key)
                user_input = input("Press 'f' to flip, 'd' to move on to the next term, and 'q' to return to the main menu: ")
        if user_input == "d":
            continue
        elif user_input == "q":
            return 0

def create_numeric_options(options_list):
    options_dict = {}
    for i in range(len(options_list)):
        key = i + 1
        option = options_list[i]
        options_dict[key] = option
    return options_dict

def process_match_input(user_answer):
    user_answer_list = user_answer.split(",")
    for i in range(len(user_answer_list)):
        try:
            user_answer_list[i] = [int(user_answer_list[i][0]), user_answer_list[i][1].upper()]
        except:
            print("Invalid input. Reloading question...")
            match(newest_dict)
    return user_answer_list

def check_match_answer(user_answer, options_dict_numeric, options_dict, study_dict):
    """Takes user answer, the matching option dictionaries, and actual study set to check if answers are correct."""
    matches_correct = 0
    matches_wrong = []
    right_matches = []
    TOTAL_POINTS = len(study_dict)
    user_answer = process_match_input(user_answer)
    
    for list in user_answer:
        key = options_dict_numeric[list[0]]
        answer = options_dict[list[1]]
        
        if study_dict[key] == answer:
            matches_correct += 1
        
        else:
            matches_wrong.append(f"{list[0]}{list[1]}")
            right_matches.append(f"{list[0]}{get_dict_key(options_dict, answer)}")
    
    if matches_correct == TOTAL_POINTS:
        print("All correct! Good job.")
    
    else:
        print(f"Incorrect, you scored {matches_correct} / {TOTAL_POINTS}.")
        print("Incorrect matches:")
        for i in range(len(matches_wrong)):
            print(f"{matches_wrong[i]} should be {right_matches[i]}")

def match(study_dict):
    """Manages the matching terms quiz version of any given study set."""
    # Set up Question
    terms_list = list(study_dict.keys())
    random.shuffle(terms_list)
    definitions_list = list(study_dict.values())
    random.shuffle(definitions_list)
    options_dict = create_chronological(definitions_list)
    options_dict_numeric = create_numeric_options(terms_list)
    
    # Print Question
    print()
    print_words_from_options_dict(options_dict_numeric)
    print_from_options_dict(options_dict)
    user_input = input("Enter the matches in any order in the form 1B,2A,3D,4C: ")
    if input == "q":
        return 0
    check_match_answer(user_input, options_dict_numeric, options_dict, study_dict)

def print_menu():
    print("Press 'c' to create a study set.")
    print("Press 's' to save a created study set to a csv file.")
    print("Press 'r' to read a study set from a csv file.")
    print("Press 'mcqdef' to be quizzed with mcq questions with definitions as answers.")
    print("Press 'mcqkey' to be quizzed with MCQ questions with key terms as answers.")
    print("Press 'selectall' to be quizzed with Select All questions (definitions as answers).")
    print("Press 'w' to be quizzed by writing the key term corresponding to the definition.")
    print("Press 'm' to be quizzed by matching key terms to definitions.")
    print("Press 'fc' for flashcard mode of studying.")
    print("Press 'chr' to be quizzed with ordering questions on key terms.")
    print("Press 'q' to quit.")

global newest_dict
newest_dict = {}

# Main program loop
def main():
    clear_console()

    print_menu()
    user_input = input()

    while user_input != 'q':
        if user_input == 'c':
            newest_dict = enter_data()

        elif user_input == 's':
            save_data_to_csv(newest_dict)

        elif user_input == 'r':
            newest_dict = read_data_from_csv()

        elif user_input == 'mcqdef':
            multiple_choice(newest_dict)

        elif user_input == 'mcqkey':
            multiple_choice_flipped(newest_dict)

        elif user_input == "selectall":
            select_all(newest_dict)

        elif user_input == "w":
            write(newest_dict)

        elif user_input == "m":
            match(newest_dict)

        elif user_input == "fc":
            flashcard(newest_dict)

        elif user_input == "chr":
            chronological(newest_dict)

        print_menu()
        user_input = input()

    else:
        clear_console()

main()
