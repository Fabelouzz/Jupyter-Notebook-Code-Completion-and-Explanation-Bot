# Jupyter Notebook Code Completion Bot

This project provides an automated code solution for Jupyter notebooks by leveraging OpenAI's Assistant and ChatCompletion API. It consists of two main components:

## Components

### Assistant Notebook (`assistant_bot.ipynb`)
A Jupyter Notebook that utilizes the OpenAI Assistant API to complete code cells based on preceding markdown instructions and existing code. It maintains context across cells, keeping contextually accurate code completions.

### Chat Completion Bot (`chat_completion_bot.py`)
A Python script that employs OpenAI's ChatCompletion API to automate code completion within Jupyter notebooks. For every completed code block, the bot generates detailed explanations and saves them to a text file (`code_explanations.txt`). This helps with better understanding and documentation of the generated code.

## Features

- **Automated Code Completion:**  
  Automatically completes incomplete code cells in Jupyter notebooks based on markdown instructions and existing code snippets.
  
- **Explanatory Documentation:**  
  Generates explanations for each completed code block, improving the maintainability of the notebook.

- **Contextual Understanding:**  
  Accumulates and utilizes relevant markdown instructions and previous code to ensure that code completions are contextually appropriate.

- **Logging and Monitoring:**  
  Implements logging to monitor the bot's activities, track execution times, and handle errors.

- **Environment Configuration:**  
  Utilizes `.env` files for secure management of OpenAI API keys and other sensitive configurations.

## Getting Started

### 1. Clone the Repository:
```bash
git clone https://github.com/yourusername/jupyter-code-completion-bot.git
cd jupyter-code-completion-bot
```
### 2. Set up the Environment:
```bash
pip install -r requirements.txt
```
Add your OpenAI API key in the .env file.

### 3. Run the Code: 
You can run either the chat_completion_bot.py or the assistant_bot.ipynb. Make sure to set the path correctly to match the name of the Jupyter notebook you want to complete. It is initially set to "jupyter.ipynb" in the current directory. An updated notebook named "updated_jupyter.ipynb" will be saved, along with a text file (code_explanations.txt) containing the explanations.

### Project Structure
```bash
jupyter-code-completion-bot/
├── assistant_bot.ipynb
├── chat_completion_bot.py
├── code_explanations.txt
├── requirements.txt
├── .env.example
└── README.md
```

### Contributing
Contributions are welcome! Please fork the repository and create a pull request with your enhancements.

