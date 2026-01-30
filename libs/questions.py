import random
import libs.utils as utils
import libs.check_question as check

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

    Returns None.
    
    """
    # Creates list of potential questions from key terms of study set.
    TOTAL_POINTS = len(study_dict)
    list_of_keys = list(study_dict.keys())
    user_correct = 0
    
    for i in range(len(study_dict)):
        # Prints question header and chooses a key term.
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        # Removes the chosen key term, finds the correct answer, and creates a question.
        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_options(answer, study_dict.values())

        # Prints question and options.
        utils.print_from_options_dict(options_dict)
        user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
        
        # Allows user to return to main menu.
        if user_answer == "q":
            return None
        
        output = check.check_answer(user_answer, answer, options_dict)
        user_correct += output
    
    print()

    # Print and save user score.
    user_score = user_correct / TOTAL_POINTS
    print(f"Your score is {user_correct} / {TOTAL_POINTS} and your accuracy is {user_score * 100:.2f}%.")
    
    # UPDATE ME: once study_set_name tracking is implemented.
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
    global completion
    list_of_values = list(study_dict.values())
    TOTAL_POINTS = len(study_dict)
    user_correct = 0
    
    for i in range(len(study_dict)):

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Print question.
        print("Question", i + 1)
        for row in definition:
            print(row)
        
        # Set up answer and options.
        answer = utils.get_dict_key(study_dict, definition)
        options_dict = create_options(answer, study_dict.keys())
        utils.print_words_from_options_dict(options_dict)
        completion = False

        while completion != True:
            # Get and check user answer.
            user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
            
            # Allow user to exit mcqkey mode by entering "q" at any time.
            if user_answer == "q":
                return None
            
            question_score = utils.check_answer_one_phrase(user_answer, answer, options_dict)

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