from typing import Any
import libs.utils as utils
from libs.chronological import chronological
from libs.questions import multiple_choice, multiple_choice_flipped, flashcard

# Check files files inside ./libs folder for all the code that was once here.
# If you need help finding everything, let me know!
# - Asley

# Global Constants
NEWEST_DICT: dict[Any, Any] = {}
ACCEPTED_USER_INPUTS: list[str] = ['q', 'c', 's', 'r', 'mcqdef', 
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

    user_input = input()
    while user_input != 'q':
        if user_input in ACCEPTED_USER_INPUTS:

            if user_input == 'c':
                NEWEST_DICT = utils.enter_data()

            elif user_input == 's':
                utils.save_data_to_csv(NEWEST_DICT)

            elif user_input == 'r':
                NEWEST_DICT = utils.read_data_from_csv()

            elif user_input == 'mcqdef':
                multiple_choice(NEWEST_DICT)

            elif user_input == 'mcqkey':
                multiple_choice_flipped(NEWEST_DICT)

            elif user_input == "selectall":
                utils.select_all(NEWEST_DICT)

            elif user_input == "w":
                utils.write_data(NEWEST_DICT)

            elif user_input == "m":
                utils.match_answers(NEWEST_DICT)

            elif user_input == "fc":
                flashcard(NEWEST_DICT)

            elif user_input == "chr":
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