import os, platform, csv, random
import libs.chronological as chrono
import libs.check_question as check
from datetime import datetime

# Bunch of helper functions and stuff I couldn't find the place to actually
# sort them into. Very messy, I know :)

# ==================================== Constants =================================
ACCEPTED_READ_SCORE_INPUTS = ["mode", "all", "q"]
ACCEPTED_STUDY_MODE_LIST = ["mcqdef", "mcqkey", "write", "match", "selectall", "chron"]

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
    
    # Save study set name to variable and prepare file name for reading.
    if not(name.endswith(".csv")):
        study_set_name = name
        name += ".csv"
    else:
        study_set_name = name[:-4] # Remove .csv extension from name

    with open(name, "a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        print(os.path.abspath(name))
        
        # Write each row to the csv file.
        for key in entry_dict:
            list_to_write = [] # Clear list_to_write.
            list_to_write = [key] + entry_dict[key]
            csv_writer.writerow(list_to_write)

    input("Your file has been saved. Press any key to contine...")
    return study_set_name

def read_data_from_csv():
    """Takes csv file and reads csv file into test-ready dictionary."""
    csv_to_read = input("Input name of csv to read with extension: ")
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
    print("Welcome to Study Set!")
    print("By Emily Lim. 2026.")
    print("=" * 50, "\n")

    if (file_name != ""):
        print(f"File loaded: {file_name}\n")
    print("Program options:\n")


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
    print("Press 'readscore' to see your saved scores.")
    print("Press 'exit' to quit.")

#=============================== Study Set Creation =======================================
def enter_data():
    """Gets user to input study set and returns a dictionary."""
    # Initializes data entry mode.
    print("Data Entry: Enter key terms and definitions as prompted.\nEnter 'done' to quit.")
    entry_dict = {}
    key = input("Input key term: ")
    
    while key != 'done':
        definition_list = [] 
        def_input = ""

        while True:
            # Allows user to enter all related definitions for the key term.
            def_input = input("Input definition(s) of key term or 'f' to finish this term: ")

            if def_input == "f":
                break

            definition_list.append(def_input)

        # Updates study set dictionary and allows user to enter next key term.
        entry_dict[key] = definition_list
        key = input("Input key term: ")
    
    # Gets user to name dictionary for score saving purposes.
    study_set_name = input("Enter temporary name for study set: ")
    
    return entry_dict, study_set_name

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
    section = os.path.join("test_files", section)
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
        filepath = os.path.join("test_files", filepath)
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
        filepath = os.path.join("test_files", filepath)
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
