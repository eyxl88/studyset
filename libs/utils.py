import os, platform, csv, random
import libs.chronological as chrono
import libs.check_question as check
from datetime import datetime

# Bunch of helper functions and stuff I couldn't find the place to actually
# sort them into. Very messy, I know :)

# ==================================== Constants =================================
ACCEPTED_READ_SCORE_INPUTS = ["mode", "all", "q"]
ACCEPTED_STUDY_MODE_LIST = ["mcqdef", "mcqkey", "write", "match", "selectall", "chron"]
LATEX_DICT = {
    "pia": f"\pi_a",
    "pie": f"\pi_e",
    "pit": f"\pi_t",
    "pit+1": "\pi_{t+1}",
    "Etpit+1": "E_t\pi_{t+1}",
    "Etpit": "E_t\pi_t",
    "mu": r"\mu",
    "yt": r"y_t",
    "Yt": r"Y_t",
    "Kt": r"K_t",
    "kt": r"k_t",
    ">=": r"geq",
    "<=": r"leq",
    "!=": r"neq",
    "AtNt": r"A_t N_t",
    "Yt+1": r"Y_{t+1}"
}

LATEX_NON_STRICT = {
    "kdott": r"\dot{k}_t",
    "ktalpha": r"k_t^\alpha",
    "Ktalpha": r"K_t^\alpha",
    "alpha": r"\alpha",
    "beta": r"\beta",
    "rho": r"\rho",
    "kdot": r"\dot{k}",
    "ydot": r"\dot{y}",
    "Kdot": r"\dot{K}",
    "Ydot": r"\dot{Y}",
    "Ualpha": r"u^{\alpha}",
    "U*": r"U^\text{*}",
    "y*": r"y^\text{*}",
    "pi0": r"\pi_0",
    "delta": r"\delta"
}

# ==================================== Create ====================================

def create_select_all(answer, study_dict_view_object, is_correct_answer_shown = False):
    """
    Takes all possible answers to create a dictionary of select all \
        options with wrong and right answers.
    """
    if is_correct_answer_shown:
        print(f"There are {len(answer)} correct answer(s)\n")

    study_dict_choices = [item for item in study_dict_view_object]
    study_dict_choices.remove(answer)
    select_all_choices = []
    number_of_choices = random.randint(-2, 4) + 6

    for list in study_dict_choices:
        for item in list:
            select_all_choices.append(item)

    # Select questions for user
    random.shuffle(select_all_choices)
    select_all_choices = select_all_choices[:number_of_choices]

    # Add back correct answer
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


# ==================================== CSV Specific ====================================

