import libs.utils as utils

ACCEPTED_MCQ_LIST = ["A", "B", "C", "D", "E"]

# All answer checking found here.

def check_answer(user_answer, answer, options_dict):
    """Checks if user answer is correct.
    
    Parameters: 
    --user_answer: string which should be a key in options_dict
    --answer: list with 1+ items which is the correct answer (definition)
    --options_dict: dictionary with option letters or numbers as keys and 
                    the answer text as values.

    Returns:
        None: if user input is invalid
        (0 | 1): depends on whether user gets the answer correct (1) or wrong (0)
    
    """
    # Reformat string as capital letter and check if user answer matches real answer.
    user_answer = user_answer.upper().strip()
    
    # Return None for invalid inputs to trigger exception in mcqdef main function.
    if user_answer not in ACCEPTED_MCQ_LIST:
        return None
    
    # If answer is correct
    if answer == options_dict[user_answer]:
        print("Correct")
        print()
        return 1

    # If initial answer is incorrect
    else:
        # Second chance for user to answer correctly.
        user_answer = input("Incorrect. One last try: ")
        user_answer.upper().strip()
            
        if answer == options_dict[user_answer]:
            print("Correct")
            print()
                    
        else:
            # Print the correct answer on multiple lines if the answer list consists
            # of more than one line of definitions.
            print(f"The correct answer is {"\n".join(answer)}")
            print()
            
        return 0


def check_answer_one_phrase(user_answer, answer, options_dict):
    """Checks user answer with answer when the correct answer is a word or phrase.
    
    Parameters:
        user_answer (str): string which should be a single letter key in options_dict.
        answer (str): string which is the correct answer
        options_dict (str): dictionary containing the question choices and associated text.

    Returns:
        (0 | 1): depends on whether user answer is correct (1) or wrong (0).
        None: if the input is invalid.

    """
    
    # Reformat user text as a capital letter without spaces and check.
    user_answer = user_answer.strip().upper()
        
    if answer == options_dict[user_answer]:
        print("Correct")
        print()
        return 1
        
    # Return none to trigger exception in question function.
    elif user_answer not in ACCEPTED_MCQ_LIST:
        print("Invalid input. Try again.")
        return None

    else:
        # Second chance for user to answer correctly.
        user_answer = input("Incorrect. One last try: ")
        user_answer.upper().strip()

        if answer == options_dict[user_answer]:
            print("Correct!")
            print()

        # Print incorrect answer message.
        else:
            print(f"The correct answer is {answer}")
            print()
        
        return 0


def check_select_all_answer(user_answer, answer, options_dict):
    """
    Checks user answers for select all mode against correct answers.
    
    Parameters:
        user_answer (str): user answer as a comma separated string of numbers
        answer (list[str]): correct answer with a list of string options
        options_dict (dict[int: str]): dictionary of integers corresponding to string answers.
    
    Returns:
        user_score (0 | 1): depends on whether user answers are correct (1) or wrong (0).
        None: triggers exception in select_all function for invalid input
    
    """
    
    # Turn user answer string into user answer list.
    if "," in user_answer:
        user_answer = user_answer.split(",")
    else:
        user_answer = list(user_answer)

    # Remove blank entries from the user answer list.
    user_answer = [int(i) for i in user_answer if i.isspace() != True]
    user_answer.sort()

    # Initialize tracking variables.
    user_total = 0
    user_correct_answers = []
    user_incorrect_answers = []
    correct_total = len(answer)

    for num in user_answer:
        if num not in options_dict.keys():
            return None

        if options_dict[num] in answer:
            user_total += 1
            user_correct_answers.append(num)

        else:
            user_incorrect_answers.append(num)
    
    # If the user selects all correct answers.
    if user_total == correct_total and len(user_incorrect_answers) == 0:
        print(f"Correct! You selected {user_total}/{correct_total} correct answers"\
              " and 0 wrong answers!\n")
        
        return 1

    # If the user selects additional wrong answers.
    elif user_total == correct_total and len(user_incorrect_answers) != 0:
        print(f"Almost there! You selected {user_total}/{correct_total} correct"\
             f" answers and {len(user_incorrect_answers)} wrong answers!")
        print(f"The following answers were incorrect: {", ".join(user_incorrect_answers)}\n")
        
        return 0

    # If the user selects multiple wrong answers and not enough correct answers.
    elif user_total != correct_total and len(user_incorrect_answers) != 0:
        print(f"Incorrect. You selected {user_total}/{correct_total} correct answers"\
              f" and {len(user_incorrect_answers)} wrong answers!")
        print(f"The correct answers included:\n{"\n".join(answer)}")
        print(f"You additionally selected these wrong answers:")
        utils.print_comma_separated_values(user_incorrect_answers) 
        print()

        return 0
    
    # If the user does not select all the correct answers, but didn't select the wrong answers.
    else:
        print(f"Incorrect. You selected {user_total}/{correct_total}"\
            f" correct answers and 0 wrong answers.")
        print(f"The correct answers included:\n{"\n".join(answer)}\n")
        
        return 0

