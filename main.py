from typing import Any
import libs.utils as utils
from libs.chronological import chronological
from libs.questions import multiple_choice, multiple_choice_flipped, flashcard, write_mode, match_answers, select_all
from libs.utils import check_file_loaded

# Check files files inside ./libs folder for all the code that was once here.
# If you need help finding everything, let me know!
# - Asley

# Global Constants
NEWEST_DICT: dict[Any, Any] = {}
ACCEPTED_USER_INPUTS: list[str] = ['exit', 'c', 's', 'r', 'mcqdef', 
                        'mcqkey', 'selectall',
                        'w', 'm', 'fc', 'chr', 'readscore']

# Main program loop
def main():
    """
    Main program file. Starts the program loop.
    """

    # Sets up the main menu
    utils.clear_console()
    utils.print_menu()

    is_file_loaded = False
    study_set_name = ""

    user_input = input()
    while user_input != 'exit':
        if user_input in ACCEPTED_USER_INPUTS:

            if user_input == 'c':
                NEWEST_DICT, study_set_name = utils.enter_data()
                is_file_loaded = True

            elif user_input == 's' and check_file_loaded(is_file_loaded):
                study_set_name = utils.save_data_to_csv(NEWEST_DICT)

            elif user_input == 'r':
                NEWEST_DICT, study_set_name = utils.read_data_from_csv()
                if len(NEWEST_DICT) != 0:
                    is_file_loaded = True

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
        
        else:
            # User input is not valid.
            print("\nIncorrect option. Try again.")
            input("Press any key to continue...")

        # Re-print the menu
        utils.clear_console()
        utils.print_menu()
        user_input = input()

    else:
        # After quitting the program. Clean the console.
        utils.clear_console()

# Initialize the program
main()