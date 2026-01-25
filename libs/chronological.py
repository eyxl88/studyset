import random
import libs.utils as utils

# All chronological type of question logic found here.

def create_chronological(list_of_terms):
    """
    Generates a dictionary associating letters with each key term.
    
    Parameters:
        list_of_terms (list[str]): list of strings of key terms in random order.

    Returns:
        options_dict (dict[str, str]): dictionary with letters as keys and key terms as values.

    """
    options_dict = {}

    for i in range(len(list_of_terms)):
        key = chr(ord("A") + i) # Assign a letter from A onwards as the key.
        term_to_order = list_of_terms[i] 
        options_dict[key] = term_to_order

    return options_dict

def get_chron_answer(options_dict: dict[str, list[str]], study_dict: dict[str, list[str]]):
    """
    Get the correctly ordered answer in terms of option letters for chronological questions.
    
    Parameters:
        options_dict (dict[str, list[str]]): dict with option letters as keys and definitions as values.
        study_dict (dict[str, list[str]]): dict with key terms as keys and definitions as values.
    
    Returns:
        answer_list (list[str]): list with chronologically ordered letter answer choices.
    
    """
    answer_list = []

    # Find the letter corresponding to each key in study_dict in the original entry order.
    for key in study_dict:
        letter = utils.get_dict_key(options_dict, key)
        answer_list.append(letter)

    return answer_list

def check_chron_answer(user_answer, answer):
    """
    Checks user answer against the correctly ordered answer.
    
    Parameters:
        user_answer (string): string of comma separated letters representing the ordered answers.
        answer (list[str]): list of strings (capital letters) in the correct chronological order.
    
    Returns:
        (0 | 1): 0 if user answer is wrong and 1 if user answer is correct.

    """
    if user_answer == "q":
        return None
    
    # Split user answer into a list by comma and remove empty values, capitalizing letters.
    user_answer = user_answer.split(",")

    while "" in user_answer:
        user_answer.remove("")

    for i in range(len(user_answer)):
        user_answer[i] = user_answer[i].strip().upper()

    # Print correct or incorrect message if user answer is correct or wrong.
    if user_answer == answer:
        print("Correct.\n")
        return 1

    if user_answer != answer:
        print("Incorrect. The correct order was: ", end="")
        utils.print_comma_separated_values(answer)
        print()
        return 0

def chronological(study_dict):
    """
    Manages the chronological question and saves user scores.
    
    Parameters:
        study_dict (dict[str, list[str]]): study set containing key terms and definitions.

    Returns None.

    """
    # Make the key terms of the study set into a list and randomize order.
    list_of_keys = list(study_dict.keys())
    random.shuffle(list_of_keys)
    print("Order the following terms in chronological / logical order: ")

    # Create options for chronological question and print them.
    options_dict = create_chronological(list_of_keys)
    utils.print_words_from_options_dict(options_dict)

    # Get user input and check answer.
    user_answer = input("Which of the following are correct? Enter a list of"\
                        " comma-separated numbers (ie. B,A,D,C,F,E): ")
    
    if user_answer == "q":
        return None
    
    answer = get_chron_answer(options_dict, study_dict)
    check_chron_answer(user_answer, answer)
    
    # Implement save_score()