import random
import libs.utils as utils
import libs.check_question as check
import libs.chronological as chrono

# All quizzes, flashcard logic found in here.

def create_options(answer: str, option_view_object):
    """
    Randomly chooses MCQ answers from a list and returns dictionary of options \
        A-E, including correct answer.

        Parameters:
            answer (str): 
            option_view_object: Options to choose from, view object of a dictionary.

        Returns:
            options_dict (dict[str, str]): Finalized options dictionary.
    """
    # Create a list of options and add the correct answer.
    options_list = []
    options_list.append(answer)

    # Transform option view object into a list and remove the correct answer.
    incorrect_answer_list = list(option_view_object)
    incorrect_answer_list.remove(answer)

    # Choose another 4 random incorrect options to add to options_list.
    for i in range(4):
        new_option = random.choice(incorrect_answer_list)
        incorrect_answer_list.remove(new_option)
        options_list.append(new_option)

    # Assign letters A, B, C, D, E to the randomized options.
    random.shuffle(options_list)
    key_list = ["A", "B", "C", "D", "E"]
    options_dict = {}

    for i in range(len(key_list)):
        options_dict[key_list[i]] = options_list[i]

    return options_dict


def multiple_choice(study_dict: dict[str, list[str]], study_set_name):
    """
    Creates multiple choice questions for each term in the study set and saves user score.
    
    Parameter:
        study_dict (dict[str, list[str]]): study set containing key terms and definitions.
        study_set_name (str): string representing name of study set for save_score purposes.
    
    Returns None.
    
    """
    # Creates list of potential questions from key terms of study set.
    TOTAL_POINTS = len(study_dict)
    list_of_keys = list(study_dict.keys())
    user_correct = 0
    number_of_questions = len(study_dict)
    
    for i in range(len(study_dict)):
        # Clear console
        utils.clear_console()

        # Prints question header and chooses a key term.
        key_term = random.choice(list_of_keys)
        print(f"Question {i + 1} out of {number_of_questions} - {key_term} \n")

        # Removes the chosen key term, finds the correct answer, and creates a question.
        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_options(answer, study_dict.values())

        # Prints question and options.
        utils.print_from_options_dict(options_dict)
        
        while True:
            user_answer = input("\nWhat is the correct answer? Enter A, B, C, D, or E: ")
            
            # Allows user to return to main menu.
            if user_answer == "q":
                return None
            
            try:
                output = check.check_answer(user_answer, answer, options_dict)
                user_correct += output
                utils.pause_input()
                break

            except:
                print("Invalid input. Try again.\n")

        
        print()

    # Print and save user score.
    user_score = user_correct / TOTAL_POINTS * 100
    print(f"Your score is {user_correct} / {TOTAL_POINTS} and your accuracy is {user_score:.2f}%.")
    utils.ask_to_save_score(study_set_name, "mcqdef", user_score)

def multiple_choice_flipped(study_dict: dict[str, list[str]], study_set_name):
    """Generates multiple choice questions with the key term as the answer for
    a given study set, going through all key terms.
    
    Parameters:
        study_dict (dict[str, list[str]]): dictionary with key terms as keys and definitions as answers.
        study_set_name (str): string containing name of current study set.

    Returns None.

    """
    # Convert all definitions in the study dictionary into a list of lists and initialize score vars.
    list_of_values = list(study_dict.values())
    TOTAL_POINTS = len(study_dict)
    user_correct = 0
    number_of_question = len(study_dict)
    
    for i in range(len(study_dict)):

        # Clear console
        utils.clear_console()

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Print question.
        print(f"Question {i + 1} out of {number_of_question}")
        for row in definition:
            print(row)
        else:
            # Add extra space
            print()

        # Set up answer and options.
        answer = utils.get_dict_key(study_dict, definition)
        options_dict = create_options(answer, study_dict.keys())
        utils.print_words_from_options_dict(options_dict)

        while True:
            # Get and check user answer.
            user_answer = input("\nWhat is the correct answer? Enter A, B, C, D, or E: ")
                
            # Allow user to exit mcqkey mode by entering "q" at any time.
            if user_answer == "q":
                return None
                
            try:
                question_score = check.check_answer_one_phrase(user_answer, answer, options_dict)
                utils.pause_input()
                break

            except:
                print("Invalid input. Try again.")
        
        user_correct += question_score

    # Calculate, print, and save score.
    user_score = user_correct / TOTAL_POINTS * 100
    print(f"\nYour score is {user_correct}/{TOTAL_POINTS} and your accuracy is {user_score:.2f}%.")
    utils.ask_to_save_score(study_set_name, "mcqkey", user_score)