def check_written_answer(user_answer, answer):
    """
    Checks written answers against actual answers and prints relevant messages.
    
    Parameters:
        user_answer (str): string entered by user representing key term.
        answer (str): the correct key term.

    Returns:
        (0 | 1): depends on whether user enters the correct answer (1) or incorrect answer (0).
    
    """
    # Process user answer and the correct answer so they can be compared.
    user_answer = utils.process_text(user_answer)
    answer_processed = utils.process_text(answer)
    
    # Check and print relevant (in)correct answer messages.
    if user_answer == answer_processed:
        print("Correct.\n")
        return 1
    
    elif user_answer in answer_processed:
        print(f"Close. The answer was '{answer}'.\n")
        return 0
    
    elif answer_processed in user_answer:
        print(f"Almost there. The answer is just '{answer}'.\n")
        return 0

    else:
        print(f"Incorrect. The answer is '{answer}'.\n")
        return 0

def check_match_answer(user_answer, options_dict_numeric, options_dict, study_dict):
    """
    Takes user answer, the matching option dictionaries, and actual study set to 
    check if answers are correct. 
    
    Parameters:
        user_answer (str): 
        options_dict_numeric (dict[int, str]): dictionary with numbers linked to key terms.
        options_dict (dict[str, list[str]]): dictionary with letters linked to definitions.
        study_dict (dict[str, list[str]]): dictionary with key terms and definitions.

    Returns:
        user_score (int | float): depends on whether user_answer is correct (1) or incorrect.

    """
    TOTAL_POINTS = len(study_dict)
    
    matches_correct = 0
    match_correct_list = []
    matches_wrong = []
    right_matches = []
    user_answer = utils.process_match_input(user_answer, options_dict_numeric, options_dict)

    if user_answer == "InvalidInput":
        return None
    
    # Count how many correct matches there are and append each wrong match to matches_wrong.
    for list in user_answer:
        key = options_dict_numeric[list[0]]
        answer = options_dict[list[1]]
        
        if study_dict[key] == answer:
            matches_correct += 1
            match_correct_list.append(list[0])
            print(match_correct_list)
        
        else:
            matches_wrong.append(f"{list[0]}{list[1]}")
            right_matches.append(f"{list[0]}{utils.get_dict_key(options_dict, study_dict[key])}")
    
    if matches_correct == TOTAL_POINTS:
        print("All correct! Good job.\n")
        user_score = 1
    
    else:
        print(f"Incorrect, you scored {matches_correct} / {TOTAL_POINTS}.")
        print("Incorrect matches:")

        # Print incorrect matches and correct answers.
        for i in range(len(matches_wrong)):
            print(f"{matches_wrong[i]} should be {right_matches[i]}")
        
        print()
        
        if len(matches_wrong) + len(match_correct_list) < TOTAL_POINTS:
            print("You forgot to include these matches: ")
            
            # Check if there are matches (key integers) not in the user's answers.
            for key in options_dict_numeric:
                print(key)
                for item in matches_wrong:
                    print(item)
                    for correct_answer in match_correct_list:
                        print(correct_answer)
                        if str(key) not in item and str(key) not in correct_answer:
                            print("x")
                            answer = utils.get_dict_key(options_dict, study_dict[key])
                            print(f"{key}{answer}")

        user_score = matches_correct / TOTAL_POINTS
    
    return user_score