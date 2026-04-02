from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os, random
import libs.chronological as chrono
import utils

ACCEPTED_QUESTION_MODES = ["selectall", "chr", "w", "m", ""]

def write_words_from_options_dict(options_dict):
    """Prints each key and one-line phrase definition from a given dictionary."""
    test_options = ""
    for key in options_dict:
        test_options += f"{key}: {options_dict[key]}\n"
    return test_options

def mcqkey_test(study_dict):
    """
    Creates a full set of randomized MCQ questions and the answer key.
    
    Parameters:
        study_dict (dict[str, list[str]]): dictionary containing key terms and definitions as values.
    
    Returns:
        test_lines (str): a string containing all test questions and options, formatted.
        answer_key (str): the correct answers to each question.
    """
    list_of_values = study_dict.values()
    test_lines = ""
    answer_key = ""

    for i in range(len(study_dict)):

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Add question and options to test material.
        test_lines += f"Question {i + 1} out of {len(study_dict)}:\n"
        answer_key += f"Question {i + 1} out of {len(study_dict)}: "

        for row in definition:
            test_lines += f"{row}\n"
        
        # Set up answer and options.
        answer = utils.get_dict_key(study_dict, definition)
        
        options_list = [answer]
        options_list.extend(study_dict.keys())
        options_dict = chrono.create_chronological(answer)
        test_lines += write_words_from_options_dict(options_dict)
        test_lines += "_" * 79 + "\n"

        answer_letter = utils.get_dict_key(options_dict, definition)
        answer_key += str(answer_letter) + "\n"
        answer_key += str(answer) + "\n"
    
    return test_lines, answer_key


def create_pdf(file_path, text_lines):
    """
    Creates a PDF file with the given text lines.

    Parameters:
        file_path: Path where the PDF will be saved.
        text_lines: List of strings to write into the PDF.
    """
    try:
        # Create a canvas object for PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Set title and font
        c.setTitle("Generated PDF")
        c.setFont("Helvetica", 12)

        # Starting position for text
        y_position = height - 50

        for line in text_lines:
            c.drawString(50, y_position, line)
            y_position -= 20  # Move down for next line

            # If page is full, create a new page
            if y_position < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

        # Save the PDF
        c.save()
        print(f"PDF created successfully at: {os.path.abspath(file_path)}")

    except Exception as e:
        print(f"Error creating PDF: {e}")

def get_question_type():
    question_call = ""
    time = 0

    while question_call not in ACCEPTED_QUESTION_MODES:
        if time > 1:
            print("Invalid question mode. Try again.")
            
        question_call = input("Enter the mode of question to be created (mcqdef, mcqkey,\n" \
            "selectall, m, chron, or w: ").strip().lower()
        
        time += 1
    
    return question_call

def create_mcqkey_test(study_dict):
    # Get text to write.
    test_lines, answer_lines = mcqkey_test(study_dict)
    test_lines = test_lines.split("\n")
    answer_lines = answer_lines.split("\n")
    create_save_test(test_lines, answer_lines)

def create_save_test(test_lines, answer_lines):

    # Get and process user input on filename.
    user_input = input("Enter name for this test without extension: ")
    filename = ""
    for letter in user_input.strip():
        if letter == " ":
            filename += "_"
        if letter.isalpha():
            filename += letter
        if letter == ".":
            break
    
    # Create filepaths.
    test_filename = filename + "_test.pdf"
    answer_filename = filename + "_answers.pdf"
    test_filepath = os.path.join(os.path.abspath("test_files"), test_filename)
    answer_filepath = os.path.join(os.path.abspath("test_files"), answer_filename)

    create_pdf(test_filepath, test_lines)
    create_pdf(answer_filepath, answer_lines)
    print("Test and answer keys created successfully.")
    print("Test at", test_filepath)
    print("Answer key at", answer_filepath)
    input("Press any key to return to the main menu... ")

def manage_single_question(study_dict):
    question_call = get_question_type()
               
    if question_call == "mcqdef":
        pass

    elif question_call == "mcqkey":
        create_mcqkey_test(study_dict)

    elif question_call == "m":
        pass
    elif question_call == "w":
        pass
    elif question_call == "selectall":
        pass
    elif question_call == "chr":
        pass

def manage_multi_question(study_dict):
    pass

def initialize_pdf(study_dict):
    question_types = input("Would you like to see 1 type of question or multiple?\n"\
                        "Enter '1' for 1 type or 'm' for multiple: ")

    if question_types == "1":
        manage_single_question(study_dict)
    
    elif question_types == "m":
        manage_multi_question(study_dict)
        