def save_data_to_csv(entry_dict: dict[str, list[str]]):
    """
    Saves dictionary data to csv file containing key terms and definitions.
    
    Parameters:
        entry_dict (dict[str, list[str]]): dictionary containing the study set to save.
    
    Returns:
        study_set_name (str): string representing name of study set needed to save scores.
    
    """
    name = input("Enter name of csv file to save: ")
    file_path = ""
    
    # Save study set name to variable and prepare file name for reading.
    if not(name.endswith(".csv")):
        study_set_name = name
        name += ".csv"
    else:
        study_set_name = name[:-4] # Remove .csv extension from name

    name = os.path.join("test_files", name)
    with open(name, "a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        file_path = os.path.abspath(name)
        print(os.path.abspath(name))
        
        # Write each row to the csv file.
        for key in entry_dict:
            list_to_write = [] # Clear list_to_write.
            list_to_write = [key] + entry_dict[key]
            csv_writer.writerow(list_to_write)

    input("Your file has been saved. Press any key to contine...")
    return study_set_name, file_path

def read_data_from_csv(csv_to_read):
    """Takes csv file and reads csv file into test-ready dictionary."""
    csv_to_read = os.path.abspath(csv_to_read)
    study_set_name = csv_to_read[:-4] # Remove .csv extension
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
        print("File not found. Try again by pressing 'r' after the main menu prints." \
              " Use a valid file name.")
        pause_input()
        dict_read_from_csv, study_set_name = None, None
        
    return dict_read_from_csv, study_set_name

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


def process_match_input(user_answer, options_dict_numeric, options_dict):
    """Turns match string input into a list of lists in the form list[list[int, str]]."""
    user_answer_list = user_answer.split(",")

    for i in range(len(user_answer_list)):
        formatted_list = []
        for i in range(len(user_answer_list)):
            formatted_list.append(["", ""])
            for char in user_answer_list[i]:
                if char.isdigit():
                    formatted_list[i][0] += char # Add numbers to first list item.
                else:
                    formatted_list[i][1] += char.upper() # Add letters to second list item.
            
        formatted_list = [[int(i[0]), i[1]] for i in formatted_list] # Make numbers to integers
        
        # Check for invalid input values in either the letters or numbers provided.
        integer_list = [i[0] for i in formatted_list]
        letter_list = [i[1] for i in formatted_list]

        for i in range(len(integer_list)):
            if (integer_list[i] not in options_dict_numeric.keys() or
            letter_list[i] not in options_dict.keys()):
                break

        else:
            # If all processed inputs are valid.
            return formatted_list
        
        # If input is invalid:
        return("InvalidInput")

# ==================================== Print ====================================

def print_keys(study_dict):
    """Prints all the keys of the dictionary each on its own line."""
    print("Word bank:")
    
    for key in study_dict:
        print(key)

def print_words_from_options_dict(options_dict):
    """Prints each key and one-line phrase definition from a given dictionary."""
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def print_from_options_dict(options_dict):
    """Prints options A-E from an options dict, separating answer lists onto new \
        lines for printing."""
    for key in options_dict:
        print(f"{key}: {"\n   ".join(options_dict[key])}")
        print("-" * 79)

def print_select_all(options_dict: dict[int, str]):
    """
    Prints select all options.
    
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
        if i == len(list_to_print) - 1:
            print(list_to_print[i])
        else:
            print(f"{list_to_print[i]}, ")


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

def print_menu(file_name = ""):
    NUMBER_OF_LINES = 50

    print("Welcome to Study Set!")
    print("By Emily Lim. 2026.")
    print("=" * NUMBER_OF_LINES, "\n")

    if (file_name != ""):
        print(f"File loaded: {file_name}\n")
    print("Program options:\n")

    print("Press 'mcqdef' to be quizzed with mcq questions with definitions as answers.")
    print("Press 'mcqkey' to be quizzed with MCQ questions with key terms as answers.")
    print("Press 'selectall' to be quizzed with Select All questions (definitions as answers).")
    print("Press 'w' to be quizzed by writing the key term corresponding to the definition.")
    print("Press 'm' to be quizzed by matching key terms to definitions.")
    print("Press 'fc' for flashcard mode of studying.")
    print("Press 'chr' to be quizzed with ordering questions on key terms.")
    print("Press 'readscore' to see your saved scores.")

    print("\nSettings")
    print("=" * NUMBER_OF_LINES, "\n")
    print("Press 'c' to create a study set.")
    print("Press 's' to save a created study set to a csv file.")
    print("Press 'e' to edit a study set you have loaded.")
    print("Press 'r' to read a study set from a csv file.")
    print("Enter 'pdf' to print a test to pdf from  study set.")

    print("Press 'exit' to quit.")

#=============================== Study Set Creation =======================================
def enter_data():
    """Gets user to input study set and returns a dictionary."""
    # Initializes data entry mode.
    print("Data Entry: Enter key terms and definitions as prompted.\nEnter 'done' to quit.")
    entry_dict = {}
    key = input("Input key term: ")
    
    while key != 'done':

        # Initialize choice and check if key in dictionary.
        if key in entry_dict:
            choice = existing_term_handling(entry_dict, key)
        else:
            choice = "o"
        
        definition_list = [] 
        def_input = ""

        while True:
            # Existing term handling of delete and skip.
            if choice == "del":
                del entry_dict[key]
                break

            if choice == "skip":
                break

            # Allows user to enter all related definitions for the key term.
            def_input = input("Input definition(s) of key term or 'f' to finish this term: ")

            if def_input == "f":
                break

            definition_list.append(def_input)

        # Updates study set dictionary and allows user to enter next key terms.
        if choice == "add":
            entry_dict[key].extend(definition_list)
        
        if choice == "o":
            entry_dict[key] = definition_list

        key = input("Input key term: ")
    
    # Gets user to name dictionary for score saving purposes.
    study_set_name = input("Enter temporary name for study set: ")
    
    return entry_dict, study_set_name

def existing_term_handling(entry_dict, key):
    """
    Handles existing terms which the user attempts to enter again. Asks user if they would
    like to overwrite the original entry, delete it, add to it, or continue.

    Parameters:
        entry_dict (dict[str: str | list [str]]): dictionary being created.
        key (str): the key which is repeated and must be edited.
    
    Returns:
        choice (str): "o" if user wishes to overwrite previous entry, "del" if user
        wishes to delete previous entry, "skip" if user doesn't want to do anything,
        or "add" if user wants to add to previous entry.

    """
    # Print existing key to alert user to error.
    print(f"{key}:")
    
    if len(entry_dict[key]) > 1:
        print("\n    ".join(entry_dict[key]))
    
    else:
        print(entry_dict[key])
    
    print("This term is already in study set.")
    choice = input("Enter 'o' to overwrite the existing entry.\n"\
                   "Enter 'del' to delete the existing entry.\n"\
                    "Enter 'skip' to enter a new, different key term.\n"\
                    "Enter 'add' to add to the existing entry: ")
    return choice

# ================= Other / Misc. =======================================================

def get_dict_key(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key

def check_file_loaded(is_file_loaded, 
                      error_msg="File not loaded. You must load a file first."):
    """Checks if file is loaded and prints error message otherwise."""
    
    if is_file_loaded != True:
        print(error_msg)
        input("Press any key to continue...")

    return is_file_loaded

def pause_input(msg="\nPress any key to continue..."):
    """Pause the program to ask by using an input, can use different messages."""
    input(msg)

# ==================================== Score Saving ====================================

def ask_to_save_score(study_set_name, section, score):
    """
    Asks user if they would like to save score and calls save_score function.
    
    Parameters:
        study_set_name (str): name of the study set currently loaded. 
        section (str): name of the mode they are currently using. 
        score (float): float as a percent out of 100 that is the score of the user.
    
    Returns None.

    """
    user_input = input("Press 'y' to save your score or any other key"\
                       " to return to the main menu: ")
    if user_input == "y":
        save_score(study_set_name, section, score)


def reformat_scores_list(list):
    """
    Processes a given list of scores and returns the rows and overall score.
    
    Parameters:
        list (list[str]): list of strings read from a txt file.

    Returns:
        list_to_return (list[str]): each attempt and score of the user as a string.
        overall_score (list): last line of the file; overall score of the user.
    
    """
    list_to_return = []
    
    # Remove empty rows from list.
    for row in list:
        if row:
            list_to_return.append(row)
    
    # Attempt to get the last item from the list and assign to overall_score.
    try:
        overall_score = list_to_return.pop()
        return list_to_return, overall_score
    
    except:
        overall_score = "FileNotWritten"
        input(overall_score)
        return list_to_return, overall_score


def create_score_attempt(time_string, score):
    """Takes a string representing the time and a score, formatting an attempt string"""
    string = time_string + " - You scored " + f"{score:.2f}%\n"
    return string


def create_overall_score(score):
    """Takes a float score and returns a 1st attempt overall score string"""
    string = f"Your overall score is {score:.2f}% after 1 attempt!\n"
    return string


def update_overall_score(list_of_history: list[str]):
    """Takes a list of all scores to update the overall score string."""
    past_score_list = []
    
    # Get float score percentage for all attempts and append to list.
    for row in list_of_history:
        if row:
            temp_list = row.split(" - You scored ")
            score = float(temp_list[1][:-2]) # Remove newline and percentage from scores.
            past_score_list.append(score)
    
    # Calculate average score and number of attempts from past_score_list.
    avg_score = sum(past_score_list) / len(past_score_list)
    num_attempts = len(past_score_list)

    # Create a new updated overall score string and return.
    string = f"Your overall score is {avg_score:.2f}% after {num_attempts} attempts!\n"
    
    return string

    
def save_score(study_set_name, section, score):
    """
    Saves user scores for a certain section of the studyset quizzes.
    
    Parameters:
        study_set_name (str): string representing the studyset being studied.
        section (str): string which describes the mode of studyset. 
        score (float): unrounded floating-point score of the user for that attempt.
    
    Returns None.
        
    """
    # Find current time to save score under.
    now = datetime.now()
    now_formatted = now.strftime("%Y/%m/%d %H:%M")
    
    # Find / create filename for the scores file of this study mode.
    section = study_set_name + "_" + section + "_scores.txt"
    section = os.path.join("user_data", section)
    section = os.path.abspath(section)

    # Create / open file and read contents to update (if any).
    if os.path.exists(section):
        with open(section, "r") as file:
            list_of_contents = []
            
            for line in file.readlines():
                list_of_contents.append(line)

            rewrite_list, overall_score = reformat_scores_list(list_of_contents)
            
            # If the user score file has existing attempts on record:
            rewrite_list.append(create_score_attempt(now_formatted, score))
                
            # Rewrite existing file contents
            with open(section, "w") as file2:
                for item in rewrite_list:
                    file2.write(item)
                    
                # Write the last overall score line.
                file2.write(update_overall_score(rewrite_list))

    # If the user score file for that section is empty:
    else:
        with open(section, "w") as file:
            file.write(create_score_attempt(now_formatted, score))
            file.write(create_overall_score(score))

# ======================= Read Score ====================================================

def read_score(study_set_name, study_mode):
    if study_mode not in ACCEPTED_STUDY_MODE_LIST:
        print("Invalid study mode. Returning to read score menu...")
        ask_to_read_score()

    try:
        filepath = study_set_name + "_" + study_mode + "_scores.txt"
        filepath = os.path.join("user_data", filepath)
        filepath = os.path.abspath(filepath)
        
        with open(filepath, "r") as score_file:
            contents = score_file.readlines()
            for line in contents:
                print(line, end="")

    except:
        input("File not found. Press any key to return to the score reading menu.")
        ask_to_read_score()


def read_all_scores(study_set_name):
    """Reads scores for all modes in a study set which have been played"""
    for mode in ACCEPTED_STUDY_MODE_LIST:
        # Create filepath for files
        filepath = study_set_name + "_" + mode + "_scores.txt"
        filepath = os.path.join("user_data", filepath)
        filepath = os.path.abspath(filepath)

        # For modes which have existing score files
        if os.path.exists(filepath):
            read_score(study_set_name, mode)
            print()

def ask_to_read_score():
    print("Would you like to read scores only from a specific mode of a study set?")
    print("Or would you like to read scores from all modes of a particular study set?")

    while True:
        user_choice = input("Enter 'mode' or 'all' or 'q' to exit: ")
        user_choice.strip().lower()
        
        # Handles incorrect inputs.
        if user_choice not in ACCEPTED_READ_SCORE_INPUTS:
            print("Invalid input. Try again...")
            continue
        
        # Returns user to Main Menu.
        elif user_choice == "q":
            break
        
        study_set_name = input("Enter name of study set: ")
        study_set_name.strip().lower()
        
        if user_choice == "mode":
            study_mode = input("Enter mode that you want scores from: ")
            read_score(study_set_name, study_mode)
            input("Press any key to return to the main menu...")
            break

        elif user_choice == "all":
            read_all_scores(study_set_name)
            input("Press any key to continue / return to the main menu...")
            break

#================================ Dictionary Editing Functions =================================================

def print_alpha_from_list(list):
    for i in range(len(list)):
        print(chr(ord("A") + i), end = "")
        print(":", list[i])

def get_dict_key_from_index(index, string_input, study_dict):
    term_index = int(string_input)
    validate_edit_term(index, term_index)
    term = list(study_dict.keys())[term_index - 1]
    return term

def validate_edit_term(index, term_index):
    if (term_index < index - 8) or term_index > index + 1:
        raise ValueError

def separate_string_from_int(string):
    """Takes a single string and splits the numeric characters into an int from string characters."""
    term_index = ""
    definition_char = ""

    for char in string:
        if char.isdigit():
            term_index += char
        else:
            definition_char += char

    return int(term_index), definition_char

def find_definition_string(char, term, study_dict):
    """
    Finds the definition string for removal.

    Parameters:
        char (str): character from A onwards representing the definition
        term (str): key in the study dictionary related to the definition to be found.
        study_dict (dict[str: list[str]]): dictionary of key terms and definition lists
    
    Returns:
        definition (str): the definition referenced by the character.
    
    """
    definition_index = ord(char.upper()) - ord("A")
    return study_dict[term][definition_index]

def delete_term_or_definition(index, study_dict):
    
    user_input = input("Enter term or definition to be deleted in the following format:\n" \
                            "1 for term 1, 1A for term 1 definition A or q to exit this edit mode: ").strip().upper()
    try:
        # Remove entire term with all its definitions
        if user_input.isdigit():
            term = get_dict_key_from_index(index, user_input, study_dict)
            del study_dict[term]
                                
        # Remove a specified definition from a specific term.
        else:
            term_index, definition_char = separate_string_from_int(user_input)
            term = get_dict_key_from_index(index, term_index, study_dict)
            definition_str = find_definition_string(definition_char, term, study_dict)
            study_dict[term].remove(definition_str)
                                
    except:
        input("Invalid input. Press any key to try again...")
        user_input = input("Enter term or definition to be deleted in the following format:\n" \
                            "1 for term 1, 1A for term 1 definition A or q to exit this edit mode:" ).strip()
        
def modify_term(index, study_dict):
    # Identify the term to be changed and the new wording.
    term_index = input("Enter the number of the term you would like to change\n"
                        "or enter 'q' to exit this edit mode: ")
    
    # Continue until user enters q to exit this mode.
    while term_index != "q":
        # try:
            # Find the definition, which must be added to the entry of the new term.
            old_term = get_dict_key_from_index(index, term_index, study_dict)
            definition = study_dict[old_term]
            new_term = input("Please enter the new key term for this definition: ")

            # Delete old term and replace with new term and same definition.
            del study_dict[old_term]
            study_dict[new_term] = definition

            term_index = input("Enter the number of the term you would like to change\n"
                               "or enter 'q' to flip to the next set of terms: ")
            
        # except:
        #     print("Invalid term index. Please enter a valid number.")

# Implement adding definitions
# Implement reprinting of the terms available to edit (fixes the last delete bugs)
# Ensure all excepts have new input methods
# Implement clearing
# Implement mandatory saving

def modify_def(index, study_dict):
    """Modifies a specific definition line for a certain term in the dictionary."""
    # Get user input / confirmation to proceed.
    raw_input = input("Enter the term number and definition letter to be changed (eg. 1A)\n"
                              "or enter 'q' to exit this edit mode: ")
    
    while raw_input != "q":
        # try:
            # Find term and definition index to be able to access the edited location.
            term_index, definition_char = separate_string_from_int(raw_input)
            key = get_dict_key_from_index(index, term_index, study_dict)
            definition_index = ord(definition_char.upper()) - ord("A")

            # Update this section of the definition
            new_definition = input("Enter the new definition: ")
            study_dict[key][definition_index] = new_definition

            raw_input = input("Enter the term number and definition letter to be changed (eg. 1A)\n"
                              "or enter 'q' to exit to another edit mode: ")
                            
        # except:
        #     print("Invalid entry. Please try again.")
        #     raw_input = input("Enter the term number and definition letter to be changed (eg. 1A)\n"
        #                       "or enter 'q' to exit to another edit mode: ")


def modify_study_set(study_dict):
    """Modifies study dict in place upon user's request."""
    
    print("Warning: if using chronological mode, do NOT modify the dictionary.")
    
    for index, key in enumerate(study_dict):
        
        # Print the 10 terms to preview.
        print(f"{index + 1}: {key}")
        print_alpha_from_list(study_dict[key])
        print("-" * 79)

        # Begin process every 10 entries or so.
        if (index + 1) % 10 == 0 or index == len(study_dict) - 1:
            should_continue = True
            
            while should_continue:
                user_choice = input("Would you like to modify anything?\n" \
                "Enter 'term' to modify a key term or 'def' to modify a definition or " \
                "'del' to delete a term or 'n' to continue or 'q' to exit edit mode: ")

                if user_choice == 'q':
                    return None 
                
                elif user_choice == "term":
                    modify_term(index, study_dict)
                
                elif user_choice == "def":
                    modify_def(index, study_dict)

                elif user_choice == "del":
                    delete_term_or_definition(index, study_dict)

                elif user_choice == "n":
                    should_continue = False
        
            clear_console()
    
    # Ask user to save updated study set.
    user_save = input("Would you like to save the updated dictionary? (y/n): ")
    if user_save == "y":
        save_data_to_csv(study_dict)

def latexify(string_list):
    for i in range(len(string_list)):
        for entry in LATEX_DICT:
            if entry == string_list[i]:
                string_list[i] = LATEX_DICT[entry]
        
        for entry in LATEX_NON_STRICT:
            if entry in string_list[i]:
                string_list[i] = LATEX_NON_STRICT[entry].join(string_list[i].split(entry))

def parse_parenthetical(string):
    string_list = string.split("(")
    string_list[1:1] = string_list[1].split(")")
    string_list[1:1] = string_list[1].split()
    
    latexify(string_list)
    return string_list[0] + "(" + " ".join(string_list[1:-1]) + ")" + string_list[-1]

def handle_parentheses(string_list):
    """
    Handles parentheses related issues, parsing the areas around parentheses
    and within them and recombining these entries for greater ease of use.
    """
    new_list = []
    long_string = ""
    accumulate = False
    for i in range(len(string_list)):    
        if "(" in string_list[i]:
            accumulate = True
        
        if accumulate:
            long_string += string_list[i]
        else:
            new_list.append(string_list[i])
 
        if ")" in string_list[i]:
            new_list.append(parse_parenthetical(long_string))
            accumulate = False
    return new_list

def manage_latexify(string):
    string_list = handle_parentheses(string.split())
    latexify(string_list)
    formatted_string = " ".join(string_list)
    return formatted_string