def flashcard(study_dict: dict[str, list[str]]):
    """
    Allows user to flip between key terms and definitions, like flashcards.
    
    Parameter:
        study_dict (dict[str, list[str]]): dictionary containing key terms as keys and definitions as values.

    Returns None.

    """
    for key in study_dict:
        print("Press 'f' to flip, 'd' to move on to the next term, and 'q' to return to the main menu.")
        print(key, end=": ")

        user_input = input().strip().lower()
        while user_input == 'f':
            # Prints each line of the definition on its own line.
            for i in range(len(study_dict[key])):
                print(study_dict[key][i])

            user_input = input("Press 'f' to flip, 'd' to move on to the next term,"\
                               " and 'q' to return to the main menu: ")
            
            # Allows user to move on to the next term.
            if user_input == 'd':
                break
            
            # Allows user to leave flashcard mode entirely and return to main menu.
            if user_input == "q":
                return None
            
            else:
                # Prints key term and allows user to decide next action.
                print(key)
                user_input = input("Press 'f' to flip, 'd' to move on to the next"\
                                   " term, and 'q' to return to the main menu: ")
        
        # Allows user to move on to the next term.
        if user_input == "d":
            continue
        
        # Allows user to leave flashcard mode entirely and return to main menu.
        elif user_input == "q":
            return None
        
        else:
            print("Incorrect input. Moving on.")


# ==================================== Write Mode ====================================

def write_mode(study_dict, study_set_name):
    """Sets up the 'write' test mode and checks answers."""
    list_of_keys = list(study_dict.keys())
    user_correct = 0
    TOTAL_POINTS = len(study_dict)
    
    for i in range(len(study_dict)):
        # Clear console
        utils.clear_console()
        
        # Prints word bank and chooses the key term, removing from list of terms to test.
        utils.print_keys(list_of_keys)
        print()
        key_term = random.choice(list_of_keys)
        list_of_keys.remove(key_term)
        answer = key_term

        print("Question", i + 1, "out of", len(study_dict), end=" - ")

        # Prints the definition neatly on multiple lines if necessary.
        for i in range(len(study_dict[key_term])):
            if i == len(study_dict[key_term]) - 1:
                print(study_dict[key_term][i])
            else:
                print(study_dict[key_term][i], end=", ")

        # Get user input and check if correct.
        while True:
            user_answer = input("Type the key term which corresponds"
                                    " to the given definition: ")
            if user_answer == "q":
                return 0
            
            try:
                user_correct += check.check_written_answer(user_answer, answer)
                utils.pause_input()
                break
            
            except:
                print("Invalid input. Try again.")

    # Calculate and save user score.
    user_score = user_correct / TOTAL_POINTS * 100
    print(f"You scored {user_score:.2f}%")
    utils.ask_to_save_score(study_set_name, "write", user_score)


# ==================================== Match ====================================

def match_answers(study_dict, study_set_name):
    """
    Manages the matching terms quiz version of any given study set.
    
    Parameters:
        study_dict (dict[str, list(str)]): dictionary of key terms and lists of definitions.
        study_set_name: name of study set
    
    Returns:
        None
    
    """
    # Set up Question
    terms_list = list(study_dict.keys())
    random.shuffle(terms_list)

    definitions_list = list(study_dict.values())
    random.shuffle(definitions_list)

    options_dict = chrono.create_chronological(definitions_list)
    options_dict_numeric = utils.create_numeric_options(terms_list)
    
    # Print Question
    print()
    utils.print_words_from_options_dict(options_dict_numeric)
    utils.print_from_options_dict(options_dict)
    
    while True:
        user_input = input("Enter the matches in any order in the form 1B,2A,3D,4C: ")
        if user_input == "q":
            return 0

        # Calculate, print, and save score.
        try:
            user_score = check.check_match_answer(user_input, options_dict_numeric, 
                                            options_dict, study_dict) * 100
            break

        except:
            print("Invalid input. Try again or enter q to exit.")
    
    # Prints and saves user overall score
    print(f"You scored {user_score:.2f}%!")
    utils.ask_to_save_score(study_set_name, "match", user_score)

# ==================================== Select ====================================

def select_all(study_dict, study_set_name):
    """Generates select all questions with definitions as answers for each key term 
    in a studyset.
    
    Parameters:
        study_dict (dict[str, list[str]]): study set with key terms and definitions
        study_set_name (str): name of the study set for save_score purposes
    
    Returns:
        None

    """
    TOTAL = len(study_dict)
    user_correct = 0
    list_of_keys = list(study_dict.keys())
    is_correct_answer_shown = input("Would you like to see the number of correct answers in each question? (y/n): ")
    is_correct_answer_shown = is_correct_answer_shown == "y"

    # Clear console
    utils.clear_console()

    for i in range(len(study_dict)):
        # Selects key term and prints question header.
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, "out of", len(study_dict), " - ", key_term)

        # Removes key term from list, finds answer, creates and prints options.
        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = utils.create_select_all(answer, study_dict.values(), is_correct_answer_shown)
        
        utils.print_select_all(options_dict)
        print()
        
        while True:
            user_answer = input("Which of the following are correct? Enter a list"\
                                " of comma-separated numbers (ie. 1,3,7): ")
            
            # Allows user to return to main menu.
            if user_answer == "q":
                return None
            
            try:
                user_correct += check.check_select_all_answer(user_answer, 
                                                    answer, options_dict)
                
                # Let user know their answer and then clean the console
                utils.pause_input()
                utils.clear_console()

                break
            except:
                print("Invalid input. Try again.")

    # Print and save user score.
    user_score = user_correct / TOTAL * 100
    print(f"Your score is {user_correct} / {TOTAL} and"\
        f" your accuracy is {user_score:.2f}%.")
    utils.ask_to_save_score(study_set_name, "selectall", user_score)