from typing import Any
import libs.utils as utils
from libs.chronological import chronological
from libs.questions import multiple_choice, multiple_choice_flipped, flashcard
from libs.utils import check_file_loaded

# Check files files inside ./libs folder for all the code that was once here.
# If you need help finding everything, let me know!
# - Asley

# Global Constants
NEWEST_DICT: dict[Any, Any] = {}
ACCEPTED_USER_INPUTS: list[str] = ['exit', 'c', 's', 'r', 'mcqdef', 
                        'mcqkey', 'selectall', 'selectall', 
                        'w', 'm', 'fc', 'chr']

# Main program loop
def main():
    """
    Main program file. Starts the program loop.
    """

    # Sets up the main menu
    utils.clear_console()
    utils.print_menu()

    is_file_loaded = False

    user_input = input()
    while user_input != 'exit':
        if user_input in ACCEPTED_USER_INPUTS:

            if user_input == 'c':
                NEWEST_DICT = utils.enter_data()
                is_file_loaded = True

            elif user_input == 's' and check_file_loaded(is_file_loaded):
                utils.save_data_to_csv(NEWEST_DICT)

            elif user_input == 'r':
                NEWEST_DICT = utils.read_data_from_csv()
                if len(NEWEST_DICT) != 0:
                    is_file_loaded = True

            elif user_input == 'mcqdef' and check_file_loaded(is_file_loaded):
                multiple_choice(NEWEST_DICT)

            elif user_input == 'mcqkey' and check_file_loaded(is_file_loaded):
                multiple_choice_flipped(NEWEST_DICT)

            elif user_input == "selectall" and check_file_loaded(is_file_loaded):
                utils.select_all(NEWEST_DICT)

            elif user_input == "w" and check_file_loaded(is_file_loaded):
                utils.write_data(NEWEST_DICT)

            elif user_input == "m" and check_file_loaded(is_file_loaded):
                utils.match_answers(NEWEST_DICT)

            elif user_input == "fc" and check_file_loaded(is_file_loaded):
                flashcard(NEWEST_DICT)

            elif user_input == "chr" and check_file_loaded(is_file_loaded):
                chronological(NEWEST_DICT)
        
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