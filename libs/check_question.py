import libs.utils as utils

# All answer checking found here.

def check_answer(user_answer, answer, options_dict):
    try:
        user_answer.upper().strip()
        if answer == options_dict[user_answer]:
            print("Correct")
            print()
        else:
            user_answer = input("Incorrect. One last try: ")
            if answer == options_dict[user_answer]:
                print("Correct")
                print()
            else:
                print(f"The correct answer is {"\n".join(answer)}")
                print()
    except:
        print("Invalid entry. Moving to next question.\n")

def check_answer_one_word(user_answer, answer, options_dict):
    try:
        user_answer.upper().strip()
        if answer == options_dict[user_answer]:
            print("Correct")
            print()
        else:
            user_answer = input("Incorrect. One last try: ")
            if answer == options_dict[user_answer]:
                print("Correct")
                print()
            else:
                print(f"The correct answer is {answer}")
                print()
    except:
        print("Invalid entry. Moving to next question.\n")

def check_select_all_answer(user_answer, answer, options_dict):
    # Turn user answer string into user answer list.
    user_answer = user_answer.split(",")
    # Remove blank entries from the user answer list.
    user_answer = [int(i) for i in user_answer if i.isspace() != True]
    user_answer.sort()
    user_total = 0
    user_correct_answers = []
    user_incorrect_answers = []
    correct_total = len(answer)

    for num in user_answer:
        if options_dict[num] in answer:
            user_total += 1
            user_correct_answers.append(num)
        else:
            user_incorrect_answers.append(num)

    if user_total == correct_total and len(user_incorrect_answers) == 0:
        print(f"Correct! You selected {user_total}/{correct_total} correct answers and 0 wrong answers!")

    elif user_total == correct_total and len(user_incorrect_answers) != 0:
        print(f"Almost there! You selected {user_total}/{correct_total} correct\
             answers and {len(user_incorrect_answers)} wrong answers!")
        print(f"The following answers were incorrect: {", ".join(user_incorrect_answers)}")   

    elif user_total != correct_total and len(user_incorrect_answers) != 0:
        print(f"Incorrect. You selected {user_total}/{correct_total} correct answers \
              and {len(user_incorrect_answers)} wrong answers!")
        print(f"The correct answers included:\n{"\n".join(answer)}")
        print(f"You additionally selected these wrong answers:")

        for i in range(len(user_incorrect_answers)):
            if i == len - 1:
                print(user_incorrect_answers[i])
            else:
                print(f"{user_incorrect_answers[i]}, ")
    else:
         print(f"Incorrect. You selected {user_total}/{correct_total} correct answers and 0 wrong answers.")
         print(f"The correct answers included:\n{"\n".join(answer)}")

def check_written_answer(user_answer, answer):
    """Checks written answers against actual answers and prints relevant messages."""
    user_answer = utils.process_text(user_answer)
    answer_processed = utils.process_text(answer)
    if user_answer == answer_processed:
        print("Correct.\n")
    
    elif user_answer in answer_processed:
        print(f"Close. The answer was '{answer}'.\n")
    
    elif answer_processed in user_answer:
        print(f"Almost there. The answer is just '{answer}'.\n")

    else:
        print(f"Incorrect. The answer is '{answer}'.\n")

def check_match_answer(user_answer, options_dict_numeric, options_dict, study_dict):
    """Takes user answer, the matching option dictionaries, and actual study set to check if answers are correct."""
    
    matches_correct = 0
    matches_wrong = []
    right_matches = []
    TOTAL_POINTS = len(study_dict)
    user_answer = utils.process_match_input(user_answer)
    
    for list in user_answer:
        key = options_dict_numeric[list[0]]
        answer = options_dict[list[1]]
        
        if study_dict[key] == answer:
            matches_correct += 1
        
        else:
            matches_wrong.append(f"{list[0]}{list[1]}")
            right_matches.append(f"{list[0]}{utils.get_dict_key(options_dict, study_dict[key])}")
    
    if matches_correct == TOTAL_POINTS:
        print("All correct! Good job.")
    
    else:
        print(f"Incorrect, you scored {matches_correct} / {TOTAL_POINTS}.")
        print("Incorrect matches:")

        for i in range(len(matches_wrong)):
            print(f"{matches_wrong[i]} should be {right_matches[i]}")

        print()