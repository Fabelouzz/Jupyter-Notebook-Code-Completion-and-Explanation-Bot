import nbformat
import os
import openai
from dotenv import load_dotenv
import re

load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI()  # Initialize the OpenAI client
model = 'gpt-4o-mini'      # Specify the model to use

def read_notebook(file_path):
    """Read a Jupyter notebook file and parse it into a JSON object."""
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    return notebook

def extract_cells(notebook):
    """Extract markdown and code cells, removing large base64 image strings from markdown."""
    cells = notebook['cells']
    paired_cells = []  # List of tuples in the form (markdown_instructions, code_cell)

    current_markdown = []
    image_pattern = re.compile(r'!\[.*?\]\(data:image/(?:png|jpg|jpeg|gif);base64,[^\)]+\)')

    for cell in cells:
        if cell['cell_type'] == 'markdown':
            clean_source = re.sub(image_pattern, '', cell['source'])
            current_markdown.append(clean_source)
        elif cell['cell_type'] == 'code':
            paired_cells.append((current_markdown, cell))
            current_markdown = []  # Reset markdown for the next pair

    return paired_cells

def filter_relevant_cells(paired_cells):
    """
    Combine irrelevant code and markdown cells as instructions for the next relevant code cell 
    that includes any variation of the phrase 'start code here', case insensitive.
    """
    relevant_cells = []
    accumulated_instructions = []
    start_code_pattern = re.compile(r'#.*start\s*code\s*here', re.IGNORECASE)

    for markdown_instructions, code_cell in paired_cells:
        combined_markdown = "\n".join(markdown_instructions)
        if not start_code_pattern.search(code_cell['source']):
            accumulated_instructions.append(f"Markdown Instructions:\n{combined_markdown}")
            accumulated_instructions.append(f"Previous Code:\n{code_cell['source']}")
        else:
            full_instructions = "\n\n".join(accumulated_instructions) + f"\n\nMarkdown Instructions:\n{combined_markdown}"
            relevant_cells.append(([full_instructions], code_cell))
            accumulated_instructions = []  # Reset the accumulated instructions

    return relevant_cells

def generate_prompt(markdown_instructions, code):
    instructions_text = "\n".join(markdown_instructions)
    prompt = (
        f"Below are the instructions and previous code:\n\n"
        f"{instructions_text}\n\n"
        f"Current Code Cell:\n{code}\n\n"
        f"Complete the code in the 'Current Code Cell' based on the instructions. "
        f"Only return the code itself, as it will be placed in a code cell in a Jupyter notebook."
    )
    return prompt

def generate_explanation(code):
    """Generate an explanation for the given code using the OpenAI API."""
    prompt = f"Explain the functionality of the following Python code:\n\n{code}\n\n"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.with_raw_response.create(
        messages=messages,
        model="gpt-4o-mini",
    )
    explanation = response.parse().choices[0].message.content.strip()
    return explanation

def complete_code(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.with_raw_response.create(
        messages=messages,
        model="gpt-4o-mini",
    )
    completed_code = response.parse().choices[0].message.content.strip()
    return completed_code

def save_code_and_explanation(index, code, explanation, file_path="code_explanations.txt"):
    """Save the code and its explanation to a text file."""
    with open(file_path, 'a') as f:
        f.write(f"Code Snippet {index}:\n")
        f.write(f"{code}\n\n")
        f.write(f"Explanation:\n{explanation}\n")
        f.write("="*50 + "\n\n")

def update_notebook(notebook, paired_cells):
    for i, (markdown_instructions, code_cell) in enumerate(paired_cells):
        current_code = code_cell['source']
        prompt = generate_prompt(markdown_instructions, current_code)
        completed_code = complete_code(prompt)

        # Get explanation for the completed code
        explanation = generate_explanation(completed_code)

        # Save code and explanation
        save_code_and_explanation(i, completed_code, explanation)

        # Update the notebook code cell
        code_cell['source'] = completed_code

def save_notebook(notebook, original_path):
    directory, original_filename = os.path.split(original_path)
    new_filename = f"updated_{original_filename}"
    new_path = os.path.join(directory, new_filename)
    with open(new_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)
    print(f"Notebook saved as {new_path}")

def process_notebook(file_path):
    notebook = read_notebook(file_path)
    paired_cells = extract_cells(notebook)
    relevant_cells = filter_relevant_cells(paired_cells)
    update_notebook(notebook, relevant_cells)
    save_notebook(notebook, file_path)

# Example usage:
file_path = "jupyter.ipynb"
process_notebook(file_path)