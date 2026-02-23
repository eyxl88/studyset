from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os, random
import utils

ACCEPTED_QUESTION_MODES = ["selectall", "chr", "w", "m", ""]

def write_words_from_options_dict(options_dict):
    """Prints each key and one-line phrase definition from a given dictionary."""
    test_options = ""
    for key in options_dict:
        test_options += f"{key}: {options_dict[key]}\n"
    return test_options

def mcqdef_test(study_dict):
    """
    Docstring for mcqdef_test
    
    :param study_dict: Description
    """
    list_of_values = study_dict.values()
    test_lines = ""
    answer_key = ""

    for i in range(len(study_dict)):

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Add question and options to test material.
        test_lines += f"Question {i + 1}\n"
        answer_key += f"Question {i + 1}: "

        for row in definition:
            test_lines += f"{row}\n"
        
        # Set up answer and options.
        answer = utils.get_dict_key(study_dict, definition)
        answer_key += str(answer)
        
        options_dict = utils.create_options(answer, study_dict.keys())
        test_lines += write_words_from_options_dict(options_dict)
        test_lines += "_" * 79 + "\n"
        
        answer_letter = utils.get_dict_key(options_dict, definition)
        answer_key += str(answer_letter) + "\n"
    
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

pdf_name = input("Enter name of pdf to be saved without extension: ") + ".pdf"
question_types = input("Would you like to see 1 type of question or multiple?\n"\
                      "Enter '1' for 1 type or 'm' for multiple: ")

if question_types == "1":
    question_call = ""
    time = 0
    
    while question_call not in ACCEPTED_QUESTION_MODES:
        question_call = input("Enter the mode of question to be created (mcqdef, mcqkey,\n" \
        "selectall, m, chron, or w: ")
        
        if time > 1:
            print("Invalid question mode. Try again.")
        
        time += 1
    
    if question_call == "mcqdef":
        pass
    elif question_call == "mcqkey":
        pass
    elif question_call == "m":
        pass
    elif question_call == "w":
        pass
    elif question_call == "selectall":
        pass
    elif question_call == "chr":
        pass

lines = [
]
create_pdf(pdf_name, lines)