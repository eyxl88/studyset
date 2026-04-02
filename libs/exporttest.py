from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os, random
import libs.chronological as chrono
import libs.utils as utils
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

ACCEPTED_QUESTION_MODES = ["selectall", "chron", "w", "m", "mcqdef", "mcqkey"]
LETTER_COLORS = {
    "A": colors.green,
    "B": colors.blue,
    "C": colors.orange,
    "D": colors.purple,
    "E": colors.red,
}

def write_words_from_options_dict(options_dict):
    """Prints each key and one-line phrase definition from a given dictionary."""
    test_options = ""
    for key in options_dict:
        test_options += f"{key}: {options_dict[key]}\n"
    return test_options

def get_options_list(answer, study_dict_object):
    """
    Creates options list with 4 incorrect options and the given answer.
    """
    options_list = [answer]
    incorrect_options = list(study_dict_object)
    incorrect_options.remove(answer)

    for i in range(4):
        selected = random.choice(incorrect_options)
        incorrect_options.remove(selected)
        options_list.append(selected)
    
    random.shuffle(options_list)
    return options_list

def mcqkey_test(study_dict):
    """
    Creates a full set of randomized MCQ questions and the answer key.
    
    Parameters:
        study_dict (dict[str, list[str]]): dictionary containing key terms and definitions as values.
    
    Returns:
        test_lines (str): a string containing all test questions and options, formatted.
        answer_key (str): the correct answers to each question.
    """
    list_of_values = list(study_dict.values())
    test_lines = ""
    answer_key = []

    for i in range(len(study_dict)):

        # Create question and remove from list.
        definition = random.choice(list_of_values)
        list_of_values.remove(definition)
        
        # Add question and options to test material.
        test_lines += f"Question {i + 1} out of {len(study_dict)}:\n"
        answer_key_row = [i + 1]

        for row in definition:
            test_lines += f"{row}\n"
        
        # Set up answer and options.
        answer = utils.get_dict_key(study_dict, definition)
        
        options_list = get_options_list(answer, study_dict.keys())
        options_dict = chrono.create_chronological(options_list)

        # Write into test lines
        test_lines += write_words_from_options_dict(options_dict)
        test_lines += "_" * 79 + "\n"

        # Write into answer key lines.
        answer_letter = utils.get_dict_key(options_dict, answer)
        answer_key_row.append(answer_letter)
        answer_key_row.append(answer)
        answer_key.append(answer_key_row)
    
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


def build_answer_sheet(filepath, data):
    """
    Parameters:
        filepath (str): path to save the file
        data (list [list[int | str]]): nested 2D list containing lists of question
        number, answer letter, and written answer.
    """

    pdf = SimpleDocTemplate(filepath, pagesize=letter)

    # Header row
    table_data = [["Q#", "Ans", "Written Answer"]]

    # Add rows
    for row in data:
        table_data.append(row)

    # Column widths: narrow | narrow | wide
    table = Table(table_data, colWidths=[40, 40, 400])

    # Style
    style = TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), colors.lightseagreen),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 12),

        # Body text
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "TOP"),

        # Padding
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),

        # Grid
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
    ])

    # Alternating row colors
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            style.add("BACKGROUND", (0,i), (-1,i), colors.whitesmoke)
    
    # Color‑code the answer column
    for i in range(1, len(table_data)):
        letter = str(table_data[i][1]).strip().upper()
        if letter in LETTER_COLORS:
            style.add("TEXTCOLOR", (1, i), (1, i), LETTER_COLORS[letter])
            style.add("FONTNAME", (1, i), (1, i), "Helvetica-Bold")
    table.setStyle(style)

    pdf.build([table])

def get_question_type():
    question_call = ""
    time = 0
    input("outside loop")
    while question_call not in ACCEPTED_QUESTION_MODES:
        if time > 1:
            print("Invalid question mode. Try again.")
            
        question_call = input("Enter the mode of question to be created (mcqdef, mcqkey,\n" \
            "selectall, m, chron, or w: ").strip().lower()
        
        time += 1
    
    return question_call

def create_test(study_dict, function):
    # Get text to write.
    test_lines, answer_lines = function(study_dict)
    test_lines = test_lines.split("\n")
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
    build_answer_sheet(answer_filepath, answer_lines)
    print("Test and answer keys created successfully.")
    input("Press any key to return to the main menu... ")

def manage_single_question(study_dict):
    question_call = get_question_type()
    input("Post question call")
               
    if question_call == "mcqdef":
        pass

    elif question_call == "mcqkey":
        create_test(study_dict, mcqkey_test)

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
    """
    Initializes the function calls for the rest of the pdf functionality.

    Parameters:
        study_dict: dictionary of key terms and definitions to be printed as a quiz
    Returns:
        None

    """
    question_types = input("Would you like to see 1 type of question or multiple?\n"\
                        "Enter '1' for 1 type or 'm' for multiple: ")

    if question_types == "1":
        manage_single_question(study_dict)
    
    elif question_types == "m":
        manage_multi_question(study_dict)
        