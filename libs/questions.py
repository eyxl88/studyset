import random, utils

# All quizzes, flashcard logic found in here.

def create_options(answer: str, option_view_object):
    """
    Randomly chooses MCQ answers from a list and returns dictionary of options \
        A-E, including correct answer.

        Parameters:
            answer (str): 
            option_view_object: Options to choose from.

        Returns:
            options_dict (dict[str, str]): Finalized options dictionary.
    """
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

def multiple_choice(study_dict):
    list_of_keys = list(study_dict.keys())
    for i in range(len(study_dict)):
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_options(answer, study_dict.values())

        utils.print_from_options_dict(options_dict)
        user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
        
        if user_answer == "q":
            return 0
        
        utils.check_answer(user_answer, answer, options_dict)

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
        answer = utils.get_dict_key(study_dict, definition)
        options_dict = create_options(answer, study_dict.keys())
        utils.print_words_from_options_dict(options_dict)

        # Get and check user answer.
        user_answer = input("What is the correct answer? Enter A, B, C, D, or E: ")
        if user_answer == "q":
            return 0
        utils.check_answer_one_word(user_answer, answer, options_dict)

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