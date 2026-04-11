from typing import Any
import libs.utils as utils
from libs.chronological import chronological
from libs.questions import multiple_choice, multiple_choice_flipped, flashcard, write_mode, match_answers, select_all
from libs.utils import check_file_loaded
from libs.exporttest import initialize_pdf
import os
import pickle

# Check files files inside ./libs folder for all the code that was once here.
# If you need help finding everything, let me know!
# - Asley

# Global Constants
NEWEST_DICT: dict[Any, Any] = {}
ACCEPTED_USER_INPUTS: list[str] = ['exit', 'c', 's', 'r', 'merge', 'mcqdef', 
                        'mcqkey', 'selectall', 'e', 'pdf',
                        'w', 'm', 'fc', 'chr', 'readscore']

# Main program loop
def main():
    """
    Main program file. Starts the program loop.
    """
    is_file_loaded = False
    study_set_name = ""

    # Sets up the main menu
    utils.clear_console()
    utils.print_menu()

    user_input = input("\nSelect one option: ")
    while user_input != 'exit':
        if user_input in ACCEPTED_USER_INPUTS:

            if user_input == 'c':
                NEWEST_DICT, study_set_name = utils.enter_data()
                is_file_loaded = True

            elif user_input == 's' and check_file_loaded(is_file_loaded):
                study_set_name, file_name = utils.save_data_to_csv(NEWEST_DICT)
                NEWEST_DICT = utils.read_data_from_csv(os.path.join("test_files", file_name.split(os.path.sep)[-1]))[0] # TUPLE SLICED!

            elif user_input == 'e' and check_file_loaded(is_file_loaded):
                utils.modify_study_set(NEWEST_DICT)

            elif user_input == 'r':
                file_name = input("Input name of csv to read with extension: ")
                NEWEST_DICT, study_set_name = utils.handle_read_data_from_csv(file_name)
                if NEWEST_DICT != None:
                    if len(NEWEST_DICT) != 0:
                        is_file_loaded = True
            
            elif user_input == "merge":
                NEWEST_DICT, study_set_name = utils.merge_dicts()

            elif user_input == 'mcqdef' and check_file_loaded(is_file_loaded):
                multiple_choice(NEWEST_DICT, study_set_name)

            elif user_input == 'mcqkey' and check_file_loaded(is_file_loaded):
                multiple_choice_flipped(NEWEST_DICT, study_set_name)

            elif user_input == "selectall" and check_file_loaded(is_file_loaded):
                select_all(NEWEST_DICT, study_set_name)

            elif user_input == "w" and check_file_loaded(is_file_loaded):
                write_mode(NEWEST_DICT, study_set_name)

            elif user_input == "m" and check_file_loaded(is_file_loaded):
                match_answers(NEWEST_DICT, study_set_name)

            elif user_input == "fc" and check_file_loaded(is_file_loaded):
                flashcard(NEWEST_DICT)

            elif user_input == "chr" and check_file_loaded(is_file_loaded):
                chronological(NEWEST_DICT, study_set_name)

            elif user_input == "readscore":
                utils.ask_to_read_score()
            
            elif user_input == "pdf" and check_file_loaded(is_file_loaded):
                initialize_pdf(NEWEST_DICT)
        
        else:
            # User input is not valid.
            print("\nIncorrect option. Try again.")
            input("Press any key to continue...")

        # Re-print the menu
        utils.clear_console()
        if is_file_loaded and study_set_name != None:
            utils.print_menu(study_set_name.split(os.path.sep)[-1]) # Get last item when spliting abs path
        else:
            utils.print_menu()

        user_input = input("\nSelect one option: ")

    else:
        # After quitting the program. Clean the console.
        utils.clear_console()


# Initialize the program
try:
    main()

except:
    try:
        print("An unpreventable error has occured. Emergency saving activated...")
        utils.save_data_to_csv(NEWEST_DICT)
    except:
        with open(os.path.abspath(os.path.join("test_files", "backup.pkl")), "w") as f1:
            pickle.dump((NEWEST_DICT), f1)
    
    print("An error has occurred...Restarting main...")
    main()

    