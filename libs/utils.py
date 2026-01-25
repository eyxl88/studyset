import os, platform, csv, random
import libs.chronological as chrono
import libs.check_question as check

# Bunch of helper functions and stuff I couldn't find the place to actually
# sort them into. Very messy, I know :)

# ==================================== Create ====================================

def create_select_all(answer, study_dict_view_object):
    """
    Takes all possible answers to create a dictionary of select all \
        options with wrong and right answers.
    """
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

def create_numeric_options(options_list):
    options_dict = {}

    for i in range(len(options_list)):
        key = i + 1
        option = options_list[i]
        options_dict[key] = option

    return options_dict

# ==================================== Match ====================================

def match_answers(study_dict):
    """Manages the matching terms quiz version of any given study set."""
    # Set up Question
    terms_list = list(study_dict.keys())
    random.shuffle(terms_list)

    definitions_list = list(study_dict.values())
    random.shuffle(definitions_list)

    options_dict = chrono.create_chronological(definitions_list)
    options_dict_numeric = chrono.create_numeric_options(terms_list)
    
    # Print Question
    print()
    print_words_from_options_dict(options_dict_numeric)
    print_from_options_dict(options_dict)

    user_input = input("Enter the matches in any order in the form 1B,2A,3D,4C: ")
    if input == "q":
        return 0

    check.check_match_answer(user_input, options_dict_numeric, options_dict, study_dict)

# ==================================== CSV Specific ====================================

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
        print("File not found. Try again by pressing 'r' after the main menu prints. \
              Use a valid file name.")
    return dict_read_from_csv

# ==================================== Process ====================================
def process_text(string):
    """Process string by removing empty spaces between words and lower-casing all letters."""
    list_of_words = string.split()
    final_string = ""
    
    # Add lowercased versions of non-empty entries to final string.
    for word in list_of_words:
        if word:
            word = word.lower()
            final_string += word
    
    return final_string


def process_match_input(user_answer, study_dict):
    user_answer_list = user_answer.split(",")
    
    for i in range(len(user_answer_list)):
        try:
            user_answer_list[i] = [int(user_answer_list[i][0]), user_answer_list[i][1].upper()]

        except:
            print("Invalid input. Reloading question...")
            match_answers(study_dict)

    return user_answer_list

# ==================================== Print ====================================

def print_keys(study_dict):
    """Prints all the keys of the dictionary each on its own line."""
    print("Word bank:")
    
    for key in study_dict:
        print(key)

def print_words_from_options_dict(options_dict):
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def print_from_options_dict(options_dict):
    """Prints options A-E from an options dict, separating answer lists onto new \
        lines for printing."""
    for key in options_dict:
        print(f"{key}: {"\n".join(options_dict[key])}")

def print_select_all(options_dict: dict[int, str]):
    """
    Docstring for print_select_all
    
    Parameters:
        options_dict (dict[int, str]): dictionary with numbers (keys) corresponding to definitions (values) 
    
    Returns None.

    """
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def print_comma_separated_values(list_to_print):
    """
    Prints the items in a list with commas and spaces separating them, other than last item.
    
    Parameters:
        list_to_print (list[str]): list containing string items to be printed separated.

    Returns None.

    """
    for i in range(len(list_to_print)):
        if i == len - 1:
            print(list_to_print[i])
        else:
            print(f"{list_to_print[i]}, ")

# ==================================== Select ====================================

def select_all(study_dict):
    list_of_keys = list(study_dict.keys())

    for i in range(len(study_dict)):
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_select_all(answer, study_dict.values())

        print_select_all(options_dict)
        user_answer = input("Which of the following are correct? Enter a list \
                            of comma-separated numbers (ie. 1,3,7): ")
        
        if user_answer == "q":
            return 0
        
        check.check_select_all_answer(user_answer, answer, options_dict)

# =================== Program Specific Functions ===================

def clear_console():
    """
    Clears the terminal/console screen in a cross-platform way.
    Works on Windows, macOS, and Linux.
    """
    try:
        # Detect the OS and run the appropriate command
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as e:
        print(f"Error clearing console: {e}")

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
    print("Press 'exit' to quit.")

# ==================================== Other/Misc ====================================

def write_data(study_dict):
    """Sets up the 'write' test mode and checks answers."""
    list_of_keys = list(study_dict.keys())
    
    for i in range(len(study_dict)):
        
        # Prints word bank and chooses the key term, removing from list of terms to test.
        print_keys(study_dict)
        print()
        key_term = random.choice(list_of_keys)
        list_of_keys.remove(key_term)
        answer = key_term

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
        
        check.check_written_answer(user_answer, answer)

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

def get_dict_key(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key