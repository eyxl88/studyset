import os, platform, csv, random
import libs.chronological as chrono
import libs.check_question as check
import datetime

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

def match_answers(study_dict, study_set_name):
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

    # Calculate, print, and save score.
    user_score = check.check_match_answer(user_input, options_dict_numeric, 
                                        options_dict, study_dict) * 100
    print(f"You scored {user_score:.2f}%!")
    ask_to_save_score(study_set_name, "match", user_score)

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
        print("File not found. Try again by pressing 'r' after the main menu prints. \
              Use a valid file name.")
        
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


def process_match_input(user_answer, study_dict):
    """Turns match string input into a list of lists in the form list[list[int, str]]."""
    user_answer_list = user_answer.split(",")

    for i in range(len(user_answer_list)):
        try:
            # Turns the first character of each list item into an int and the second character
            # into an upper case letter, then replaces the item with this list.
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
    """Prints each key and one-line phrase definition from a given dictionary."""
    for key in options_dict:
        print(f"{key}: {options_dict[key]}")

def print_from_options_dict(options_dict):
    """Prints options A-E from an options dict, separating answer lists onto new \
        lines for printing."""
    for key in options_dict:
        print(f"{key}: {"\n".join(options_dict[key])}")

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
        if i == len - 1:
            print(list_to_print[i])
        else:
            print(f"{list_to_print[i]}, ")

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

    for i in range(len(study_dict)):
        # Selects key term and prints question header.
        key_term = random.choice(list_of_keys)
        print("Question", i + 1, key_term)

        # Removes key term from list, finds answer, creates and prints options.
        list_of_keys.remove(key_term)
        answer = study_dict[key_term]
        options_dict = create_select_all(answer, study_dict.values())

        print_select_all(options_dict)
        
        while True:
            user_answer = input("Which of the following are correct? Enter a list \
                                of comma-separated numbers (ie. 1,3,7): ")
            
            # Allows user to return to main menu.
            if user_answer == "q":
                return None
            
            try:
                user_correct += check.check_select_all_answer(user_answer, 
                                                    answer, options_dict)
                break
            except:
                print("Invalid input. Try again.")

    # Print and save user score.
    user_score = user_correct / TOTAL * 100
    print(f"Your score is {user_correct} / {TOTAL} and"\
        f"your accuracy is {user_score:.2f}%.")
    ask_to_save_score(study_set_name, "selectall", user_score)


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

# ==================================== Write Mode ====================================

def write_mode(study_dict, study_set_name):
    """Sets up the 'write' test mode and checks answers."""
    list_of_keys = list(study_dict.keys())
    user_correct = 0
    TOTAL_POINTS = len(study_dict)
    
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
        while True:
            user_answer = input("Type the key term which corresponds"
                                    "to the given definition: ")
            if user_answer == "q":
                return 0
            
            try:
                user_correct += check.check_written_answer(user_answer, answer)
                break
            
            except:
                print("Invalid input. Try again.")

    # Calculate and save user score.
    user_score = user_correct / TOTAL_POINTS * 100
    print(f"You scored {user_score:.2f}%")
    ask_to_save_score(study_set_name, "write", user_score)

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
    
    return list_to_return, overall_score


def create_score_attempt(time_string, score):
    """Takes a string representing the time and a score, formatting an attempt string"""
    string = time_string + " - You scored " + f"{score:.2f}%"
    return string


def create_overall_score(score):
    """Takes a float score and returns a 1st attempt overall score string"""
    string = f"Your overall score is {score:.2f}% after 1 attempt!"
    return string


def update_overall_score(list_of_history: list[str]):
    """Takes a list of all scores to update the overall score string."""
    past_score_list = []
    
    # Get float score percentage for all attempts and append to list.
    for row in list_of_history:
        if row:
            temp_list = row.split(" - You scored ")
            score = float(temp_list[1][:-1])
            past_score_list.append(score)
    
    # Calculate average score and number of attempts from past_score_list.
    avg_score = sum(past_score_list) / len(past_score_list)
    num_attempts = len(past_score_list)

    # Create a new updated overall score string and return.
    string = f"Your overall score is {avg_score:.2f}% after {num_attempts} attempts!"
    
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
    now = datetime.now
    now_formatted = now.strftime("%Y/%m/%d %H:%M")
    
    # Find / create filename for the scores file of this study mode.
    section = study_set_name + "_" + section + "_scores.txt"

    # In case the section file is created in a different local folder.
    if os.path.exists(section):
        section = os.path.find(section)
    
    # Create / open file and read contents to update (if any).
    with open(section, "w+") as file:
        list_of_contents = file.readlines()
        rewrite_list, overall_score = reformat_scores_list(list_of_contents)
        
        # If the user score file for that section is empty:
        if overall_score == "FileNotWritten":
            file.write(create_score_attempt(now_formatted, score))
            file.write(create_overall_score(score))
        
        # If the user score file has existing attempts on record:
        else:
            rewrite_list.append(create_score_attempt(now_formatted, score))
            
            for item in rewrite_list:
                file.write(item)
            
            file.write(update_overall_score(rewrite_list))